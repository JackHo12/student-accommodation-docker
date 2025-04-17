This is an optimization for the Prophet-Barnes/Accommodation-Direct-Monitor project. The main change is deploying the scripts to run on Docker, reducing the hassle of environment configuration.This tutorial does not cover how to get telegram bot id and telegram chat it.

***Be sure you have installed Docker.***

***Be sure to add the .env file before running it.***

.env:
```dotenv
TELEGRAM_BOT_TOKEN=REPLAEC WITH YOUR TELEGRAM BOT TOKEN
TELEGRAM_CHAT_ID=REPLACE WITH YOUR TELEGRAM CHAT ID
CHECK_URL=https://www.studentbostader.se/en/find-apartments/search-apartments
```
run:
```bash
docker-compose up -d

```
