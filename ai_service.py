from openai import AsyncOpenAI
import config

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=config.OPENROUTER_API_KEY,
)

# Модели, которые реально найдены в твоем аккаунте
FREE_MODELS = [
    "nvidia/nemotron-3.5-lightning:free",
    "qwen/qwen3.8-27b:free",
    "liquid/lfm-2.5-2.6b:free",
    "apodex/apodex-1.1-mini:free",
    "dots-studio/dots-3-note-preview:free",
    "thinkingmachines/inkling:free",
]

async def generate_support_reply(user_message: str) -> str:
    """Генерация ответа через рабочие модели OpenRouter"""
    for model_name in FREE_MODELS:
        try:
            response = await client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": config.SYSTEM_PROMPT},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.8,
                max_tokens=300,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Модель {model_name} временно занята: {e}. Переходим к следующей...")
            continue

    return "В данный момент все операторы заняты, пожалуйста, повторите ваш вопрос чуть позже."