import black
import hikari
import isort

from ddt.config import TOKEN
from ddt.http import create_gist
from ddt.utils import (find_valid_tokens, format_code, get_attachments_tokens, get_website_tokens)

cache_settings = hikari.CacheSettings(components=hikari.CacheComponents())

intents = hikari.Intents.GUILD_MESSAGES | hikari.Intents.ALL_MESSAGE_REACTIONS

bot = hikari.GatewayBot(token=TOKEN, cache_settings=cache_settings, intents=intents)


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
            color=0x5F7EEA,
        )
        embed.set_image("assets/banner.png")
        embed.set_footer(
            text="Tokens are invalidated through GitHub", icon="assets/github.png"
        )
        await event.message.respond(embed, reply=True)


@bot.listen()
async def on_reaction_add(event: hikari.ReactionAddEvent) -> None:
    if event.is_for_emoji("\U0001F504") is True:
        message = await bot.rest.fetch_message(event.channel_id, event.message_id)
        code = format_code(message.content)
        if code is not None:
            await message.respond(code)


bot.run()
