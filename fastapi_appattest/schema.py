from pydantic import BaseModel

class AttestationRequest(BaseModel):
    token: str
    challenge: str
    device_id: str
