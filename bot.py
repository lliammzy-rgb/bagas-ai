import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GUILD_ID = os.getenv("GUILD_ID")

if not DISCORD_TOKEN or not GROQ_API_KEY:
    raise RuntimeError("Pastikan DISCORD_TOKEN dan GROQ_API_KEY sudah diisi di file .env")

if GUILD_ID:
    try:
        GUILD_ID = str(int(GUILD_ID))
    except ValueError as exc:
        raise RuntimeError("GUILD_ID harus berisi angka ID server Discord") from exc

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Initialize Discord bot with intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

SYSTEM_PROMPT = (
    "Kamu adalah bot Discord bernama Bagas. Kamu adalah teman mengobrol yang ramah, "
    "asyik, cerdas, dan membantu. Kamu WAJIB merespon menggunakan Bahasa Indonesia "
    "yang natural, santai, dan hindari gaya kaku seperti robot formal. "
    "Gunakan format markdown Discord seperti bold atau bullet points agar pesanmu enak dibaca."
)
MODEL_NAME = "llama-3.3-70b-versatile"


def extract_prompt(message):
    prompt = message.content.strip()

    for mention in message.mentions:
        prompt = prompt.replace(f"<@{mention.id}>", "")
        prompt = prompt.replace(f"<@!{mention.id}>", "")

    return prompt.strip()


def is_liamm_related(prompt: str) -> bool:
    normalized = prompt.lower()
    return "liammzy" in normalized or "liamm major" in normalized or "liamm" in normalized


@bot.event
async def on_ready():
    print(f"=== Bot {bot.user.name} Berhasil Online! ===")
    if GUILD_ID:
        print(f"Mode server eksklusif aktif untuk guild ID: {GUILD_ID}")


@bot.command(name="commands")
async def commands_command(ctx):
    help_text = (
        "**Commands Bagas**\n"
        "• `@Bagas [prompt]` — Tanya apa saja ke Bagas\n"
        "• `!commands` — Lihat daftar command\n"
        "• `!shutdown` — Matikan bot"
    )
    await ctx.send(help_text)


@bot.command(name="shutdown")
@commands.is_owner()
async def shutdown_command(ctx):
    await ctx.send("Bot sedang dimatikan...")
    await bot.close()


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if GUILD_ID and not isinstance(message.channel, discord.DMChannel):
        if not message.guild or str(message.guild.id) != GUILD_ID:
            await bot.process_commands(message)
            return

    is_mentioned = bot.user in message.mentions
    is_dm = isinstance(message.channel, discord.DMChannel)

    if not (is_mentioned or is_dm):
        await bot.process_commands(message)
        return

    user_message = extract_prompt(message)

    if not user_message:
        await message.channel.send("Yoo! Ada yang bisa Bagas bantu? Sebutin aja pertanyaannya.")
        await bot.process_commands(message)
        return

    if is_liamm_related(user_message):
        await message.channel.send("Dia penciptaku tuh")
        await bot.process_commands(message)
        return

    async with message.channel.typing():
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message},
                ],
                model=MODEL_NAME,
                max_tokens=1024,
            )

            response_text = chat_completion.choices[0].message.content

            if len(response_text) > 2000:
                for i in range(0, len(response_text), 2000):
                    await message.channel.send(response_text[i : i + 2000])
            else:
                await message.channel.send(response_text)

        except Exception as exc:
            print(f"Error saat memanggil Groq API: {exc}")
            await message.channel.send(
                "Waduh, otak Bagas lagi kepenuhan nih. Coba lagi beberapa saat lagi ya! 🤖"
            )

    await bot.process_commands(message)


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
