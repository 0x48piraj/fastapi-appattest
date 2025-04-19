
from fastapi import APIRouter, HTTPException
from fastapi_appattest import (
    generate_client_challenge,
    verify_attestation_token,
    issue_attested_session_token,
    validate_challenge
)
from .schema import AttestationRequest


router = APIRouter()


@router.get("/challenge")
def get_challenge(device_id: str):
    if not device_id:
        raise HTTPException(status_code=400, detail="Missing device_id")
    return {"challenge": generate_client_challenge(device_id)}

@router.post("/attest")
async def attest(request: AttestationRequest):
    if not validate_challenge(request.challenge, request.device_id):
        raise HTTPException(status_code=400, detail="Invalid or expired challenge")

    try:
        await verify_attestation_token(request.token, request.device_id, request.challenge)
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))

    token = issue_attested_session_token(request.device_id)
    return {"status": "attestation_success", "session_token": token}
