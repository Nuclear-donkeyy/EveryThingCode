from __future__ import annotations

from typing import Iterable, Iterator, Tuple


Reading = Tuple[str, float]


def parse_readings(lines: Iterable[str]) -> Iterator[Reading]:
    for line_number, line in enumerate(lines, start=1):
        name, raw_value = line.strip().split(",", 1)
        value = float(raw_value)
        print(f"parsed line {line_number}")
        yield name, value


def only_warm(readings: Iterable[Reading], threshold: float) -> Iterator[Reading]:
    for name, value in readings:
        if value >= threshold:
            yield name, value


def first_n(readings: Iterable[Reading], count: int) -> Iterator[Reading]:
    iterator = iter(readings)
    remaining = count
    while remaining > 0:
        try:
            reading = next(iterator)
        except StopIteration:
            return
        yield reading
        remaining -= 1


def main() -> None:
    lines = [
        "north,18.5",
        "east,22.1",
        "south,25.4",
        "west,19.9",
    ]

    pipeline = first_n(only_warm(parse_readings(lines), threshold=20.0), count=2)
    print("pipeline created")
    for name, value in pipeline:
        print(f"alert: {name} is warm at {value:.1f}C")


if __name__ == "__main__":
    main()
