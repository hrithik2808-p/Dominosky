# Domino Sky: Black Box Edition

## 60-second demo
1. Start with `docker compose up --build`.
2. Open `http://localhost:8080`.
3. The console pre-selects BOM and a 09:00–10:30 closure.
4. Press **RUN CASCADE** or Space.
5. Click a flight in the network or Causal X-Ray to inspect its blame receipt.
6. Use the ledger **VERIFY** button. Run `python security_selftest.py` for the security table.

## Architecture
`flight_network.json -> deterministic Python engine -> FastAPI -> static OCC console`

The engine recomputes all state from a canonical fingerprint of dataset hash, disruption, and actions.

## Dataset schema
- `meta`, `airports`, `flights`, `connections`, `crews`, `spare_aircraft`
- Times are integer minutes internally and formatted as HH:MM only at presentation edges.
- The supplied dataset is the only source of airports, flights, crews, seats, and passenger counts.

## Security table
| Threat | Mitigation |
|---|---|
| Prompt injection | Delimited/sandboxed dispatcher payload; strict schema; labels bounded to engine fields |
| Hallucinated numbers | Allowed-number verifier and engine templating |
| Malicious input | Pydantic bounds, integer windows, 64 KB proxy discipline |
| Recovery DoS | 20k node budget and per-IP 30 req/min limit |
| Tampered metrics | Hash-chained ledger and verify endpoint |
| Secret leakage | Server-side environment key; `.env` ignored |
| XSS | Text nodes and strict CSP |
| CORS | Explicit local origin allowlist and CSRF token |
| Supply chain | Pinned Python dependency versions |
| Audit gaps | Structured fingerprinted ledger entries |

## Security self-test
Run:

```powershell
python security_selftest.py
```

The result is printed as a PASS/FAIL table with an ALL GREEN summary.

## Validation
- Pure engine tests cover BOM cascade propagation, deterministic fingerprints, breakdown invariants, stranded passengers, recovery plans, and ledger tampering.
- Engine and API intentionally leave advanced tail exchange and external LLM calls as deliberately limited implementations; the action grammar and bounded recovery are executable in code.
