# FastAPI-Appattest

<p align="center">
  <img src="https://github.com/user-attachments/assets/457f649d-dcb9-4a38-87b9-a2c752b61ba3" alt="Establishing App Integrity" />
</p>

As mobile applications increasingly rely on unauthenticated APIs for performance and user experience, the absence of robust security controls creates a soft target for exploitation. Left unprotected, these endpoints can expose sensitive logic and open vectors for abuse—ranging from data leakage to unauthorized system interaction.

Mobile apps commonly rely on unauthenticated APIs for tasks such as retrieving configuration data or serving publicly accessible content. While this approach reduces friction, it also introduces risk. Without proper safeguards, these endpoints become easy targets for misuse. Malicious actors can:

- Generate synthetic traffic to manipulate and/or disrupt backend operations. 
- Interact with the APIs from compromised environments—such as emulators, rooted devices, or unauthorized clients—bypassing intended usage boundaries.

**FastAPI-Appattest** is a lightweight FastAPI extension that integrates Apple’s App Attest, offering a secure and developer-friendly way to validate device integrity. Designed for minimal overhead and seamless integration, it adds a critical layer of trust to unauthenticated mobile API traffic—without complicating your stack.

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

## Roadmap

- [ ] Add IP address / user-agent binding to session tokens
- [ ] Store active tokens in Redis with revocation support
- [ ] Use short-lived JWTs + refresh token flow
- [ ] Log suspicious token re-use or mismatched device claims
- [ ] Integrate Google's Play Integrity API (???)