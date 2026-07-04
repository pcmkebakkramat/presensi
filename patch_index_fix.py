import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Change (Klik) to >
content = content.replace('Total Jamaah Aktif: <span id="totalJamaahHeader">-</span> (Klik)</a>', 
                          'Total Jamaah Aktif: <span id="totalJamaahHeader">-</span> ></a>')

# 2. Fix showAllJamaah fallback
old_show = "let users = (globalRankingData && globalRankingData.allUsers) ? globalRankingData.allUsers : [];"
new_show = "let users = (globalRankingData && globalRankingData.allUsers) ? globalRankingData.allUsers : (globalRankingData ? globalRankingData.topUsers : []);"
content = content.replace(old_show, new_show)

# 3. Fix renderDaftarAum
old_render_daftar = """      function renderDaftarAum(daftar) {
        let c = document.getElementById('listDaftarAum');
        if (daftar.length === 0) { c.innerHTML = "<div class='text-center small text-muted py-3'>Belum ada data.</div>"; return; }
        let html = `<div class="alert alert-light border small text-center mb-3"><i class="bi bi-info-circle text-primary"></i> Total AUM Terdaftar: <strong>${daftar.length}</strong></div>`;"""

new_render_daftar = """      function renderDaftarAum(daftar) {
        let th = document.getElementById('totalAumDaftarHeader');
        if(th) th.innerText = daftar.length;
        let c = document.getElementById('listDaftarAum');
        if (daftar.length === 0) { c.innerHTML = "<div class='text-center small text-muted py-3'>Belum ada data.</div>"; return; }
        let html = "";"""

content = content.replace(old_render_daftar, new_render_daftar)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("fixed index.html")
