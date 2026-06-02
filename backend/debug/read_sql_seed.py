with open("z:/sql/techmatch.sql", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()
    
print("Checking categories table inserts in techmatch.sql:")
for line in lines:
    if "categorias" in line.lower() or "insert into" in line.lower():
        if any(c in line.lower() for c in ["almacenamiento", "ram", "gpu", "laptop", "cpu"]):
            print(line.strip())
