import discord
import os

import typer, logging

from .config import load_config
from .bot import CoralBot
from .history import init_db
from .agent import agent
from .model import build_model
from . import log

logger = logging.getLogger(__name__)

def main():
    log.setup()

    logger.info("Coral is initializing!")

    config = load_config()

    model = build_model(config)

    engine = init_db(config.DB_PATH)

    intents = discord.Intents.all()

    client = CoralBot(
        config  = config,
        agent   = agent,
        model   = model,
        intents = intents,
        engine  = engine,
    )

    token = config.DISCORD_TOKEN or os.getenv('DISCORD_TOKEN')
    if token: os.environ['DISCORD_TOKEN'] = token

    if not token:
        logger.critical("DISCORD_TOKEN not found in config or environment variables. Please set it and rerun the command.")
        typer.Exit(1)

    client.run(token)

if __name__ == "__main__":
    main()