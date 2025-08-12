from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    app_host: str
    app_port: int
    reload: bool

    database_url: str
    mysql_user: str
    mysql_password: str
    mysql_host: str
    mysql_port: str
    mysql_database: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


settings = Settings()
