
tg = '6386064090:AAHUGPFL8TD6PcaOVYPyftZKQOqJkauLKXg'
folder = 'b1g21r27r6v0oji74ckg'
iam = "t1.9euelZqVipONis2LjZaJyZTOjcaTle3rnpWajZrIx8aXzp2PnZCals6Pnpnl8_doYV5P-e9YXVg2_N3z9ygQXE_571hdWDb8zef1656VmpGPnJDLzJyPjpyalouZl53J7_zF656VmpGPnJDLzJyPjpyalouZl53JveuelZqbk5mXiZuNls3Gk4uRmJ7PibXehpzRnJCSj4qLmtGLmdKckJKPioua0pKai56bnoue0oye.tDMB-mIrbYc6t0xE0j-fleDIWA-Wd0DHL3mCCwOth-IT5wGLx3FaQKUVk1w75Yd0B52wPvY3Y59jLqJqma9pAg"

MAX_PROJECT_TOKENS = 15000
MAX_USERS = 3
MAX_SESSIONS = 4
MAX_TOKENS_IN_SESSION = 1000
MAX_GPT_TOKENS = 125

GPT_MODEL = 'yandexgpt-lite'

SYSTEM_PROMPT = (
"Ты постепенно создаешь сюжет. Если кто-то попросит, уточняй уже развивающийся сюжет. При необходимости, вплетай в сюжет диалоги между персонажами. Для диалогов используй новые строки и тире. Избегай лишних пояснений в начале и продолжай сюжет логично."
)
START_STORY = '\nНапиши начало истории. Не пиши никакой пояснительный текст от себя'
CONTINUE_STORY = '\nПродолжи сюжет в 1-3 предложения и оставь интригу. Не пиши никакой пояснительный текст от себя'
END_STORY = '\nНапиши завершение истории c неожиданной развязкой. Не пиши никакой пояснительный текст от себя'
