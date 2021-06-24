import base64
import binascii
import io
import re
import typing

import hikari
import magic

from dtv.http import get_html_from

TOKEN_REGEX: re.Pattern = re.compile(r"[\w-]{23,28}\.[\w-]{6,7}\.[\w-]{27}")
URL_REGEX: re.Pattern = re.compile(r"https?:\/\/(?:www\.)?[a-z0-9-]{2,62}\.(?:[a-z]\.?)+[^\s]*")

def find_valid_tokens(s: str) -> typing.Generator[str, None, None]:
    tokens = TOKEN_REGEX.findall(s)
    for token in tokens:
        user_id, *_ = token.split(".")
        try:
            user_id = int(base64.b64decode(user_id, validate=True))
        except (ValueError, binascii.Error):
            continue
        
        yield token

async def read_stream(stream: hikari.files.WebReader, max_bytes: typing.Optional[int]=None) -> bytes:
    c = 0
    buff = bytearray()
    async for chunk in stream:
        if c == max_bytes:
            break
            
        buff.extend(chunk)
        c += 1

    return bytes(buff)

async def get_attachments_tokens(attachments: typing.Iterable[hikari.Attachment]) -> typing.List[str]:
    attachments_tokens = []
    for attachment in attachments:
        async with attachment.stream() as stream:
            buff = await read_stream(stream, 2048)
            mimetype = magic.from_buffer(buff, mime=True)
            if not mimetype.startswith("text"):
                continue

            data = buff + await read_stream(stream)

        text = data.decode()
        tokens = find_valid_tokens(text)
        attachments_tokens.extend(tokens)

    return attachments_tokens

async def get_website_tokens(s: str) -> typing.List[str]:
    urls = URL_REGEX.findall(s)
    website_tokens = []
    for url in urls:
        html = await get_html_from(url)
        tokens = find_valid_tokens(html)
        website_tokens.extend(tokens)

    return website_tokens
