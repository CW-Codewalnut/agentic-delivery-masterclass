from __future__ import annotations

import sys
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

EXAMPLE_DIR = Path(__file__).resolve().parents[1] / "worked-example"
sys.path.insert(0, str(EXAMPLE_DIR))

from order_cancellation import (  # noqa: E402
    CancellationCode,
    IdempotencyConflict,
    InMemoryOrderStore,
    Order,
    OrderCancellationService,
    OrderStatus,
)


class OrderCancellationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.store = InMemoryOrderStore(
            [Order(order_id="ORD-1042", owner_id="customer-7", status=OrderStatus.CONFIRMED)]
        )
        self.service = OrderCancellationService(self.store)

    def test_owner_can_cancel_before_fulfilment(self) -> None:
        result = self.service.cancel("ORD-1042", "customer-7", "req-001", expected_version=1)

        self.assertEqual(CancellationCode.CANCELLED, result.code)
        self.assertEqual(OrderStatus.CANCELLED, self.store.get("ORD-1042").status)
        self.assertEqual(2, self.store.get("ORD-1042").version)
        self.assertEqual(1, len(self.store.events))

    def test_owner_can_cancel_placed_order(self) -> None:
        store = InMemoryOrderStore(
            [Order(order_id="ORD-1043", owner_id="customer-7", status=OrderStatus.PLACED)]
        )

        result = OrderCancellationService(store).cancel(
            "ORD-1043", "customer-7", "req-placed", expected_version=1
        )

        self.assertEqual(CancellationCode.CANCELLED, result.code)
        self.assertEqual(OrderStatus.CANCELLED, store.get("ORD-1043").status)
        self.assertEqual(2, store.get("ORD-1043").version)
        self.assertEqual(1, len(store.events))

    def test_non_owner_is_refused_without_mutation(self) -> None:
        result = self.service.cancel("ORD-1042", "customer-8", "req-002")

        self.assertEqual(CancellationCode.NOT_OWNER, result.code)
        self.assertEqual(OrderStatus.CONFIRMED, self.store.get("ORD-1042").status)
        self.assertEqual([], self.store.events)

    def test_fulfilment_started_is_too_late(self) -> None:
        store = InMemoryOrderStore(
            [Order(order_id="ORD-2042", owner_id="customer-7", status=OrderStatus.FULFILMENT_STARTED)]
        )

        result = OrderCancellationService(store).cancel("ORD-2042", "customer-7", "req-003")

        self.assertEqual(CancellationCode.TOO_LATE, result.code)
        self.assertEqual(OrderStatus.FULFILMENT_STARTED, store.get("ORD-2042").status)
        self.assertEqual([], store.events)

    def test_shipped_is_too_late(self) -> None:
        store = InMemoryOrderStore(
            [Order(order_id="ORD-2043", owner_id="customer-7", status=OrderStatus.SHIPPED)]
        )

        result = OrderCancellationService(store).cancel("ORD-2043", "customer-7", "req-shipped")

        self.assertEqual(CancellationCode.TOO_LATE, result.code)
        self.assertEqual(OrderStatus.SHIPPED, store.get("ORD-2043").status)
        self.assertEqual(1, store.get("ORD-2043").version)
        self.assertEqual([], store.events)

    def test_same_idempotency_key_replays_result_without_second_event(self) -> None:
        first = self.service.cancel("ORD-1042", "customer-7", "req-004")
        replay = self.service.cancel("ORD-1042", "customer-7", "req-004")

        self.assertEqual(first, replay)
        self.assertEqual(1, len(self.store.events))
        self.assertEqual(2, self.store.get("ORD-1042").version)

    def test_reusing_key_for_different_request_is_a_conflict(self) -> None:
        self.service.cancel("ORD-1042", "customer-7", "req-005")

        with self.assertRaises(IdempotencyConflict):
            self.service.cancel("ORD-1042", "customer-9", "req-005")

    def test_new_key_after_cancellation_reports_existing_outcome(self) -> None:
        self.service.cancel("ORD-1042", "customer-7", "req-006")

        result = self.service.cancel("ORD-1042", "customer-7", "req-007")

        self.assertEqual(CancellationCode.ALREADY_CANCELLED, result.code)
        self.assertEqual(1, len(self.store.events))

    def test_already_cancelled_precedes_stale_version_for_new_intent(self) -> None:
        self.service.cancel("ORD-1042", "customer-7", "req-006-first", expected_version=1)

        result = self.service.cancel(
            "ORD-1042", "customer-7", "req-006-later", expected_version=1
        )

        self.assertEqual(CancellationCode.ALREADY_CANCELLED, result.code)
        self.assertEqual(OrderStatus.CANCELLED, result.order_status)
        self.assertEqual(2, result.order_version)
        self.assertEqual(1, len(self.store.events))

    def test_unknown_order_is_not_found(self) -> None:
        result = self.service.cancel("ORD-missing", "customer-7", "req-008")

        self.assertEqual(CancellationCode.NOT_FOUND, result.code)
        self.assertEqual("ORD-missing", result.order_id)
        self.assertEqual([], self.store.events)

    def test_stale_expected_version_is_rejected(self) -> None:
        result = self.service.cancel("ORD-1042", "customer-7", "req-009", expected_version=99)

        self.assertEqual(CancellationCode.VERSION_CONFLICT, result.code)
        self.assertEqual(OrderStatus.CONFIRMED, self.store.get("ORD-1042").status)
        self.assertEqual([], self.store.events)

    def test_concurrent_requests_emit_exactly_one_cancellation_event(self) -> None:
        workers = 12
        barrier = threading.Barrier(workers)

        def attempt(index: int):
            barrier.wait()
            return self.service.cancel("ORD-1042", "customer-7", f"race-{index:02d}")

        with ThreadPoolExecutor(max_workers=workers) as pool:
            results = list(pool.map(attempt, range(workers)))

        codes = [result.code for result in results]
        self.assertEqual(1, codes.count(CancellationCode.CANCELLED))
        self.assertEqual(workers - 1, codes.count(CancellationCode.ALREADY_CANCELLED))
        self.assertEqual(1, len(self.store.events))
        self.assertEqual(2, self.store.get("ORD-1042").version)


if __name__ == "__main__":
    unittest.main()
