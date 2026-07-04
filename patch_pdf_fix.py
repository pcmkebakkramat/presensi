import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Change icons for modals
modal_blocks = ["leaderboardScreen", "heatmapScreen", "daftarAumScreen", "detailScreen"]
for modal in modal_blocks:
    # We replace pdf-fill with printer-fill only in the headers of these modals.
    # We can just do a regex replace in the modal header strings.
    pass

content = content.replace(
    'title="Cetak PDF"><i class="bi bi-file-earmark-pdf-fill"></i>',
    'title="Cetak PDF"><i class="bi bi-printer-fill"></i>'
)

# 2. Fix variable references in cetakPalingAktif
content = content.replace(
    "var tableBody = cachedRankData.map((item, index) => [",
    "if(!globalRankingData) return;\n              var tableBody = globalRankingData.topUsers.map((item, index) => ["
)
content = content.replace(
    "item.total + \"x\"",
    "item.count + \"x\""
)
content = content.replace(
    "formatTanggalIndoSimple(item.terakhirHadir)",
    "formatTanggalIndoSimple(item.firstTime)"
)

# 3. Fix variable references in cetakAumTeraktif
content = content.replace(
    "var tableBody = cachedAumData.map((item, index) => [",
    "if(!globalRankingData) return;\n              var tableBody = globalRankingData.topAums.map((item, index) => ["
)
content = content.replace(
    "item.totalHadir + \"x\",\n                  item.jumlahJamaah + \" Org\",\n                  item.persentase + \"%\"",
    "item.count + \"x\",\n                  item.memberList.length + \" Org\",\n                  \"-\""
)

# 4. Fix variable references in cetakDaftarAum
content = content.replace(
    "doc.text(\"Total AUM: \" + cachedAumList.length, 15, 60);",
    "doc.text(\"Total AUM: \" + globalRankingData.daftarAum.length, 15, 60);"
)
content = content.replace(
    "var tableBody = cachedAumList.map((item, index) => [",
    "if(!globalRankingData) return;\n              var tableBody = globalRankingData.daftarAum.map((item, index) => ["
)
# Note: daftarAum is just an array of strings now!
content = content.replace(
    "item.aum,\n                  item.jumlahJamaah + \" Orang\"",
    "item,\n                  \"-\""
)

# 5. Inject globals for currentDetailData and currentDetailType
if "var currentDetailData" not in content:
    content = content.replace(
        "var reportData = [];",
        "var reportData = [];\n            var currentDetailData = null;\n            var currentDetailType = \"\";"
    )

# 6. Inject assignments in showUserDetail
showUser_assign = """              document.getElementById('detailTitle').innerText = user.nama;
              
              currentDetailType = 'user';
              currentDetailData = {
                  nama: user.nama,
                  aum: user.aum,
                  total: user.count,
                  history: user.history.map(h => ({
                      tanggal: h.tglStr,
                      jam: h.waktu,
                      lokasi: h.lokasi
                  }))
              };"""
content = content.replace(
    "document.getElementById('detailTitle').innerText = user.nama;",
    showUser_assign
)

# 7. Inject assignments in showAumDetail
showAum_assign = """              document.getElementById('detailTitle').innerText = "Detail AUM: " + aum.aum;
              
              currentDetailType = 'aum';
              currentDetailData = {
                  aum: aum.aum,
                  totalHadir: aum.count,
                  jamaahList: aum.memberList.map(m => ({
                      nama: m.nama,
                      hadir: m.count
                  }))
              };"""
content = content.replace(
    "document.getElementById('detailTitle').innerText = \"Detail AUM: \" + aum.aum;",
    showAum_assign
)


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("done")
