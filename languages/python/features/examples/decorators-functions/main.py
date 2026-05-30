from __future__ import annotations

from functools import wraps
from time import perf_counter
from typing import Any, Callable, Dict, List


AuditEntry = Dict[str, object]
AuditLog = List[AuditEntry]


def audit_step(label: str, audit_log: AuditLog) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorate(function: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            started = perf_counter()
            try:
                result = function(*args, **kwargs)
            except Exception as error:
                audit_log.append({"step": label, "ok": False, "error": str(error)})
                raise
            elapsed_ms = (perf_counter() - started) * 1000
            audit_log.append({"step": label, "ok": True, "elapsed_ms": round(elapsed_ms, 3)})
            return result

        return wrapper

    return decorate


def main() -> None:
    audit_log: AuditLog = []

    @audit_step("parse-price", audit_log)
    def parse_price(raw: str) -> float:
        return float(raw.replace("$", ""))

    @audit_step("apply-tax", audit_log)
    def apply_tax(price: float, rate: float) -> float:
        return round(price * (1 + rate), 2)

    price = parse_price("$12.50")
    total = apply_tax(price, rate=0.08)

    print(f"{parse_price.__name__} -> {price:.2f}")
    print(f"total -> {total:.2f}")
    for entry in audit_log:
        print(entry)


if __name__ == "__main__":
    main()
