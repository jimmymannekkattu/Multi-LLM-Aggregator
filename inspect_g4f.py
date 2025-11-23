import g4f

print("Available attributes in g4f.models:")
for attr in dir(g4f.models):
    if not attr.startswith("__"):
        print(attr)
