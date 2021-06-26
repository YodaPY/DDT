import pytest

from dtv.utils import find_valid_tokens
from dtv.utils import read_stream

async def stream_mock():
    chunks = [[1, 2, 3], [4, 5, 6]]
    for chunk in chunks:
        yield chunk

@pytest.mark.asyncio
async def test_read_stream():
    stream = stream_mock()
    bytes_ = await read_stream(stream)
    assert b"\x01\x02\x03\x04\x05\x06" == bytes_
    
    stream = stream_mock()
    bytes_ = await read_stream(stream, 1)
    assert b"\x01\x02\x03" == bytes_

def test_find_valid_tokens():
    token = "NzAwMDA5MzE2NTA5NTQ4NTk0.Xpcseg.6-GZwDQqWP_7c8lxKglIVuVBqsE"
    text = f"Look! {token}, a token!"
    valid_tokens = find_valid_tokens(text)
    assert [token] == list(valid_tokens)