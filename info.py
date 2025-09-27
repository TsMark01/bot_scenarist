MAX_PROJECT_TOKENS = 15000
MAX_USERS = 3
MAX_SESSIONS = 4
MAX_TOKENS_IN_SESSION = 1000
MAX_GPT_TOKENS = 125

GPT_MODEL = 'yandexgpt-lite'

SYSTEM_PROMPT = (
    "You gradually create the plot. If someone asks, clarify the ongoing plot. "
    "If necessary, weave dialogues between characters into the plot. "
    "For dialogues, use new lines and dashes. "
    "Avoid unnecessary explanations at the beginning and continue the plot logically."
)
START_STORY = '\nWrite the beginning of the story. Do not write any explanatory text from yourself.'
CONTINUE_STORY = '\nContinue the plot in 1-3 sentences and leave an intrigue. Do not write any explanatory text from yourself.'
END_STORY = '\nWrite the ending of the story with an unexpected twist. Do not write any explanatory text from yourself.'
