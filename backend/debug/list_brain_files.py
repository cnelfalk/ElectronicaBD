import os
base = r"C:\Users\lucas\.gemini\antigravity-ide\brain\23d54e36-20b2-44a4-bddc-d682a46b468c"
if os.path.exists(base):
    for root, dirs, files in os.walk(base):
        for f in files:
            path = os.path.join(root, f)
            print(path)
else:
    print("Base dir doesn't exist.")
