import os
import typing

from dotenv import load_dotenv

load_dotenv()

TOKEN: typing.Final[str] = os.environ["TOKEN"]
GITHUB_TOKEN: typing.Final[str] = os.environ["GITHUB_TOKEN"]
GITHUB_URL: typing.Final[str] = "https://api.github.com/gists"