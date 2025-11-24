import g4f

def inspect_models():
    print("Available g4f models matching 'gemini':")
    found = False
    for attr in dir(g4f.models):
        if attr.startswith("_"):
            continue
        if "gemini" in attr.lower():
            print(f"- {attr}")
            found = True
    
    if not found:
        print("No models found matching 'gemini'.")

    print("\nAll available models (first 50):")
    count = 0
    for attr in dir(g4f.models):
        if not attr.startswith("_"):
            print(f"- {attr}")
            count += 1
            if count >= 50:
                break

if __name__ == "__main__":
    inspect_models()
