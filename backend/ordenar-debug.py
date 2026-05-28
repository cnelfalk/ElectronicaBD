import os, shutil
os.makedirs('debug', exist_ok=True)
archivos = ['debug_amd.html', 'debug_amd_http1.html', 'debug_amd_new.html', 'debug_compra_gamer.html', 'debug_intel.html', 'debug_lenovo_consumer.html', 'debug_lenovo_psref.html', 'ml_debug.html', 'debug_sources.py', 'debug_ml.py']
for a in archivos:
    if os.path.exists(a):
        if a.endswith('.py'):
            with open(a, 'r', encoding='utf-8') as f: lines = f.readlines()
            for i, l in enumerate(lines):
                if 'sys.path.append(os.path.dirname(os.path.abspath(__file__)))' in l:
                    lines[i] = 'sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))\n'
            with open(a, 'w', encoding='utf-8') as f: f.writelines(lines)
        shutil.move(a, os.path.join('debug', a))
        print(f'Movido: {a} -> debug/{a}')