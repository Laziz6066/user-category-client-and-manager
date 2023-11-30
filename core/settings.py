from dataclasses import dataclass
import os
from dotenv import load_dotenv


load_dotenv('.env')


@dataclass
class Bots:
    bot_token: str
    admin_id: int


@dataclass
class Settings:
    bots: Bots


def get_settings():
    return Settings(
        bots=Bots(
            bot_token=os.getenv('BOT_TOKEN'),
            admin_id=int(os.getenv("ADMIN_ID"))
        )
    )


settings = get_settings()