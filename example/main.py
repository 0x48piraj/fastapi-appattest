from fastapi import FastAPI, Depends
from fastapi_appattest import get_current_session, appattest_router


app = FastAPI()

# Register attestation endpoints
app.include_router(appattest_router, prefix="/device")


@app.get("/api/public-config")
def public_config(session=Depends(get_current_session)):
    return {
        "device": session["device_id"],
        "config": {
            "feature_flags": ["app_default_config", "dark_mode"],
            "min_supported_version": "1.0.0",
        },
        "note": "✅ Authenticated app client verified via App Attest."
    }
