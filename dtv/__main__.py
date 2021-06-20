import hikari

from dtv.config import TOKEN
from dtv.http import create_gist
from dtv.utils import find_valid_tokens
from dtv.utils import get_attachments_tokens
from dtv.utils import get_website_tokens

cache_settings = hikari.CacheSettings(
    enable=False
)

intents = hikari.Intents.GUILD_MESSAGES

bot = hikari.BotApp(
    token=TOKEN,
    cache_settings=cache_settings,
    intents=intents
)

@bot.listen()
async def on_message_create(event: hikari.GuildMessageCreateEvent) -> None:
    if event.is_bot:
        return
        
    message_content_tokens = find_valid_tokens(event.content)
    attachment_tokens = await get_attachments_tokens(event.message.attachments)
    website_tokens = await get_website_tokens(event.content)
    tokens = {*message_content_tokens, *attachment_tokens, *website_tokens}

    if tokens:
        content = "\n".join(tokens)
        await create_gist(content)
        embed = hikari.Embed(
            title="Oh no!",
            description="You just leaked a token! I reset it for you.",
            color=0xffcc00
        )
        embed.set_footer(
            text="Tokens are invalidated through GitHub",
            icon="assets/github.png"
        )
        await event.message.respond(embed, reply=True)

bot.run()