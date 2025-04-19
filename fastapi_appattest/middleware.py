
from fastapi import APIRouter, HTTPException, Depends, Header
from jose import jwt, JWTError
from fastapi_appattest import (
    settings,
    generate_client_challenge,
    verify_attestation_token,
    issue_attested_session_token,
    get_current_session,
    validate_challenge,
    AttestationRequest
)


def get_current_session(authorization: str = Header(...)):
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        if payload.get("type") != "attested_session":
            raise HTTPException(status_code=403, detail="Invalid session type")
        return payload
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid or expired session token")


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
