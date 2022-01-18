import typing

import pytest

from dtv.utils import find_valid_tokens
from dtv.utils import get_attachments_tokens
from dtv.utils import get_website_tokens
from dtv.utils import read_stream

TOKENS: typing.Final[typing.List[str]] = ["NzAwMDA5MzE2NTA5NTQ4NTk0.Xpcseg.6-GZwDQqWP_7c8lxKglIVuVBqsE"]

async def stream_mock():
    chunks = [[1, 2, 3], [4, 5, 6]]
    for chunk in chunks:
        yield chunk

class AsyncStreamContextManagerMock:
    async def __aenter__(self):
         return stream_mock()
    
    async def __aexit__(self, *args):
        pass

class AttachmentMock:
    def stream(self):
        return AsyncStreamContextManagerMock()

@pytest.mark.asyncio
async def test_get_attachments_token():
    attachments = (AttachmentMock(), )
    assert not await get_attachments_tokens(attachments)

@pytest.mark.asyncio
async def test_read_stream():
    stream = stream_mock()
    bytes_ = await read_stream(stream)
    assert b"\x01\x02\x03\x04\x05\x06" == bytes_
    
    stream = stream_mock()
    bytes_ = await read_stream(stream, 1)
    assert b"\x01\x02\x03" == bytes_

@pytest.mark.asyncio
async def test_get_website_tokens():
    text = "Here is my code: https://pastebin.com/uA14yixJ"
    website_tokens = await get_website_tokens(text)
    assert TOKENS == list(set(website_tokens))

def test_find_valid_tokens():
    token = "NzAwMDA5MzE2NTA5NTQ4NTk0.Xpcseg.6-GZwDQqWP_7c8lxKglIVuVBqsE"
    text = f"Look! {token}, a token!"
    valid_tokens = find_valid_tokens(text)
    assert TOKENS == list(valid_tokens)

