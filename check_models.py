import asyncio
from openai import AsyncOpenAI
import config

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=config.OPENROUTER_API_KEY,
)

async def check():
    try:
        models = await client.models.list()
        # Ищем все модели, у которых в названии есть "free"
        free = [m.id for m in models.data if ":free" in m.id.lower() and "guard" not in m.id.lower()]
        
        print(f"\nВсего моделей в каталоге: {len(models.data)}")
        print(f"Бесплатных найдено: {len(free)}\n")
        for m in free[:10]:
            print(f'"{m}",')
    except Exception as e:
        print(f"Ошибка получения списка: {e}")

if __name__ == "__main__":
    asyncio.run(check())