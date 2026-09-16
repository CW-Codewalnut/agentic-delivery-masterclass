#!/usr/bin/env python3
"""Run a disposable semantic mutation against exact-replay idempotency.

The repository is never edited. The script copies the implementation to a
temporary directory, removes the successful prior-result return, and runs one
focused unittest that must fail. Exit 1 is the expected RED result.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "worked-example" / "order_cancellation.py"
ORIGINAL = "                return prior_result\n"
MUTATED = "                # NEGATIVE CONTROL: do not replay prior_result\n"
TEST = '''\
import unittest
from order_cancellation import InMemoryOrderStore, Order, OrderCancellationService, OrderStatus


class ExactReplayNegativeControl(unittest.TestCase):
    def test_exact_retry_returns_original_result(self):
        store = InMemoryOrderStore([
            Order(order_id="ORD-NC-1", owner_id="customer-nc", status=OrderStatus.CONFIRMED)
        ])
        service = OrderCancellationService(store)
        first = service.cancel("ORD-NC-1", "customer-nc", "req-nc")
        replay = service.cancel("ORD-NC-1", "customer-nc", "req-nc")
        self.assertEqual(first, replay)
        self.assertEqual(1, len(store.events))


if __name__ == "__main__":
    unittest.main()
'''


def main() -> int:
    source = SOURCE.read_text()
    if source.count(ORIGINAL) != 1:
        print("Refusing to run: exact replay statement was not found uniquely.", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory() as temporary:
        sandbox = Path(temporary)
        (sandbox / "order_cancellation.py").write_text(source.replace(ORIGINAL, MUTATED))
        (sandbox / "test_negative_control.py").write_text(TEST)
        completed = subprocess.run(
            [sys.executable, "-m", "unittest", "test_negative_control", "-v"],
            cwd=sandbox,
            text=True,
            capture_output=True,
            check=False,
        )

    output = (completed.stdout + completed.stderr).replace(str(sandbox) + "/", "")
    print("Mutation: suppress exact replay return and continue decision processing")
    print(output, end="")
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
