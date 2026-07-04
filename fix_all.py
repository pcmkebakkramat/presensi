with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Paling Aktif PDF: Persentase & Total Global
content = content.replace(
    '''                doc.text("Per Tanggal: " + formatTanggalIndoSimple(new Date()), pageWidth / 2, 51, { align: "center" });

                if(!globalRankingData) return;''',
    '''                if(!globalRankingData) return;
                var globalTotalStr = document.getElementById('statCountText').innerText.split(" dari ")[1] || "1";
                var globalTotal = parseInt(globalTotalStr) || 1;
                var firstTime = Math.min(...globalRankingData.topUsers.map(u => u.firstTime));
                var titleStr = "Per Tanggal: " + formatTanggalIndoSimple(new Date()) + " (Total keseluruhan: sejak " + formatTanggalIndoSimple(firstTime) + ")";
                doc.text(titleStr, pageWidth / 2, 51, { align: "center" });'''
)
content = content.replace(
    "head: [['No', 'Nama Jamaah', 'Asal AUM', 'Hadir', 'Terakhir Hadir']]",
    "head: [['No', 'Nama Jamaah', 'Asal AUM', 'Hadir', 'Persentase']]"
)
content = content.replace(
    "formatTanggalIndoSimple(item.firstTime)",
    "Math.round((item.count / globalTotal) * 100) + \"%\""
)

# 2. AUM Teraktif PDF: Paling Aktif
content = content.replace(
    "head: [['No', 'Nama AUM', 'Total Hadir', 'Jml Jamaah', 'Persentase']]",
    "head: [['No', 'Nama AUM', 'Total Hadir', 'Jml Jamaah', 'Paling Aktif']]"
)
content = content.replace(
    '''                  item.count + "x",
                  item.memberList.length + " Org",
                  "-"''',
    '''                  item.count + "x",
                  item.memberList.length + " Org",
                  item.memberList.length > 0 ? cleanString(item.memberList[0].nama) : "-"'''
)

# 3. Cetak AUM Detail Output is Wrong (Fix missing injection)
showAum_assign = """              document.getElementById('detailTitle').innerText = "Detail AUM: " + cleanString(aum.aum);
              
              currentDetailType = 'aum';
              currentDetailData = {
                  aum: cleanString(aum.aum),
                  totalHadir: aum.count,
                  jamaahList: aum.memberList.map(m => ({
                      nama: cleanString(m.nama),
                      hadir: m.count
                  }))
              };"""
if "document.getElementById('detailTitle').innerText = aum.aum;" in content:
    content = content.replace(
        "document.getElementById('detailTitle').innerText = aum.aum;",
        showAum_assign
    )
else:
    print("Warning: Could not find showAumDetail assignment string.")

# To make names clickable inside AUM Detail:
content = content.replace(
    '''<div class="text-truncate" style="max-width:75%;"><span class="fw-bold me-2" style="color:#64748b;">${idx + 1}.</span> <span class="text-capitalize">${m.nama.toLowerCase()}</span></div>''',
    '''<div class="text-truncate" style="max-width:75%; cursor:pointer; color:var(--primary);" onclick="showUserDetailByName('${m.nama.replace(/'/g, "\\'")}')"><span class="fw-bold me-2" style="color:#64748b;">${idx + 1}.</span> <span class="text-capitalize text-decoration-underline">${m.nama.toLowerCase()}</span></div>'''
)

# We need to add showUserDetailByName function globally
showUserByNameFn = """            function showUserDetailByName(nama) {
              if (!globalRankingData) return;
              let idx = globalRankingData.topUsers.findIndex(u => cleanString(u.nama) === cleanString(nama));
              if (idx !== -1) {
                showUserDetail(idx);
              } else {
                alert("Detail riwayat lengkap untuk jamaah ini belum termuat di memori utama (bukan Top 20).");
              }
            }"""
if "function showUserDetail(index)" in content:
    content = content.replace(
        "function showUserDetail(index) {",
        showUserByNameFn + "\n\n            function showUserDetail(index) {"
    )

# 4. Daftar AUM PDF: fix missing jumlah jamaah
daftarAumMap = """              var tableBody = globalRankingData.daftarAum.map((item, index) => {
                var c = 0;
                var found = globalRankingData.topAums.find(a => cleanString(a.aum) === cleanString(item));
                if (found) c = found.memberList.length;
                return [
                  index + 1,
                  cleanString(item),
                  c + " Orang"
                ];
              });"""
old_daftarAumMap = """              var tableBody = globalRankingData.daftarAum.map((item, index) => [
                  index + 1,
                  cleanString(item),
                  "-"
                ]);"""
content = content.replace(old_daftarAumMap, daftarAumMap)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("All fixes applied.")
