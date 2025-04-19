# FastAPI-Appattest

As mobile applications increasingly rely on unauthenticated APIs for performance and user experience, the absence of robust security controls creates a soft target for exploitation. Left unprotected, these endpoints can expose sensitive logic and open vectors for abuse—ranging from data leakage to unauthorized system interaction.

Mobile apps commonly rely on unauthenticated APIs for tasks such as retrieving configuration data or serving publicly accessible content. While this approach reduces friction, it also introduces risk. Without proper safeguards, these endpoints become easy targets for misuse. Malicious actors can:

- Generate synthetic traffic to manipulate and/or disrupt backend operations. 
- Interact with the APIs from compromised environments—such as emulators, rooted devices, or unauthorized clients—bypassing intended usage boundaries.

**FastAPI-Appattest** is a lightweight FastAPI extension that integrates Apple’s App Attest, offering a secure and developer-friendly way to validate device integrity. Designed for minimal overhead and seamless integration, it adds a critical layer of trust to unauthenticated mobile API traffic—without complicating your stack.

## Features

✅ Only validate attestation once per device/session

✅ Only accepts requests with valid signed tokens

✅ Tampered clients can't fake the signature

✅ Session expiration limits attack window

✅ Revoke or rotate tokens as needed

## App Attest Flow

**Step 0: Confirm App Attest Availability**

Before initiating any attestation flow, verify that the device and OS support App Attest. The API will return a capability status — if unavailable, you should fall back gracefully or restrict sensitive operations.

<p align="center">
  <img src="https://github.com/user-attachments/assets/457f649d-dcb9-4a38-87b9-a2c752b61ba3" alt="establishing-app-integrity" />
</p>

### 1. Server Issues a Challenge

Your backend generates a random, unpredictable byte string (typically 32+ bytes) and delivers it to the client app. This acts as a nonce to prevent replay attacks.

- **Purpose**: Prove the request is fresh and originated from a trusted client.
- **Transport**: Return the challenge via a standard API response (e.g., JSON over HTTPS).
- **Considerations**: Set a short expiry window for the challenge (e.g., 5 minutes) and bind it to device session metadata, if available.

### 2. App Generates a Key Pair

The app invokes the **DeviceCheck App Attest API** to generate a new cryptographic key pair stored securely in the Secure Enclave.

- **Key ID**: A base64-encoded SHA-256 hash of the public key is returned as a unique identifier.
- **Security Note**: This key never leaves the device; only its identifier and attestations are shared.

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

## Roadmap

- [ ] Add IP address / user-agent binding to session tokens
- [ ] Store active tokens in Redis with revocation support
- [ ] Use short-lived JWTs + refresh token flow
- [ ] Log suspicious token re-use or mismatched device claims
- [ ] Integrate Google's Play Integrity API (???)