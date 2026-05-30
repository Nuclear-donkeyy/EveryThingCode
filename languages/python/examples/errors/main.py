def load_name(ok: bool) -> str:
    if not ok:
        raise FileNotFoundError("config missing")
    return "learner"

try:
    print(load_name(False))
except FileNotFoundError as exc:
    print(f"recover: {exc}")
