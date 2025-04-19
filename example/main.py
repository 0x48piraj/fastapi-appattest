from fastapi import FastAPI, Depends
from fastapi_appattest import get_current_session


app = FastAPI()


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
