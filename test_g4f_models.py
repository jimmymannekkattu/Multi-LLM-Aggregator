import asyncio
import g4f

# Models from g4f inspection
POPULAR_FREE_MODELS = [
    "gpt_4",
]

async def test_model(model_name):
    print(f"Testing {model_name}...")
    try:
        # Resolve string to object
        if hasattr(g4f.models, model_name):
            model_obj = getattr(g4f.models, model_name)
        else:
            print(f"❌ {model_name}: Attribute not found in g4f.models")
            return False

        response = await g4f.ChatCompletion.create_async(
            model=model_obj,
            messages=[{"role": "user", "content": "Say Hello"}],
        )
        print(f"✅ {model_name}: Success")
        return True
    except Exception as e:
        print(f"❌ {model_name}: Failed - {e}")
        return False

async def main():
    print("Starting g4f model verification...")
    results = await asyncio.gather(*(test_model(m) for m in POPULAR_FREE_MODELS))
    print(f"Passed: {sum(results)}/{len(results)}")

if __name__ == "__main__":
    asyncio.run(main())
