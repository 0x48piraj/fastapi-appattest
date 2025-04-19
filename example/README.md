# `fastapi_appattest` Example App

This is a minimal FastAPI example that demonstrates how to use the `fastapi_appattest` extension to secure API endpoints using Apple's App Attest.

## Running the Demo

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the app:
   ```bash
   uvicorn main:app --reload
   ```

3. Make a request from your iOS app using the attested session token in the `Authorization` header:
   ```http
   GET /api/public-config
   Authorization: Bearer <session_token>
   ```

If the token is valid, you'll receive a response like:

```json
{
  "device": "A51E7E3C-XXXX-XXXX-XXXX-1234567890AB",
  "config": {
    "feature_flags": ["app_default_config", "dark_mode"],
    "min_supported_version": "1.0.0"
  },
  "note": "✅ Authenticated app client verified via App Attest."
}
```

## Working

The `/api/public-config` endpoint is protected using an **attested session token**, ensuring that:

- The client is a valid iOS app using Apple's App Attest framework.
- A secure challenge–response exchange has occurred between client and server.
- The request carries a verified session token that identifies the device.

Under the hood, this example uses:

- `fastapi_attestation.get_current_session` → Validates the session token on each request.
- Ephemeral server-side challenge storage to prevent replay attacks.
- Public key verification of the App Attest JWT issued by Apple.

Only clients that pass this full flow can access the API. All others are rejected with a `403 Unauthorized`.

For more advanced usage like Redis-backed replay prevention or customizing middleware behavior, refer to the full project documentation.
