from typing import List

from pydantic import Field,BaseModel
from pydantic_settings import BaseSettings

# Define every function's LLM settings
TASK_MODEL_MAPPING = {
    "write_story_and_characters_intro": {
        "model": "gpt-4",
        "max_tokens": 7000,
    },
    "write_shots_tldr": {
        "model": "gpt-3.5-turbo-16k",
        "max_tokens": 4096 * 2,
    },
    "write_shots_detail": {
        "model": "gpt-4",
        "max_tokens": 5000,
    },
    "design_scene": {
        "model": "gpt-4",
        "max_tokens": 5000,
    },
    "select_voice": {
        "model": "gpt-3.5-turbo-16k",
        "max_tokens": 2048,
    },
    "design_voice": {
        "model": "gpt-3.5-turbo-16k",
        "max_tokens": 9000,
    },
    "design_shots_music": {
        "model": "gpt-4",
        "max_tokens": 5000,
    },
}

APP_LOGO="""\


  .-')     .-') _                  _  .-')                        .-')     .-') _                  _ .-') _                          
 ( OO ).  (  OO) )                ( \( -O )                      ( OO ).  (  OO) )                ( (  OO) )                         
(_)---\_) /     '._   .-'),-----.  ,------.    ,--.   ,--.      (_)---\_) /     '._   ,--. ,--.    \     .'_    ,-.-')   .-'),-----. 
/    _ |  |'--...__) ( OO'  .-.  ' |   /`. '    \  `.'  /       /    _ |  |'--...__)  |  | |  |    ,`'--..._)   |  |OO) ( OO'  .-.  '
\  :` `.  '--.  .--' /   |  | |  | |  /  | |  .-')     /        \  :` `.  '--.  .--'  |  | | .-')  |  |  \  '   |  |  \ /   |  | |  |
 '..`''.)    |  |    \_) |  |\|  | |  |_.' | (OO  \   /          '..`''.)    |  |     |  |_|( OO ) |  |   ' |   |  |(_/ \_) |  |\|  |
.-._)   \    |  |      \ |  | |  | |  .  '.'  |   /  /\_        .-._)   \    |  |     |  | | `-' / |  |   / :  ,|  |_.'   \ |  | |  |
\       /    |  |       `'  '-'  ' |  |\  \   `-./  /.__)       \       /    |  |    ('  '-'(_.-'  |  '--'  / (_|  |       `'  '-'  '
 `-----'     `--'         `-----'  `--' '--'    `--'             `-----'     `--'      `-----'     `-------'    `--'         `-----' 

"""

class ClI_CONFIG(BaseModel):
    APP_LOGO: str = APP_LOGO


class Base(BaseSettings):
    OPENAI_API_KEY: str = Field("", env="OPENAI_API_KEY")
    AZURE_SPEECH_KEY: str = Field("", env="AZURE_SPEECH_KEY")
    AZURE_SPEECH_REGION: str = Field("", env="AZURE_SPEECH_REGION")
    REPLICATE_API_TOKEN: str = Field("", env="REPLICATE_API_TOKEN")
    STABILITY_KEY: str = Field("", env="STABILITY_KEY")

    WORKSPACE:str=Field("./workspace", env="WORKSPACE")
    ClI_CONFIG: ClI_CONFIG=ClI_CONFIG()

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


app_settings = Base()
