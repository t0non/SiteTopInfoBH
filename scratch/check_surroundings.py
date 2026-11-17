with open('remote-content.html', encoding='utf-8') as f:
    c = f.read()

idx1 = c.find('id="planos-empresas"')
idx2 = c.find('class="remote-section comparison-section"')
print("--- BEFORE PLANS-SECTION ---")
print(c[idx1-500:idx1])
print("--- PLANS-SECTION ---")
print(c[idx1:idx2])
print("--- AFTER PLANS-SECTION ---")
print(c[idx2:idx2+500])
