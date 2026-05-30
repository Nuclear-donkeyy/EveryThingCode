from __future__ import annotations

import asyncio
import time
from typing import Dict, Iterable, Tuple


Probe = Tuple[str, float, bool]
Reading = Dict[str, object]


async def read_probe(name: str, delay: float, healthy: bool) -> Reading:
    await asyncio.sleep(delay)
    if not healthy:
        raise TimeoutError(f"{name} did not respond")
    return {"name": name, "ok": True, "value": round(20 + delay * 10, 1)}


async def safe_read_probe(probe: Probe) -> Reading:
    name, delay, healthy = probe
    try:
        return await read_probe(name, delay, healthy)
    except TimeoutError as error:
        return {"name": name, "ok": False, "error": str(error)}


async def collect_with_task_group(probes: Iterable[Probe]) -> list[Reading]:
    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(safe_read_probe(probe)) for probe in probes]
    return [task.result() for task in tasks]


async def collect_with_gather(probes: Iterable[Probe]) -> list[Reading]:
    tasks = [safe_read_probe(probe) for probe in probes]
    return await asyncio.gather(*tasks)


async def main_async() -> None:
    probes = [
        ("north", 0.30, True),
        ("east", 0.10, False),
        ("west", 0.20, True),
    ]

    started = time.perf_counter()
    if hasattr(asyncio, "TaskGroup"):
        mode = "TaskGroup"
        readings = await collect_with_task_group(probes)
    else:
        mode = "gather compatibility"
        readings = await collect_with_gather(probes)
    elapsed = time.perf_counter() - started

    print(f"mode={mode} elapsed={elapsed:.2f}s")
    for reading in readings:
        if reading["ok"]:
            print(f"- {reading['name']}: value={reading['value']}")
        else:
            print(f"- {reading['name']}: error={reading['error']}")


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
