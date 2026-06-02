import os
log_path = r"C:\Users\lucas\.gemini\antigravity-ide\brain\23d54e36-20b2-44a4-bddc-d682a46b468c\.system_generated\tasks\task-224.log"
if os.path.exists(log_path):
    print("Log file exists. Content:")
    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        print(f.read())
else:
    print(f"Log file not found at: {log_path}")
