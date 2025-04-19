from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = True

    apple_public_keys_url: str
    app_bundle_id: str
    challenge_expiry_seconds: int
    jwt_secret: str
    jwt_expiry_seconds: int

    class Config:
        env_file = ".env"

settings = Settings()
