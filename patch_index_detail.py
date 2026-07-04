import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update showAllJamaah HTML to include onclick
old_show_all = """        users.forEach((u, i) => {
          html += `<div class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                <div>
                  <div class="fw-bold" style="font-size: 0.9rem;">${cleanString(u.nama)}</div>
                  <div style="font-size: 0.75rem; color: #64748b;">${cleanString(u.aum)}</div>
                </div>
                <div class="badge bg-primary rounded-pill">${u.count}x</div>
              </div>`;
        });"""

new_show_all = """        users.forEach((u, i) => {
          html += `<div class="list-group-item list-group-item-action d-flex justify-content-between align-items-center" onclick="showUserDetail('${cleanString(u.nama)}')">
                <div>
                  <div class="fw-bold" style="font-size: 0.9rem;">${cleanString(u.nama)}</div>
                  <div style="font-size: 0.75rem; color: #64748b;">${cleanString(u.aum)}</div>
                </div>
                <div class="badge bg-primary rounded-pill px-3 py-2" style="cursor:pointer;">${u.count}x <i class="bi bi-chevron-right ms-1"></i></div>
              </div>`;
        });"""

content = content.replace(old_show_all, new_show_all)

# 2. Update showUserDetail to accept either index or name
old_show_user_detail = """      function showUserDetail(index) {
        currentAumIndex = null;
        if (!globalRankingData) return;
        let user = globalRankingData.topUsers[index];
        if (!user) return;"""

new_show_user_detail = """      function showUserDetail(identifier) {
        currentAumIndex = null;
        if (!globalRankingData) return;
        let user = null;
        if (typeof identifier === 'number') {
            user = globalRankingData.topUsers[identifier];
        } else {
            let list = (globalRankingData.allUsers) ? globalRankingData.allUsers : globalRankingData.topUsers;
            user = list.find(u => cleanString(u.nama) === identifier);
        }
        if (!user) { alert("Data riwayat jamaah ini belum termuat sepenuhnya dari server."); return; }"""

content = content.replace(old_show_user_detail, new_show_user_detail)

# 3. Add global loading overlay and logic to loadDashboardData
loading_html = """  <!-- GLOBAL LOADING OVERLAY -->
  <div id="globalLoadingScreen" class="fullscreen-overlay hidden" style="z-index: 2000; background: rgba(255,255,255,0.9);">
    <div class="d-flex flex-column justify-content-center align-items-center h-100">
      <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;" role="status"></div>
      <h6 class="mt-3 fw-bold text-dark">Mempersiapkan Data...</h6>
      <p class="small text-muted">Sedang mengambil rekapitulasi terbaru dari server</p>
    </div>
  </div>"""

content = content.replace("<body>", "<body>\n" + loading_html)

old_load_dashboard = """      async function loadDashboardData() {
        var start = document.getElementById('filterStart').value;
        var end = document.getElementById('filterEnd').value;
        try {
          let req = await fetch(SCRIPT_URL, { method: 'POST', body: JSON.stringify({ action: 'getReport', nama: CURRENT_USER.nama, start: start, end: end }) });
          let res = await req.json();"""

new_load_dashboard = """      async function loadDashboardData() {
        document.getElementById('globalLoadingScreen').classList.remove('hidden');
        var start = document.getElementById('filterStart').value;
        var end = document.getElementById('filterEnd').value;
        try {
          let req = await fetch(SCRIPT_URL, { method: 'POST', body: JSON.stringify({ action: 'getReport', nama: CURRENT_USER.nama, start: start, end: end }) });
          let res = await req.json();"""

content = content.replace(old_load_dashboard, new_load_dashboard)

old_load_catch = """            renderDaftarAum(res.data.daftarAum);
            if (res.data.trendData) renderTrendChart(res.data.trendData);
          }
        } catch (e) {
          console.error("Gagal memuat ranking:", e);
        }
      }"""

new_load_catch = """            renderDaftarAum(res.data.daftarAum);
            if (res.data.trendData) renderTrendChart(res.data.trendData);
          }
        } catch (e) {
          console.error("Gagal memuat ranking:", e);
        } finally {
          document.getElementById('globalLoadingScreen').classList.add('hidden');
        }
      }"""

content = content.replace(old_load_catch, new_load_catch)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("index.html patched")
