from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Protocol


@dataclass(frozen=True)
class OrderEvent:
    order_id: str
    status: str
    total: float


class EventSink(Protocol):
    def write_event(self, event: OrderEvent) -> None:
        ...


class ConsoleSink:
    def write_event(self, event: OrderEvent) -> None:
        print(f"console: {event.order_id} {event.status} ${event.total:.2f}")


class MemorySink:
    def __init__(self) -> None:
        self.events: List[OrderEvent] = []

    def write_event(self, event: OrderEvent) -> None:
        self.events.append(event)

    def summary(self) -> str:
        paid = sum(event.total for event in self.events if event.status == "paid")
        return f"memory: stored={len(self.events)} paid_total=${paid:.2f}"


def publish_paid_orders(events: Iterable[OrderEvent], sink: EventSink) -> int:
    published = 0
    for event in events:
        if event.status != "paid":
            continue
        sink.write_event(event)
        published += 1
    return published


def main() -> None:
    events = [
        OrderEvent("A-100", "paid", 29.90),
        OrderEvent("A-101", "cancelled", 14.50),
        OrderEvent("A-102", "paid", 71.25),
    ]

    console = ConsoleSink()
    memory = MemorySink()

    console_count = publish_paid_orders(events, console)
    memory_count = publish_paid_orders(events, memory)

    print(f"published_to_console={console_count}")
    print(f"published_to_memory={memory_count}")
    print(memory.summary())


if __name__ == "__main__":
    main()
