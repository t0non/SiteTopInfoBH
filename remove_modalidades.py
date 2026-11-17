import re

with open('lawyers-content.html', encoding='utf-8') as f:
    c = f.read()

before = len(c)

# Remove the plans-section (MODALIDADES DE ATENDIMENTO) with its preceding comment
c2 = re.sub(r'\s*<!--\s*PLANOS E ATENDIMENTO\s*-->\s*<section class="remote-section plans-section">.*?</section>', '', c, flags=re.S)

if len(c2) == before:
    # Try without comment
    c2 = re.sub(r'\s*<section class="remote-section plans-section">.*?</section>', '', c, flags=re.S)

print(f'Before: {before}, After: {len(c2)}, Removed: {before - len(c2)} chars')
print('plans-section present after:', 'plans-section' in c2)
print('MODALIDADES present after:', 'MODALIDADES' in c2)

with open('lawyers-content.html', 'w', encoding='utf-8') as f:
    f.write(c2)
print('Done.')
