from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_file_encoding="utf-8")

    OPENROUTER_API_KEY:str
    OPENROUTER_BASE_URL:str
    
    REASONING_TEXT_MODEL:str="openai/gpt-oss-120b"
    SMALL_TEXT_MODEL:str="openai/gpt-oss-20b"
    
    
   
    SQLITE_FILES_PATH:str="sqlite_files"
    
    RESTAURANT_DATABASE:str='AGENTFOOD.db'
    ORDER_TABLES_NAME:str='ORDERS'
    
    
    ORDER_STATUS:dict[int,str]={
        0: "cancelled",
        1: "in progress",
        2: "out for delivery",
        3: "completed",
    }


settings = Settings()