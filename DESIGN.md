
# App Attest Flow

**Step 0: Confirm App Attest Availability**

Before initiating any attestation flow, verify that the device and OS support App Attest. The API will return a capability status — if unavailable, you should fall back gracefully or restrict sensitive operations.

![Basic Architecture](https://github.com/user-attachments/assets/438a2154-a566-444d-9ec1-2bf20257a848)

### 1. Server Issues a Challenge

Your backend generates a random, unpredictable byte string (typically 32+ bytes) and delivers it to the client app. This acts as a nonce to prevent replay attacks.

- **Purpose**: Prove the request is fresh and originated from a trusted client.
- **Transport**: Return the challenge via a standard API response (e.g., JSON over HTTPS).
- **Considerations**: Set a short expiry window for the challenge (e.g., 5 minutes) and bind it to device session metadata, if available.

### 2. App Generates a Key Pair

The app invokes the **DeviceCheck App Attest API** to generate a new cryptographic key pair stored securely in the [Secure Enclave](https://support.apple.com/en-au/guide/security/sec59b0b31ff/web).

- **Key ID**: A base64-encoded SHA-256 hash of the public key is returned as a unique identifier.
- **Security Note**: This key never leaves the device; only its identifier and attestations are shared.

![Device Attestation Protocol](https://github.com/user-attachments/assets/4915f21e-dec6-43ab-8a4a-e1f63738dccb)

### 3. Attestation Request

The app constructs a request to Apple’s **App Attest Service**, sending:
- The original challenge (hashed)
- The key ID

Apple returns a blob of **attestation data** — essentially, a signed statement asserting the key originated from a genuine, unmodified Apple device and was securely generated.

### 4. Server Verifies Attestation

The attestation data is sent to your backend, which performs a set of validations:

- Verifies the attestation signature via Apple’s public root certificate chain
- Confirms the challenge matches what was originally sent
- Confirms the key is newly generated and not reused improperly
- Optionally stores the key ID as a trusted identity for the device

> ✅ At this point, your backend has cryptographic proof that the app instance is genuine and running on an untampered Apple device.


### Validating Attestation Statement

The steps to validating the attestation statement are outlined [here](https://web.archive.org/web/20210302101202/https://developer.apple.com/documentation/devicecheck/validating_apps_that_connect_to_your_server).

This represents the bulk of the protocol implementation, there are lots of steps and lots of concepts to understand. Let's try and break it down to make it digestible.

1. Decode the attestation data
2. Verify statement certificates
3. Verify cryptographic nonce
4. Verify key identifier against statement certificate
5. Verify app identifier
6. Verify the signing counter
7. Verify development or production environment
8. Verify key identifier against credential identifier
9. Store attestation data for assertion data verification

![Attestation Object](https://github.com/user-attachments/assets/20bf57a0-638a-400c-be0e-020ea61d6c12)

### 5. Subsequent Requests Use Assertions

For each future request requiring integrity assurance:

- The app uses the previously created key to sign a hash of the request payload (or nonce).
- It includes the **key ID** and the **assertion** (signed hash) in the request headers or body.

## HTTP Authentication / Integration Considerations

To align with HTTP standards and security patterns:

### Use Structured Headers

Define a custom `Authorization` scheme, e.g.:

```
Authorization: Attest key_id="<key_id>", assertion="<base64_assertion>"
```

Or embed in a custom header:

```
X-App-Attest: key_id=<key_id>; assertion=<base64>
```

### Use HTTPS and Enforce TLS 1.2+

Never accept these requests over insecure connections.

### Handle Key Rotation

Devices may need to generate a new key (e.g., if the old one is invalidated). Your backend should support multiple keys per device session and allow trust re-establishment.

### Replay Protection

To prevent replay attacks:
- Bind assertions to a timestamp or nonce
- Include short-lived challenges in high-risk endpoints
- Log and monitor assertion usage patterns

## Gotchas & Things to Watch Out For

Implementing device attestation securely means avoiding subtle mistakes that could weaken the protection. Here's what to watch for:

### Challenge Reuse
- **Challenge tokens are one-time-use** by design.  
- If a challenge is reused, it will be rejected — this protects against replay attacks.
- Clients should always request a fresh challenge before initiating attestation.

> ✅ *Tip: Cache the challenge only long enough to complete the attestation handshake (e.g., 5 minutes).*

### Device ID Consistency
- The `device_id` must remain **stable and unique** for each iOS device.
- If you're using something like `identifierForVendor` (IDFV), make sure it's consistent across app sessions.

> ⚠️ If your `device_id` changes, the challenge/session verification will fail.

### JWT Secrets
- JWTs are signed with a secret (`JWT_SECRET`) — **keep this safe**.
- If compromised, attackers could forge session tokens.

> 🔄 Rotate secrets periodically and invalidate old tokens if a breach is suspected.

### Session Expiry
- JWT session tokens **expire after a set duration**.
- Clients must be ready to re-attest if the session is no longer valid.

> 💡 You can optionally implement a refresh mechanism or ask clients to repeat the attestation.

### Attestation Token Verification
- Apple’s attestation tokens are signed with **ES256**, not HS256 — use the correct algorithm.
- You **must verify** against Apple’s **official public key endpoint**.

> ⚠️ Avoid hardcoding public keys. Use the built-in key fetcher, which caches them efficiently.

### Clean Up Challenge Store
- If you're using the in-memory challenge store, expired challenges should be cleaned up regularly to avoid memory bloat.
- In production, consider switching to Redis with TTL support for automatic expiry.

### CORS & Headers
- Don’t forget to configure CORS if your mobile app and API are on different origins.
- Clients must include the `Authorization: Bearer <token>` header in each secured request.

### Emulator Detection ≠ App Attest
- App Attest ensures the app is **genuine** and **untampered**, but doesn’t directly block emulators.
- Combine with other techniques (e.g., jailbreak detection) if needed.

## References

- [Establishing your app’s integrity | Apple Developer Documentation](https://developer.apple.com/documentation/devicecheck/establishing-your-app-s-integrity)