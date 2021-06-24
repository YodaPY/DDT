from dtv.utils import find_valid_tokens

def test_find_valid_tokens():
    token = "NzAwMDA5MzE2NTA5NTQ4NTk0.Xpcseg.6-GZwDQqWP_7c8lxKglIVuVBqsE"
    text = f"Look! {token}, a token!"
    valid_tokens = find_valid_tokens(text)
    assert [token] == list(valid_tokens)