import os

def search_pattern(pattern, directory):
    for root, dirs, files in os.walk(directory):
        # Modify dirs in-place to avoid walking into them
        dirs[:] = [d for d in dirs if d not in ["venv", ".git", "node_modules", "vendor", "__pycache__", ".claude"]]
        
        for file in files:
            if file.endswith(('.py', '.php', '.sql', '.json', '.txt', '.md')):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if pattern.lower() in content.lower():
                            print(f"Match in {path}")
                            lines = content.split('\n')
                            for idx, line in enumerate(lines):
                                if pattern.lower() in line.lower():
                                    print(f"  Line {idx+1}: {line.strip()[:100]}")
                except Exception as e:
                    pass

print("Searching for 'compragamer'...")
search_pattern('compragamer', 'z:/')
