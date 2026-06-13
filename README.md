# Bagas AI Discord Bot

Bot Discord AI sederhana yang dibangun dengan Python, discord.py, dan Groq. Bot ini bisa merespons pesan dari mention, DM, dan command sederhana di server Discord.

## Fitur

- Merespons saat dipanggil dengan mention seperti @Bagas prompt
- Bisa menerima pesan lewat DM
- Mendukung command sederhana:
  - !commands
  - !shutdown
- Menangani error API dengan pesan yang ramah
- Bisa dibatasi hanya aktif di satu server lewat GUILD_ID
- Menyediakan jawaban khusus untuk topik terkait liammzy atau liamm major

## Teknologi yang Dipakai

- Python 3.10+
- discord.py
- groq
- python-dotenv

## Struktur Project

- bot.py: file utama bot
- requirements.txt: daftar dependency
- .env: menyimpan token dan API key
- Procfile: konfigurasi start command untuk hosting
- runtime.txt: versi Python untuk hosting

## Persiapan

1. Clone repository ini
2. Buat file .env dan isi variabel berikut:
   - DISCORD_TOKEN
   - GROQ_API_KEY
   - GUILD_ID (opsional)
3. Install dependency:
   - pip install -r requirements.txt
4. Jalankan bot:
   - python bot.py

## Contoh Command

- @Bagas halo
- @Bagas jelaskan Python
- !commands
- !shutdown

## Deploy ke Hosting

Project ini juga sudah disiapkan untuk hosting seperti Render atau Railway dengan file:

- Procfile
- runtime.txt

## Catatan

Pastikan bot Discord kamu sudah memiliki izin yang cukup di server, serta Message Content Intent aktif di Developer Portal Discord.
`
