from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False

    APPLE_PUBLIC_KEYS_URL: str
    APPLE_BUNDLE_ID: str
    CHALLENGE_EXPIRY_SECONDS: int
    JWT_SECRET: str
    JWT_EXPIRY_SECONDS: int

    class Config:
        env_file = ".env"

settings = Settings()
