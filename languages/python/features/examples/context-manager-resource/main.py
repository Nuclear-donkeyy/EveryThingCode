from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Iterable, Mapping


class AuditLog:
    def __init__(self, path: Path) -> None:
        self.path = path
        self._handle = None

    def __enter__(self) -> "AuditLog":
        self._handle = self.path.open("w", encoding="utf-8")
        self.record("audit log opened")
        return self

    def __exit__(self, exc_type, exc, traceback) -> bool:
        if self._handle is not None:
            if exc is not None:
                self.record(f"leaving with error: {exc}")
            self.record("audit log closed")
            self._handle.close()
        return False

    def record(self, message: str) -> None:
        if self._handle is None or self._handle.closed:
            raise RuntimeError("audit log is not open")
        self._handle.write(message + "\n")


def process_orders(rows: Iterable[Mapping[str, object]], log: AuditLog) -> int:
    accepted = 0
    for row in rows:
        try:
            order_id = str(row["id"])
            quantity = int(row["quantity"])
            if quantity <= 0:
                raise ValueError("quantity must be positive")
        except KeyError as error:
            log.record(f"skip row with missing field: {error}")
        except (TypeError, ValueError) as error:
            log.record(f"skip invalid row {row!r}: {error}")
        else:
            accepted += 1
            log.record(f"accept order {order_id} quantity={quantity}")
    return accepted


def main() -> None:
    rows = [
        {"id": "A-100", "quantity": "3"},
        {"id": "A-101", "quantity": 0},
        {"id": "A-102"},
        {"id": "A-103", "quantity": "2"},
    ]

    with tempfile.TemporaryDirectory() as temp_dir:
        log_path = Path(temp_dir) / "orders.log"
        with AuditLog(log_path) as log:
            accepted = process_orders(rows, log)

        print(f"accepted={accepted}")
        print(log_path.read_text(encoding="utf-8").strip())


if __name__ == "__main__":
    main()
