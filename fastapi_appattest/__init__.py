"""
fastapi_appattest by Piyush Raj <hello@piyushraj.org>

FastAPI extension that provides App Attest support.
"""

__version__ = "0.1.0"

from .fastapi_appattest import (
    generate_client_challenge,
    verify_attestation_token,
    issue_attested_session_token,
    validate_challenge,
)

from .middleware import get_current_session
from .middleware import router as appattest_router
from .schema import AttestationRequest
from .config import settings

__all__ = [
    "generate_client_challenge",
    "verify_attestation_token",
    "issue_attested_session_token",
    "validate_challenge",
    "get_current_session",
    "appattest_router",
    "AttestationRequest",
    "settings",
    "__version__",
]
