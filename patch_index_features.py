import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Paling Aktif Header
content = content.replace(
    '<div class="overlay-body">\n        <div id="listPalingAktif" class="list-group">',
    """<div class="overlay-body">
        <div class="alert alert-light border small text-center mb-3">
           <i class="bi bi-info-circle"></i> Top 20 jamaah dengan presensi tertinggi.
           <br><a href="#" onclick="showAllJamaah()" style="text-decoration:none; font-weight:bold;">Total Jamaah Aktif: <span id="totalJamaahHeader">-</span> (Klik)</a>
        </div>
        <div id="listPalingAktif" class="list-group">"""
)

# 1. AUM Teraktif Header
content = content.replace(
    '<div class="overlay-body">\n        <div id="listAumTeraktif" class="list-group">',
    """<div class="overlay-body">
        <div class="alert alert-light border small text-center mb-3">
           <i class="bi bi-info-circle"></i> Peringkat AUM berdasarkan partisipasi jamaah terbanyak.
           <br><b>Total AUM Terdaftar: <span id="totalAumHeader">-</span></b>
        </div>
        <div id="listAumTeraktif" class="list-group">"""
)

# 1. Daftar AUM Header
content = content.replace(
    '<div class="alert alert-light border small text-center mb-3"><i class="bi bi-info-circle"></i> Daftar Amal Usaha\n          Muhammadiyah yang terdaftar.</div>',
    """<div class="alert alert-light border small text-center mb-3"><i class="bi bi-info-circle"></i> Daftar Amal Usaha Muhammadiyah (AUM) yang terdaftar di PCM Kebakkramat Karanganyar: <b id="totalAumDaftarHeader">-</b></div>"""
)
content = content.replace(
    '<div class="alert alert-light border small text-center mb-3"><i class="bi bi-info-circle"></i> Daftar Amal Usaha Muhammadiyah yang terdaftar.</div>',
    """<div class="alert alert-light border small text-center mb-3"><i class="bi bi-info-circle"></i> Daftar Amal Usaha Muhammadiyah (AUM) yang terdaftar di PCM Kebakkramat Karanganyar: <b id="totalAumDaftarHeader">-</b></div>"""
)

# Javascript additions
# renderPalingAktif
content = content.replace(
    "function renderPalingAktif(users) {",
    """function renderPalingAktif(users) {
        let th = document.getElementById('totalJamaahHeader');
        if(th) th.innerText = (globalRankingData && globalRankingData.allUsers) ? globalRankingData.allUsers.length : users.length;
"""
)

# renderAumTeraktif
content = content.replace(
    "function renderAumTeraktif(aums) {",
    """function renderAumTeraktif(aums) {
        let th = document.getElementById('totalAumHeader');
        if(th) th.innerText = (globalRankingData && globalRankingData.daftarAum) ? globalRankingData.daftarAum.length : '-';
"""
)

# renderDaftarAum
content = content.replace(
    "function renderDaftarAum(aums) {",
    """function renderDaftarAum(aums) {
        let th = document.getElementById('totalAumDaftarHeader');
        if(th) th.innerText = aums.length;
"""
)
content = content.replace(
    "html += `<div class='text-center small text-muted mt-3 py-2 border-top'>Total AUM Terdaftar: ${aums.length}</div>`;",
    ""
)

# add showAllJamaah
show_all = """
      function showAllJamaah() {
         let users = (globalRankingData && globalRankingData.allUsers) ? globalRankingData.allUsers : [];
         let html = "<div class='text-center py-3 text-muted small'>Daftar Seluruh Jamaah Aktif ("+users.length+" Orang)</div>";
         users.forEach((u, i) => {
            html += `<div class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                <div>
                  <div class="fw-bold" style="font-size: 0.9rem;">${cleanString(u.nama)}</div>
                  <div style="font-size: 0.75rem; color: #64748b;">${cleanString(u.aum)}</div>
                </div>
                <div class="badge bg-primary rounded-pill">${u.count}x</div>
              </div>`;
         });
         document.getElementById('detailTitle').innerText = "Daftar Seluruh Jamaah";
         document.getElementById('listDetail').innerHTML = html;
         currentDetailType = 'allJamaah';
         document.getElementById('detailScreen').classList.remove('hidden');
      }
      function formatTanggalIndoSimple"""
content = content.replace("function formatTanggalIndoSimple", show_all)

# cetakDetail
cetak_detail_new = """          if (currentDetailType === 'aumUsers') {
            doc.text("LAPORAN DETAIL KEHADIRAN JAMAAH (AUM)", pageWidth / 2, 45, { align: "center" });
            doc.setFont("Helvetica", "normal");
            doc.text("Asal AUM: " + currentAumName, pageWidth / 2, 51, { align: "center" });

            let aumInfo = globalRankingData.topAums.find(x => cleanString(x.aum) === currentAumName);
            let totalHadir = aumInfo ? aumInfo.count : 0;
            let totalOrang = aumInfo && aumInfo.memberList ? aumInfo.memberList.length : 0;

            doc.text("Total Kehadiran Jamaah: " + totalHadir + "x", 15, 65);
            doc.text("Jumlah Anggota Aktif: " + totalOrang + " Orang", 15, 71);

            let tbData = [];
            if (aumInfo && aumInfo.memberList) {
              aumInfo.memberList.forEach((m, i) => { tbData.push([i + 1, cleanString(m.nama), m.count + "x"]); });
            }

            doc.autoTable({ startY: 80, head: [['No', 'Nama Jamaah', 'Jumlah Hadir']], body: tbData, theme: 'grid', styles: { fontSize: 9, cellPadding: 3 }, headStyles: { fillColor: [15, 118, 110] } });
            
          } else if (currentDetailType === 'allJamaah') {
            doc.text("DAFTAR SELURUH JAMAAH AKTIF", pageWidth / 2, 45, { align: "center" });
            doc.setFont("Helvetica", "normal");
            let users = (globalRankingData && globalRankingData.allUsers) ? globalRankingData.allUsers : [];
            doc.text("Total Jamaah: " + users.length + " Orang", pageWidth / 2, 51, { align: "center" });

            let tbData = [];
            users.forEach((u, i) => { tbData.push([i + 1, cleanString(u.nama), cleanString(u.aum), u.count + "x"]); });
            doc.autoTable({ startY: 60, head: [['No', 'Nama Jamaah', 'Asal AUM', 'Jumlah Hadir']], body: tbData, theme: 'grid', styles: { fontSize: 8, cellPadding: 3 }, headStyles: { fillColor: [15, 118, 110] } });
            
            var finalY = doc.lastAutoTable.finalY + 15;
            if (finalY > doc.internal.pageSize.getHeight() - 40) { doc.addPage(); finalY = 20; }
            var tglCetak = "Karanganyar, " + formatTanggalIndoSimple(new Date());
            doc.text(tglCetak, pageWidth - 15, finalY, { align: "right" });
            doc.text("Mengetahui,", pageWidth - 15, finalY + 5, { align: "right" });
            doc.text("Ketua PCM Kebakkramat", pageWidth - 15, finalY + 10, { align: "right" });
            doc.text("Ir. H. Paryono", pageWidth - 15, finalY + 30, { align: "right" });
            doc.setFontSize(9);
            doc.text("NBM. 1120 7223 1460 777", pageWidth - 15, finalY + 34, { align: "right" });

            doc.save("Daftar_Seluruh_Jamaah.pdf");
            return;
            
          } else {"""
content = content.replace(
    """          if (currentDetailType === 'aumUsers') {
            doc.text("LAPORAN DETAIL KEHADIRAN JAMAAH (AUM)", pageWidth / 2, 45, { align: "center" });
            doc.setFont("Helvetica", "normal");
            doc.text("Asal AUM: " + currentAumName, pageWidth / 2, 51, { align: "center" });

            let aumInfo = globalRankingData.topAums.find(x => cleanString(x.aum) === currentAumName);
            let totalHadir = aumInfo ? aumInfo.count : 0;
            let totalOrang = aumInfo && aumInfo.memberList ? aumInfo.memberList.length : 0;

            doc.text("Total Kehadiran Jamaah: " + totalHadir + "x", 15, 65);
            doc.text("Jumlah Anggota Aktif: " + totalOrang + " Orang", 15, 71);

            let tbData = [];
            if (aumInfo && aumInfo.memberList) {
              aumInfo.memberList.forEach((m, i) => { tbData.push([i + 1, cleanString(m.nama), m.count + "x"]); });
            }

            doc.autoTable({ startY: 80, head: [['No', 'Nama Jamaah', 'Jumlah Hadir']], body: tbData, theme: 'grid', styles: { fontSize: 9, cellPadding: 3 }, headStyles: { fillColor: [15, 118, 110] } });
          } else {""",
          cetak_detail_new
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("index HTML patched")
