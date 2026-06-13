# Panduan Hosting Bot Bagas

## 1. Siapkan hosting

Pilih hosting yang mendukung Python, misalnya:

- Railway
- Render
- Heroku
- VPS Ubuntu

## 2. Upload project

Upload seluruh isi folder ini ke hosting.

## 3. Set environment variables

Di panel hosting, tambahkan variabel:

- DISCORD_TOKEN
- GROQ_API_KEY
- GUILD_ID (opsional)

## 4. Start command

Gunakan:

- python bot.py

Atau jika hosting mendukung Procfile, file Procfile sudah disediakan.

## 5. Jalankan

Setelah deploy, hosting akan menjalankan bot otomatis.
