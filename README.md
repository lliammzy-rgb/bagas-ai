# AI Context: Bagas-AI Architecture (Python + Groq)

Kamu adalah AI Assistant yang bertugas memandu pengembangan Bot Discord bernama **Bagas**. File ini berisi arsitektur sistem, alur kerja (flow) penanganan pesan yang matang, dan instruksi penulisan kode menggunakan **Python**.

---

## 1. Lingkungan Pengembangan (Tech Stack)

- **Bahasa:** Python 3.10+
- **Library Utama:** `discord.py` (v2.0+) & `groq` (Official Python SDK)
- **Manajemen Environment:** `python-dotenv`
- **Model AI:** `llama3-8b-8192` (via Groq Cloud)

---

## 2. Struktur Proyek Terpuji

Pastikan struktur folder di dalam `bagas-AI` mengikuti pola bersih berikut:

````text
bagas-AI/
├── .env                  # Menyimpan rahasia (DISCORD_TOKEN & GROQ_API_KEY)
├── .gitignore            # Mengabaikan .env dan venv/
├── gemini.md             # File instruksi arsitektur ini
├── requirements.txt      # Daftar dependensi library Python
└── bot.py                # File utama eksekusi Bot Discord

---

## 3. Alur Kerja Penanganan Pesan (Production-Ready Message Flow)
Setiap kali mendesain atau memperbarui kode pada bot.py, pastikan alur logika berikut terpenuhi demi menjaga kestabilan bot dan menghindari spam:

A. Pengecekan Awal (Gatekeeping)
Bot wajib mengabaikan pesan yang dikirim oleh dirinya sendiri atau bot lain (message.author.bot).

Bot hanya merespon jika di-mention (<@bot_id>) atau diajak bicara melalui Direct Message (DM).

B. Pembersihan Input (Sanitization)
Teks mention (<@bot_id>) harus dihapus/dibersihkan dari konten pesan sebelum dikirim ke Groq API agar AI tidak bingung.

Pastikan pesan pengguna tidak kosong setelah dibersihkan.

C. Status Indikator (User Experience)
Sebelum menembak API Groq, bot harus memicu status typing (async with message.channel.typing():) agar pengguna tahu AI sedang memproses jawaban.

D. Pembungkusan API & Penanganan Eror (Robust Error Handling)
Bungkus pemanggilan Groq API dalam blok try-except.

Jika terkena Rate Limit (429) atau Timeout, bot harus mengirimkan pesan eror yang ramah di Discord, misalnya: "Waduh, otak Bagas lagi kepenuhan nih. Coba lagi beberapa saat lagi ya!" daripada crash atau diam saja.

E. Batasan Karakter Discord (Splitting Mechanism)
Discord memiliki batas maksimal 2.000 karakter per pesan.

Jika respon dari Groq melebihi 2.000 karakter, kode harus otomatis memotong teks tersebut menjadi beberapa bagian sebelum dikirim.

---

## 4. Pola Kode Dasar (Base Code Blueprint)
Gunakan pola kode di bawah ini sebagai fondasi utama penulisan bot.py:

import os
import discord
from discord.ext import commands
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Initialize Groq Client
groq_client = Groq(api_key=GROQ_API_KEY)

# Initialize Discord Bot with Intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

SYSTEM_PROMPT = (
    "Kamu adalah bot Discord bernama Bagas. Kamu adalah teman mengobrol yang ramah, "
    "asyik, cerdas, dan membantu. Kamu WAJIB merespon menggunakan Bahasa Indonesia yang "
    "natural, santai (bisa gunakan bahasa gaul internet yang sopan), dan hindari gaya kaku "
    "seperti robot formal. Gunakan format markdown Discord seperti bold atau bullet points "
    "agar pesanmu enak dibaca."
)

@bot.event
async def on_ready():
    print(f'=== Bot {bot.user.name} Berhasil Online! ===')

@bot.event
async def on_message(message):
    # 1. Gatekeeping
    if message.author.bot:
        return

    # Periksa apakah bot di-mention atau lewat DM
    is_mentioned = bot.user in message.mentions
    is_dm = isinstance(message.channel, discord.DMChannel)

    if is_mentioned or is_dm:
        # 2. Sanitization
        user_message = message.content.replace(f'<@!{bot.user.id}>', '').replace(f'<@{bot.user.id}>', '').strip()

        if not user_message:
            await message.channel.send("Yoo! Ada yang bisa Bagas bantu? Sebutin aja pertanyaannya.")
            return

        # 3. Trigger Typing Indicator
        async with message.channel.typing():
            try:
                # 4. Call Groq API
                chat_completion = groq_client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_message}
                    ],
                    model="llama3-8b-8192",
                    max_tokens=1024,
                )

                response_text = chat_completion.choices[0].message.content

                # 5. Send Response (Handles Discord 2000 char limit safely for normal use)
                if len(response_text) > 2000:
                    for i in range(0, len(response_text), 2000):
                        await message.channel.send(response_text[i:i+2000])
                else:
                    await message.channel.send(response_text)

            except Exception as e:
                print(f"Error saat memanggil Groq API: {e}")
                await message.channel.send("Aduh bro, otaknya Bagas lagi agak nge-lag nih. Coba tanya lagi bentar ya! 🤖")

    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)

---

5. Instruksi Tugas AI
Jika saya meminta kamu mengembangkan fitur baru (seperti sistem database chat history, sistem commands baru, atau integrasi fitur gambar), kamu harus selalu merujuk pada file ini agar gaya penulisan kode, penanganan error, dan persona Bahasa Indonesia dari bot Bagas tetap konsisten.


---

Sekarang file `gemini.md` kamu sudah siap pakai! Silakan buat juga file `requirements.txt` dan isi dengan teks berikut agar gampang menginstall *library*-nya nanti:

```text
discord.py
groq
python-dotenv
````
