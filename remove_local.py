import re

with open(r'c:\Users\eduar\OneDrive\Desktop\SiteTop\remote-content.html', encoding='utf-8') as f:
    c = f.read()

before = len(c)

# Remove local-section with optional preceding comment
c2 = re.sub(r'\s*<!--[^>]*-->\s*<section[^>]*class="[^"]*local-section[^"]*"[^>]*>.*?</section>', '', c, flags=re.S)
if len(c2) == before:
    c2 = re.sub(r'\s*<section[^>]*class="[^"]*local-section[^"]*"[^>]*>.*?</section>', '', c, flags=re.S)

print(f'Before: {before}, After: {len(c2)}, Removed: {before - len(c2)} chars')
print('local-section present after:', 'local-section' in c2)
print('ONDE ATENDEMOS present after:', 'ONDE ATENDEMOS' in c2)

with open(r'c:\Users\eduar\OneDrive\Desktop\SiteTop\remote-content.html', 'w', encoding='utf-8') as f:
    f.write(c2)
print('Done.')
