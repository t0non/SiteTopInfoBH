import re

with open('remote-content.html', encoding='utf-8') as f:
    c = f.read()

# Extract COMO FUNCIONA section (simple-explain-section)
m_como = re.search(r'(<section class="remote-section simple-explain-section">.*?</section>)', c, re.S)
# Extract PROBLEMAS DO DIA A DIA section
m_prob = re.search(r'(<!--\s*PROBLEMAS DO DIA A DIA.*?-->\s*<section class="remote-section" id="problemas-frequentes">.*?</section>)', c, re.S)

if not m_como:
    print("ERROR: simple-explain-section not found")
    exit(1)
if not m_prob:
    print("ERROR: problemas-frequentes section not found")
    exit(1)

sec_como = m_como.group(1)
sec_prob = m_prob.group(1)

print("COMO section chars:", len(sec_como))
print("PROB section chars:", len(sec_prob))

# The current order in file: sec_como appears first, then sec_prob
# We want: sec_prob first, then sec_como
# Replace the combined block
combined_original = sec_como + '\n\n  ' + sec_prob
combined_new = sec_prob + '\n\n  ' + sec_como

if combined_original not in c:
    # Try with actual whitespace between them
    # Find exact text between the two sections
    start_como = c.index(sec_como)
    end_como = start_como + len(sec_como)
    start_prob = c.index(sec_prob)
    between = c[end_como:start_prob]
    combined_original = sec_como + between + sec_prob
    combined_new = sec_prob + between + sec_como

if combined_original not in c:
    print("ERROR: could not locate the combined block")
    exit(1)

c2 = c.replace(combined_original, combined_new, 1)
print("Swap done, diff:", len(c2) - len(c), "chars (should be 0)")

with open('remote-content.html', 'w', encoding='utf-8') as f:
    f.write(c2)

# Verify new order
pos_prob = c2.find('id="problemas-frequentes"')
pos_como = c2.find('simple-explain-section')
print(f"PROBLEMAS position: {pos_prob}, COMO position: {pos_como}")
print("Order correct (PROBLEMAS before COMO):", pos_prob < pos_como)
