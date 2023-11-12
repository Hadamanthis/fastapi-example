from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_hostname: str
    db_port: str
    db_name: str
    db_username: str
    db_password: str
    
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int

    class Config:
        env_file = '.env'

settings = Settings()