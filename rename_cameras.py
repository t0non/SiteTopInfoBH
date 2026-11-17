import glob

files = glob.glob('dist/**/*.html', recursive=True) + ['dist/index.html']
files = list(set(files))
count = 0
for path in files:
    try:
        with open(path, encoding='utf-8') as f:
            c = f.read()
        if 'href="/#cameras">Câmeras<' in c or 'href="/suporte-remoto/../../#cameras">Câmeras<' in c or '>Câmeras<' in c:
            c2 = c.replace('>Câmeras<', '>Instalação de câmeras<')
            if c2 != c:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(c2)
                count += 1
    except Exception as e:
        print(f"Error {path}: {e}")

print(f"Updated {count} files.")
