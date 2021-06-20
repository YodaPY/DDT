import typing

import aiohttp

from dtv.config import GITHUB_TOKEN, GITHUB_URL

async def create_gist(content: str) -> None:
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
        GITHUB_URL,
        headers=headers,
        json=json
    ) as _:
        pass

async def get_html_from(url: str) -> str:
    async with aiohttp.request(
        "GET",
        url
    ) as resp:
        data = await resp.read()
    
    return data.decode()