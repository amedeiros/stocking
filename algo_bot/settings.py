import os
from dataclasses import dataclass


@dataclass
class AlgoBotSettings:
    redis_host: str
    redis_port: int
    db_host: str
    db_name: str
    db_password: str
    db_username: str
    bot_env: str


def _dev_settings() -> AlgoBotSettings:
    return AlgoBotSettings(
        redis_host="redis",
        redis_port=6379,
        db_host="db",
        db_name="algo-bot",
        db_password="root",
        db_username="root",
        bot_env="development",
    )


def _test_settings() -> AlgoBotSettings:
    return _dev_settings()


def get_settings() -> AlgoBotSettings:
    env = os.environ.get("BOT_EMV") or "development"

    if env == "development":
        return _dev_settings()
    elif env == "testing":
        return _test_settings()
