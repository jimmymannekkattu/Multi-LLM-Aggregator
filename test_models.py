import g4f
import asyncio

async def test_model(name, model):
    print(f"Testing {name}...")
    try:
        response = await g4f.ChatCompletion.create_async(
            model=model,
            messages=[{"role": "user", "content": "Hello"}],
        )
        print(f"SUCCESS {name}: {response[:50]}...")
    except Exception as e:
        print(f"FAIL {name}: {e}")

async def main():
    await test_model("gpt_4", g4f.models.gpt_4)
    await test_model("gpt_4o", g4f.models.gpt_4o)
    await test_model("llama_3_70b", g4f.models.llama_3_70b)

if __name__ == "__main__":
    asyncio.run(main())
