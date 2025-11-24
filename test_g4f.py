import asyncio
import g4f

async def test_g4f():
    models_to_test = [
        ("default", g4f.models.default),
        ("gpt-4o-mini", g4f.models.gpt_4o_mini),
        ("llama-3-70b", g4f.models.llama_3_70b),
    ]

    for name, model in models_to_test:
        print(f"\nTesting {name}...")
        try:
            response = await g4f.ChatCompletion.create_async(
                model=model,
                messages=[{"role": "user", "content": "Hello"}],
            )
            print(f"✅ Success ({name}): {response}")
            return # Stop after first success
        except Exception as e:
            print(f"❌ Failed ({name}): {e}")

if __name__ == "__main__":
    asyncio.run(test_g4f())
