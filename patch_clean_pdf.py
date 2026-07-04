with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# In cetakPalingAktif
content = content.replace(
    '                  item.nama,\n                  item.aum,',
    '                  cleanString(item.nama),\n                  cleanString(item.aum),'
)

# In cetakAumTeraktif
content = content.replace(
    '                  item.aum,\n                  item.count + "x",',
    '                  cleanString(item.aum),\n                  item.count + "x",'
)

# In cetakDaftarAum
content = content.replace(
    '                  item,\n                  "-"',
    '                  cleanString(item),\n                  "-"'
)

# In showUserDetail (we injected this previously, it assigns currentDetailData)
content = content.replace(
    '                  nama: user.nama,\n                  aum: user.aum,',
    '                  nama: cleanString(user.nama),\n                  aum: cleanString(user.aum),'
)
content = content.replace(
    'document.getElementById(\'detailTitle\').innerText = user.nama;',
    'document.getElementById(\'detailTitle\').innerText = cleanString(user.nama);'
)

# In showAumDetail
content = content.replace(
    '                  aum: aum.aum,\n                  totalHadir: aum.count,',
    '                  aum: cleanString(aum.aum),\n                  totalHadir: aum.count,'
)
content = content.replace(
    'document.getElementById(\'detailTitle\').innerText = "Detail AUM: " + aum.aum;',
    'document.getElementById(\'detailTitle\').innerText = "Detail AUM: " + cleanString(aum.aum);'
)
content = content.replace(
    '                      nama: m.nama,\n                      hadir: m.count',
    '                      nama: cleanString(m.nama),\n                      hadir: m.count'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Applied cleanString to PDFs.")
