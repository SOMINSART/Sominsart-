from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    app_name: str = 'DEPOZIO'
    database_url: str = 'sqlite+aiosqlite:///./depozio.db'
    redis_url: str = 'redis://localhost:6379/0'
    jwt_secret: str = 'change-me-secret'
    jwt_refresh_secret: str = 'change-me-refresh-secret'
    jwt_exp_minutes: int = 30
    jwt_refresh_days: int = 7
    aes_key_b64: str = 'MDEyMzQ1Njc4OWFiY2RlZjAxMjM0NTY3ODlhYmNkZWY='
    stripe_secret_key: str = 'sk_test_replace'
    stripe_price_id: str = 'price_replace'
    frontend_url: str = 'http://localhost:5173'
    google_client_id: str = 'google-client-id'
    inpi_endpoint: str = 'https://api.inpi.example/search'
    euipo_endpoint: str = 'https://api.euipo.example/search'
    wipo_endpoint: str = 'https://api.wipo.example/search'


settings = Settings()
