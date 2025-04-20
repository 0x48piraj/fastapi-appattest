# FastAPI-Appattest

As mobile applications increasingly rely on unauthenticated APIs for performance and user experience, the absence of robust security controls creates a soft target for exploitation. Left unprotected, these endpoints can expose sensitive logic and open vectors for abuse—ranging from data leakage to unauthorized system interaction.

Mobile apps commonly rely on unauthenticated APIs for tasks such as retrieving configuration data or serving publicly accessible content. While this approach reduces friction, it also introduces risk. Without proper safeguards, these endpoints become easy targets for misuse. Malicious actors can:

- Generate synthetic traffic to manipulate and/or disrupt backend operations. 
- Interact with the APIs from compromised environments—such as emulators, rooted devices, or unauthorized clients—bypassing intended usage boundaries.

**FastAPI-Appattest** is a lightweight FastAPI extension that integrates Apple’s App Attest, offering a secure and developer-friendly way to validate device integrity. Designed for minimal overhead and seamless integration, it adds a critical layer of trust to unauthenticated mobile API traffic—without complicating your stack.

<p align="center">
  <img src="https://docs-assets.developer.apple.com/published/4af6b5e0a27bb7176fa92a73104de5e3/establishing_your_app_s_integrity-1~dark@2x.png" alt="Establishing App Integrity" />
</p>

## Features

- 🔐 **Apple App Attest Integration**  
  Securely validates requests from your genuine iOS app using Apple’s App Attest — no more trusting just User-Agents or public tokens.

- 🧾 **Challenge–Response Flow**  
  Implements a secure challenge mechanism to prevent replay attacks and validate device ownership with a time-limited, per-device challenge.

- ✅ **Signed Session Tokens**  
  Issues short-lived JWT tokens to attested clients — tokens are cryptographically signed and tamper-proof.

- ⏱️ **One-Time Validation per Device/Session**  
  Attestation is performed only once per session or device; future requests just use the lightweight session token.

- 🚫 **Tamper-Proof Assurance**  
  Clients cannot spoof or forge tokens — the signature must match Apple's public key and challenge.

- 🔄 **Session Expiry & Rotation**  
  Expiring tokens reduces the attack surface, and tokens can be revoked or rotated as needed.

- 🧱 **Lightweight & Modular**  
  Drop-in FastAPI extension — no heavy frameworks, easily integrates into any app structure.

- 🧠 **In-Memory Store with Redis-Ready Design**  
  Uses an in-memory challenge store by default, with a clear path to swap in Redis for production use.

- 🌐 **Built-in Public Key Caching**  
  Efficiently fetches and caches Apple’s public keys to validate tokens without excessive network requests.

- 🧪 **Example Project Included**  
  Comes with a plug-and-play example showcasing the full attestation flow from client to protected route.

- 📦 **Configurable & Developer Friendly**  
  Environment-based configuration with sensible defaults using `pydantic-settings`.

## Installation

```bash
# Install via PyPI
pip install fastapi-appattest
```

## 🔬 Demo

An end-to-end working example is included under [`example/`](https://github.com/0x48piraj/fastapi-appattest/tree/master/example) showing:

- How to generate a challenge
- How to verify the attestation token
- How to issue + consume signed session tokens

👉 **[See example/README.md for details →](https://github.com/0x48piraj/fastapi-appattest/blob/master/example/README.md)**

## Development & Testing

Clone the repo and install dependencies with [Poetry](https://python-poetry.org):

```bash
git clone https://github.com/0x48piraj/fastapi-appattest.git
cd fastapi-appattest
poetry install
```

Run the example server:

```bash
cd example/
poetry run uvicorn main:app --reload
```

## Usage

After installing `fastapi-appattest`, you can secure your unauthenticated mobile API endpoints in just a few steps.

### 1. Import and register the attestation router

```python
from fastapi import FastAPI, Depends
from fastapi_appattest import get_current_session, appattest_router

app = FastAPI()

# Mount attestation endpoints at `/device/*`
app.include_router(appattest_router, prefix="/device")
```

This automatically sets up:
- `GET /device/challenge?device_id=...` – generate a challenge
- `POST /device/attest` – verify the token and issue a session token

---

### 2. Protect routes using attested session

Secure any endpoint by requiring a valid attested session token:

```python
@app.get("/api/config")
def get_config(session=Depends(get_current_session)):
    return {
        "device": session["device_id"],
        "config": {
            "feature_flags": ["app_default_config", "dark_mode"],
            "min_supported_version": "1.0.0",
        },
    }
```

If the client does not present a valid token:
- Request is **rejected**
- No extra code needed — validation is handled by `get_current_session`

### 3. Configure via environment variables (.env)

```env
APPLE_PUBLIC_KEYS_URL=https://apple-public-keys-url
APP_BUNDLE_ID=com.your.app.bundleid
CHALLENGE_EXPIRY_SECONDS=300
JWT_SECRET=your-secret-signing-key
JWT_EXPIRY_SECONDS=1800
```

Or set them directly via `pydantic-settings`.

### Complete Client Flow (in brief)

1. **Client requests a challenge:**

   `GET /device/challenge?device_id=...`

2. **App performs attestation on-device using the challenge**

3. **App sends the attestation payload to the server:**

   `POST /device/attest` with:

   ```json
   {
     "token": "<apple_signed_attestation_token>",
     "challenge": "<challenge_from_step_1>",
     "device_id": "<unique_device_id>"
   }
   ```

4. **Server verifies and returns a `session_token`**

5. **Client includes this token in future requests:**

   ```http
   Authorization: Bearer <session_token>
   ```

## Show your support

Star (⭐) the repository and consider following me on [GitHub](https://github.com/0x48piraj) if this project saved you time or taught you something.

## Roadmap

- [ ] Add IP address / user-agent binding to session tokens
- [ ] Store active tokens in Redis with revocation support
- [ ] Use short-lived JWTs + refresh token flow
- [ ] Log suspicious token re-use or mismatched device claims
- [ ] Integrate Google's Play Integrity API (???)