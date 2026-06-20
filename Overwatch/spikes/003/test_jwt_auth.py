"""
Spike 003 — Multi-user tokens: JWT/HMAC token-generering och validering.

Testar:
 1. Skapa en token med HMAC SHA256 (HS256)
 2. Validera samma token → OK
 3. Validera manipulerad token (tampered) → reject
 4. Validera utgången token (expired) → reject
"""
import json
import time
import jwt

# ── Konfiguration ──────────────────────────────────────────────
SECRET = "spike-003-super-secret-key-32-bytes-long!!"
ALGORITHM = "HS256"

PAYLOAD = {
    "sub": "user_007",
    "name": "James Bond",
    "role": "agent",
    "iat": int(time.time()),
}

PASS = 0
FAIL = 0


def test(name: str, condition: bool, detail: str = ""):
    global PASS, FAIL
    status = "✅ PASS" if condition else "❌ FAIL"
    if condition:
        PASS += 1
    else:
        FAIL += 1
    msg = f"  {status}  | {name}"
    if detail:
        msg += f" — {detail}"
    print(msg)


# ── 1. Skapa token ─────────────────────────────────────────────
print("=" * 64)
print("  Spike 003 — JWT Multi-User Auth Tests")
print("=" * 64)

# Med expiration (giltig 1 timme)
payload_valid = {**PAYLOAD, "exp": int(time.time()) + 3600}
token = jwt.encode(payload_valid, SECRET, algorithm=ALGORITHM)
print(f"\n🔑 Token created ({len(token)} chars): {token[:80]}...")

# ── 2. Validera samma token → OK ───────────────────────────────
print("\n── Test 1: Validera giltig token ──")
try:
    decoded = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
    test("Valid token decodes OK", decoded["sub"] == "user_007", f"sub={decoded['sub']}")
    test("Role preserved", decoded["role"] == "agent", f"role={decoded['role']}")
except Exception as e:
    test("Valid token decodes OK", False, str(e))

# ── 3. Validera manipulerad token → reject ─────────────────────
print("\n── Test 2: Validera manipulerad token (tampered signature) ──")
parts = token.split(".")
tampered_token = parts[0] + "." + parts[1] + ".invalidsignature"
try:
    jwt.decode(tampered_token, SECRET, algorithms=[ALGORITHM])
    test("Tampered token rejected", False, "Did NOT raise — should have!")
except jwt.InvalidSignatureError:
    test("Tampered token rejected", True, "InvalidSignatureError raised")
except jwt.DecodeError:
    test("Tampered token rejected", True, "DecodeError raised (base64 padding/format)")
except Exception as e:
    test("Tampered token rejected", True, f"{type(e).__name__}: {e}")

# ── Alternativ tampering: byt payload helt ─────────────────────
print("\n── Test 3: Validera token med modifierad payload ──")
try:
    # Encoda en annan payload med samma signatur — HMAC fångar det
    fake_payload = jwt.encode({"sub": "hacker", "role": "admin", "exp": int(time.time()) + 3600}, "wrong-secret-that-is-also-32-bytes!!", algorithm=ALGORITHM)
    jwt.decode(fake_payload, SECRET, algorithms=[ALGORITHM])
    test("Wrong-secret token rejected", False, "Did NOT raise — should have!")
except jwt.InvalidSignatureError:
    test("Wrong-secret token rejected", True, "InvalidSignatureError raised")
except Exception as e:
    test("Wrong-secret token rejected", True, f"{type(e).__name__}: {e}")

# ── 4. Validera utgången token → reject ────────────────────────
print("\n── Test 4: Validera utgången token (expired) ──")
payload_expired = {**PAYLOAD, "exp": int(time.time()) - 10}  # 10 sekunder sedan
expired_token = jwt.encode(payload_expired, SECRET, algorithm=ALGORITHM)
try:
    jwt.decode(expired_token, SECRET, algorithms=[ALGORITHM])
    test("Expired token rejected", False, "Did NOT raise — should have!")
except jwt.ExpiredSignatureError:
    test("Expired token rejected", True, "ExpiredSignatureError raised")
except Exception as e:
    test("Expired token rejected", True, f"{type(e).__name__}: {e}")

# ── Sammanfattning ─────────────────────────────────────────────
print("\n" + "=" * 64)
total = PASS + FAIL
print(f"  Result: {PASS}/{total} passed, {FAIL}/{total} failed")
if FAIL == 0:
    print("  Verdict: ✅ ALL TESTS PASSED — JWT multi-user auth works as expected.")
else:
    print("  Verdict: ❌ SOME TESTS FAILED — review above.")
print("=" * 64)
