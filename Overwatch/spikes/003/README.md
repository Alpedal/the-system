# Spike 003 — Multi-user tokens (JWT/HMAC Auth)

**Test:** JWT-token-generering och validering för multi-user auth med HMAC SHA256 (HS256).

---

## Testfall

### 1. Skapa och validera giltig token
- **Given** en hemlig HMAC-nyckel och en payload med `sub`, `name`, `role`, `iat`, `exp`
- **When** en JWT skapas med `jwt.encode(payload, secret, algorithm="HS256")`
- **Then** ska samma token kunna avkodas med `jwt.decode(token, secret, algorithms=["HS256"])`
- **And** claims (`sub`, `role`) ska vara oförändrade

### 2. Manipulerad signatur → reject
- **Given** en giltig JWT
- **When** signature-delen byts ut mot ogiltig data
- **Then** ska `jwt.decode` kasta `InvalidSignatureError`

### 3. Token signerad med annan nyckel → reject
- **Given** en payload signerad med en annan hemlighet
- **When** den avkodas med den ursprungliga nyckeln
- **Then** ska `jwt.decode` kasta `InvalidSignatureError`

### 4. Utgången token → reject
- **Given** en token där `exp` ligger 10 sekunder i det förflutna
- **When** den avkodas
- **Then** ska `jwt.decode` kasta `ExpiredSignatureError`

---

## Verdict

| Scenario | Status |
|---|---|
| Skapa + validera giltig token | ✅ PASS |
| Manipulerad signatur | ✅ PASS |
| Token med fel nyckel | ✅ PASS |
| Utgången token | ✅ PASS |

**Resultat: 5/5 tester passerade.**

JWT/HMAC auth med HS256 fungerar som förväntat för multi-user-scenarier. Token kan skapas med användarspecifika claims (`sub`, `role`), valideras korrekt, och ogiltiga/manipulerade/utgångna tokens avvisas med rättundantag.

---

## Körning

```bash
python Overwatch/spikes/003/test_jwt_auth.py
```

Implementationen använder [PyJWT](https://github.com/jpadilla/pyjwt) v2.13.0.
