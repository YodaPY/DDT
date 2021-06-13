import typing

import aiohttp

from dtv.config import GITHUB_TOKEN

async def create_gist(content: str) -> typing.Dict[str, typing.Any]:
    URL = "https://api.github.com/gists"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }
    json = {
        "public": True,
        "files": {
            "tokens.txt": {
                "content": content
            }
        }
    }

    async with aiohttp.request(
        "POST",
        URL,
        headers=headers,
        json=json
    ) as _:
        pass