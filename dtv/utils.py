import base64
import binascii
import io
import re
import typing

import hikari

TOKEN_REGEX: re.Pattern = re.compile(r"[\w-]{23,28}\.[\w-]{6,7}\.[\w-]{27}")

def find_valid_tokens(s: str, /) -> typing.Generator[str, None, None]:
    tokens = TOKEN_REGEX.findall(s)
    for token in tokens:
        user_id, *_ = token.split(".")
        try:
            user_id = int(base64.b64decode(user_id, validate=True))
        except (ValueError, binascii.Error):
            continue
        
        yield token

async def get_attachments_tokens(attachments: typing.Iterable[hikari.Attachment]) -> typing.List[str]:
    attachments_tokens = []
    for attachment in attachments:
        data = await attachment.read() 
        text = data.decode("utf-8")
        tokens = find_valid_tokens(text)
        attachments_tokens.extend(tokens)

    return attachments_tokens