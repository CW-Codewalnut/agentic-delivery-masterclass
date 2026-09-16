"""Executable, dependency-free order-cancellation reference example.

This is an in-process teaching implementation, not a production service. The
store's single re-entrant lock makes the order mutation, event append, and
idempotency record atomic only inside one Python process.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from threading import RLock
from typing import Dict, Iterable, List, Optional, Tuple


class OrderStatus(str, Enum):
    PLACED = "placed"
    CONFIRMED = "confirmed"
    FULFILMENT_STARTED = "fulfilment_started"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"


class CancellationCode(str, Enum):
    CANCELLED = "cancelled"
    ALREADY_CANCELLED = "already_cancelled"
    NOT_FOUND = "not_found"
    NOT_OWNER = "not_owner"
    TOO_LATE = "too_late"
    VERSION_CONFLICT = "version_conflict"


class IdempotencyConflict(ValueError):
    """Raised when one idempotency key is reused for a different request."""


@dataclass(frozen=True)
class Order:
    order_id: str
    owner_id: str
    status: OrderStatus
    version: int = 1


@dataclass(frozen=True)
class CancellationEvent:
    order_id: str
    resulting_version: int
    event_type: str = "order.cancelled"


@dataclass(frozen=True)
class CancellationResult:
    order_id: str
    code: CancellationCode
    order_status: Optional[OrderStatus]
    order_version: Optional[int]


RequestFingerprint = Tuple[str, str, Optional[int]]
IdempotencyRecord = Tuple[RequestFingerprint, CancellationResult]


class InMemoryOrderStore:
    """Owns state and the lock defining the example's atomic boundary."""

    def __init__(self, orders: Iterable[Order] = ()) -> None:
        materialized = list(orders)
        self._orders: Dict[str, Order] = {order.order_id: order for order in materialized}
        if len(self._orders) != len(materialized):
            raise ValueError("order identifiers must be unique")
        self._idempotency: Dict[str, IdempotencyRecord] = {}
        self.events: List[CancellationEvent] = []
        self.lock = RLock()

    def get(self, order_id: str) -> Optional[Order]:
        with self.lock:
            return self._orders.get(order_id)

    def _put_locked(self, order: Order) -> None:
        self._orders[order.order_id] = order

    def _idempotency_locked(self, key: str) -> Optional[IdempotencyRecord]:
        return self._idempotency.get(key)

    def _remember_locked(
        self,
        key: str,
        fingerprint: RequestFingerprint,
        result: CancellationResult,
    ) -> None:
        self._idempotency[key] = (fingerprint, result)


class OrderCancellationService:
    CANCELLABLE_STATUSES = frozenset({OrderStatus.PLACED, OrderStatus.CONFIRMED})

    def __init__(self, store: InMemoryOrderStore) -> None:
        self.store = store

    def cancel(
        self,
        order_id: str,
        actor_id: str,
        idempotency_key: str,
        *,
        expected_version: Optional[int] = None,
    ) -> CancellationResult:
        if not order_id or not actor_id or not idempotency_key:
            raise ValueError("order_id, actor_id, and idempotency_key are required")

        fingerprint = (order_id, actor_id, expected_version)
        with self.store.lock:
            prior = self.store._idempotency_locked(idempotency_key)
            if prior is not None:
                prior_fingerprint, prior_result = prior
                if prior_fingerprint != fingerprint:
                    raise IdempotencyConflict(
                        "idempotency key already belongs to a different cancellation request"
                    )
                return prior_result

            order = self.store._orders.get(order_id)
            result = self._decide(order_id, order, actor_id, expected_version)

            if result.code is CancellationCode.CANCELLED:
                assert order is not None
                updated = replace(order, status=OrderStatus.CANCELLED, version=order.version + 1)
                self.store._put_locked(updated)
                self.store.events.append(
                    CancellationEvent(order_id=updated.order_id, resulting_version=updated.version)
                )
                result = CancellationResult(
                    order_id=updated.order_id,
                    code=CancellationCode.CANCELLED,
                    order_status=updated.status,
                    order_version=updated.version,
                )

            self.store._remember_locked(idempotency_key, fingerprint, result)
            return result

    def _decide(
        self,
        order_id: str,
        order: Optional[Order],
        actor_id: str,
        expected_version: Optional[int],
    ) -> CancellationResult:
        if order is None:
            return CancellationResult(order_id, CancellationCode.NOT_FOUND, None, None)
        if order.owner_id != actor_id:
            return self._result(order, CancellationCode.NOT_OWNER)
        # A completed cancellation is the human-visible outcome even when a
        # later intent carries a stale version. No write is still attempted.
        if order.status is OrderStatus.CANCELLED:
            return self._result(order, CancellationCode.ALREADY_CANCELLED)
        if expected_version is not None and expected_version != order.version:
            return self._result(order, CancellationCode.VERSION_CONFLICT)
        if order.status not in self.CANCELLABLE_STATUSES:
            return self._result(order, CancellationCode.TOO_LATE)
        return self._result(order, CancellationCode.CANCELLED)

    @staticmethod
    def _result(order: Order, code: CancellationCode) -> CancellationResult:
        return CancellationResult(order.order_id, code, order.status, order.version)
