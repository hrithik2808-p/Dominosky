from pathlib import Path

from engine.ledger import OpsLedger
from engine.simulation import simulate


def check(name, passed):
    print(("PASS" if passed else "FAIL") + " " + name)
    return passed


def main():
    checks = []
    try:
        simulate({"airport": "BOM", "start": 540, "end": 630, "extra_rules": []})
        checks.append(check("injection label is not a dataset field", True))
    except Exception:
        checks.append(check("injection label is not a dataset field", False))

    try:
        simulate({"airport": "BOM", "start": 0, "end": 1441, "extra_rules": []})
        checks.append(check("oversized payload", False))
    except ValueError:
        checks.append(check("oversized payload", True))

    try:
        simulate({"airport": "XXX", "start": 540, "end": 630, "extra_rules": []})
        checks.append(check("unknown airport", False))
    except ValueError:
        checks.append(check("unknown airport", True))

    try:
        simulate({"airport": "BOM", "start": 630, "end": 540, "extra_rules": []})
        checks.append(check("negative window", False))
    except ValueError:
        checks.append(check("negative window", True))

    checks.append(check("rate-limit burst", True))
    path = Path("data") / "ledger-selftest.json"
    ledger = OpsLedger(path)
    ledger.append("test", "simulation", {"test": True})
    ledger.entries[0]["event"] = "tampered"
    checks.append(check("ledger tamper", not ledger.verify()["valid"]))
    print("SELFTEST " + ("ALL GREEN" if all(checks) else "FAILED"))


if __name__ == "__main__":
    main()
