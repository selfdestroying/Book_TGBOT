from dataclasses import dataclass

from environs import Env


@dataclass
class DataBaseConfig:
    database: str
    db_host: str
    db_user: str
    db_password: str


@dataclass
class TgBotConfig:
    token: str
    admin_ids: list[int]


@dataclass
class Config:
    tg_bot: TgBotConfig
    db: DataBaseConfig


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBotConfig(token=env('BOT_TOKEN'),
                                     admin_ids=list(map(int, env.list('ADMIN_IDS')))),
                  db=DataBaseConfig(database=env('DATABASE'),
                                    db_host=env('DB_HOST'),
                                    db_user=env('DB_USER'),
                                    db_password=env('DB_PASSWORD')))
