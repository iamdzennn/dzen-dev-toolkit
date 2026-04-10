# Credentials Map

Карта всех ключей, токенов и доступов. Сами ключи в `~/.config/dzen-dev-toolkit/.env.master`.

## API ключи

| Ключ | Сервис | Где используется | Где взять новый |
|------|--------|------------------|-----------------|
| OPENAI_API_KEY | OpenAI (GPT-5.4) | ask-chatgpt, aijobhunter, jobshunter | platform.openai.com/api-keys |
| GEMINI_API_KEY | Google Gemini | ask-gemini | aistudio.google.com/apikey |
| ANTHROPIC_API_KEY | Anthropic Claude API | aijobhunter, jobshunter | console.anthropic.com/settings/keys |
| BRIGHT_DATA_API_KEY | Bright Data (scraping) | aijobhunter, jobshunter | brightdata.com/cp/api |
| GOOGLE_PLACES_API_KEY | Google Places | aijobhunter, jobshunter | console.cloud.google.com |
| GOOGLE_SEARCH_API_KEY | Google Custom Search | aijobhunter, jobshunter | console.cloud.google.com |
| GOOGLE_SEARCH_ENGINE_ID | Google CSE | aijobhunter, jobshunter | programmablesearchengine.google.com |
| APIFY_TOKEN | Apify (LinkedIn scraping) | zenevich-blogs (linkedin_reader.py) | console.apify.com/account/integrations |
| TG_BOT_TOKEN | Telegram Bot API | zenevich-blogs (tg_channel_reader.py) | @BotFather |
| LIVEKIT_API_KEY | LiveKit (voice) | vox/voxa-agent | cloud.livekit.io |
| LIVEKIT_API_SECRET | LiveKit (voice) | vox/voxa-agent | cloud.livekit.io |

## Серверы

| Имя | IP | SSH | Что там |
|-----|----|-----|---------|
| Hetzner (zenevich) | 204.168.142.116 | ssh root@204.168.142.116 | Telegram бот @zenevich_events_bot, systemd: zenevich-bot.service |
| Hetzner (voora-n8n) | 46.62.225.46 | ssh root@n8n.voora.live | n8n в Docker, UI: http://n8n.voora.live:5678 |

## SSH ключи

| Файл | Для чего |
|------|----------|
| ~/.ssh/id_ed25519 | Основной ключ (GitHub, серверы) |

## GitHub

| Репо | Что |
|------|-----|
| iamdzennn/zenevich-blogs | Контент блогов, скрипты каналов |
| iamdzennn/zenevich-events-bot | Telegram бот для ивентов |
| iamdzennn/dzen-dev-toolkit | Скиллы, MCP, playbooks |
| iamdzennn/dzen-tools | Инвойсы |

## Google Cloud

- GCP проект: `gcp-integration-with-claude` (OAuth для GWS CLI)
- Apify user ID: `jDJYWh5AQA28da2Yy` (free plan, $5 кредитов)

## Как настроить новый ноутбук

1. `git clone git@github.com:iamdzennn/dzen-dev-toolkit.git ~/dev/dzen-dev-toolkit`
2. Скопировать `.env.master` в `~/.config/dzen-dev-toolkit/.env.master`
3. `cd ~/dev/dzen-dev-toolkit && ./setup.sh`
4. Для каждого проекта: `./link-to-project.sh ~/dev/<project>`
5. SSH ключ: скопировать `~/.ssh/id_ed25519` с другого ноута
