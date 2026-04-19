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
| DZEN_OS_BOT_TOKEN | Telegram Bot API | dzen-os bot | @BotFather (@dzen_os_bot) |
| GITHUB_TOKEN | GitHub API (OAuth from gh CLI) | dzen-os bot | gh auth token |
| TELEGRAM_USER_ID | Telegram user ID | dzen-os bot (ALLOWED_USERS) | @userinfobot |
| TELEGRAM_API_ID | Telegram MTProto (Telethon) — read personal account | zenevich-blogs, dzen-os (planned) | my.telegram.org |
| TELEGRAM_API_HASH | Telegram MTProto (Telethon) — read personal account | zenevich-blogs, dzen-os (planned) | my.telegram.org |

## Серверы

| Имя | IP | SSH | Что там |
|-----|----|-----|---------|
| Hetzner (zenevich) | 204.168.142.116 | ssh root@204.168.142.116 | Telegram бот @zenevich_events_bot (zenevich-bot.service), dzen-os-bot (dzen-os-bot.service) |
| Hetzner (voora-n8n) | 46.62.225.46 | ssh root@n8n.voora.live | n8n в Docker, UI: http://n8n.voora.live:5678 |

## SSH ключи

| Файл | Для чего |
|------|----------|
| ~/.ssh/id_ed25519_github | GitHub (оба ноута) |
| ~/.ssh/id_ed25519_gitlab | GitLab (оба ноута) |

## GitHub / GitLab

| Репо | Что | Где |
|------|-----|-----|
| iamdzennn/zenevich-blogs | Контент блогов, скрипты каналов | оба |
| iamdzennn/zenevich-events-bot | Telegram бот для ивентов | оба |
| iamdzennn/dzen-dev-toolkit | Скиллы, MCP, playbooks | оба |
| iamdzennn/dzen-os | Personal OS: knowledge base, decisions, wiki | оба |
| iamdzennn/dzen-tools | Инвойсы | оба |
| iamdzennn/check-site-AI-readiness | ismysite-ai-ready | личный |
| iamdzennn/travel-receipts-bot | Бот для чеков (TG + OpenAI) | личный |
| gitlab: dmitry.zenevich/prompts-testing | Тестирование промтов, скрипты ask_chatgpt/ask_gemini | рабочий |
| gitlab: dmitry.zenevich/openai-billing-bot | OpenAI billing бот | рабочий |
| (local only) trendwatching-agent | Трендвотчинг, нет remote | личный |

## Google Cloud

- GCP проект: `gcp-integration-with-claude` (OAuth для GWS CLI)
- Apify user ID: `jDJYWh5AQA28da2Yy` (free plan, $5 кредитов)

## Как настроить новый ноутбук

1. `git clone git@github.com:iamdzennn/dzen-dev-toolkit.git ~/dev/dzen-dev-toolkit`
2. `cd ~/dev/dzen-dev-toolkit && ./setup.sh`
3. Скопировать `.env.master` с другого ноута в `~/.config/dzen-dev-toolkit/.env.master`
4. Для каждого проекта: `./link-to-project.sh ~/dev/<project>`
5. SSH ключи: скопировать `~/.ssh/id_ed25519_github` и `~/.ssh/id_ed25519_gitlab` с другого ноута
