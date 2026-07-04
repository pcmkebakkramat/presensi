import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Protect against undefined history just in case
old = """        currentDetailData = {
          nama: cleanString(user.nama),
          aum: cleanString(user.aum),
          total: user.count,
          history: user.history.map(h => ({
            tanggal: h.tglStr,
            jam: h.waktu,
            lokasi: h.lokasi
          }))
        };"""

new = """        currentDetailData = {
          nama: cleanString(user.nama),
          aum: cleanString(user.aum),
          total: user.count,
          history: (user.history || []).map(h => ({
            tanggal: h.tglStr,
            jam: h.waktu,
            lokasi: h.lokasi
          }))
        };"""

content = content.replace(old, new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("patched history")
