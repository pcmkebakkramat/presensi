with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Paling Aktif PDF Title
content = content.replace(
    'var titleStr = "Per Tanggal: " + formatTanggalIndoSimple(new Date()) + " (Total keseluruhan: sejak " + formatTanggalIndoSimple(firstTime) + ")";',
    'var titleStr = "Per Tanggal: " + formatTanggalIndoSimple(new Date()) + " (Total " + globalTotal + " Kegiatan sejak " + formatTanggalIndoSimple(firstTime) + ")";'
)

# 2. AUM Teraktif Detail UI
content = content.replace(
    '''<div class="text-truncate" style="max-width:75%; cursor:pointer; color:var(--primary);" onclick="showUserDetailByName('${m.nama.replace(/'/g, "\\'")}')"><span class="fw-bold me-2" style="color:#64748b;">${idx + 1}.</span> <span class="text-capitalize text-decoration-underline">${m.nama.toLowerCase()}</span></div>
                <div class="badge bg-secondary rounded-pill">${m.count}x</div>''',
    '''<div class="text-truncate" style="max-width:75%;"><span class="fw-bold me-2" style="color:#64748b;">${idx + 1}.</span> <span class="text-capitalize">${m.nama.toLowerCase()}</span></div>
                <div class="badge bg-primary rounded-pill" style="cursor:pointer;" onclick="fetchAndShowUserDetail('${m.nama.replace(/'/g, "\\'")}', this)">${m.count}x <i class="bi bi-chevron-right ms-1"></i></div>'''
)

# Add fetchAndShowUserDetail globally
fetch_code = """
            async function fetchAndShowUserDetail(nama, btnEl) {
              var originalHtml = btnEl.innerHTML;
              btnEl.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
              try {
                let req = await fetch(SCRIPT_URL, { method: 'POST', body: JSON.stringify({ action: 'getReport', nama: nama, limit: 500 }) });
                let res = await req.json();
                btnEl.innerHTML = originalHtml;
                if(res.status === 'success') {
                  currentDetailType = 'user';
                  currentDetailData = {
                      nama: cleanString(nama),
                      aum: cleanString(res.aum),
                      total: res.history.length,
                      history: res.history
                  };
                  
                  document.getElementById('detailTitle').innerText = cleanString(nama);
                  let c = document.getElementById('listDetail');
                  
                  if(res.history.length === 0) {
                      c.innerHTML = "<div class='text-center small text-muted py-3'>Belum ada riwayat kehadiran.</div>";
                  } else {
                      let html = `<div class="alert alert-light border small text-center mb-3">
                         Total Kehadiran: <strong>${res.history.length}x</strong><br>
                         <span class="text-muted" style="font-size:0.75rem;"><i class="bi bi-building"></i> ${cleanString(res.aum)}</span>
                      </div>`;
                      res.history.forEach(item => {
                         html += `<div class="list-group-item" style="border-radius:8px; margin-bottom:4px; font-size:0.85rem;">
                           <div class="d-flex w-100 justify-content-between mb-1">
                             <strong class="text-dark">${item.tanggal}</strong>
                             <span class="badge bg-light text-dark border"><i class="bi bi-clock"></i> ${item.jam}</span>
                           </div>
                           <div class="text-muted small"><i class="bi bi-geo-alt-fill text-danger"></i> ${item.lokasi.split('(')[0].trim()}</div>
                         </div>`;
                      });
                      c.innerHTML = html;
                  }
                  
                  document.getElementById('detailScreen').classList.remove('hidden');
                } else {
                  alert("Gagal mengambil data: " + res.message);
                }
              } catch (e) {
                btnEl.innerHTML = originalHtml;
                alert("Error: " + e);
              }
            }
"""

if "function showAumDetail" in content:
    content = content.replace("function showAumDetail(index) {", fetch_code + "\n            function showAumDetail(index) {")

# 3. Daftar AUM UI
old_render_daftar = """            function renderDaftarAum(daftar) {
              let c = document.getElementById('listDaftarAum');
              if (daftar.length === 0) { c.innerHTML = "<div class='text-center small text-muted py-3'>Belum ada data.</div>"; return; }
              let html = `<div class="alert alert-light border small text-center mb-3"><i class="bi bi-info-circle text-primary"></i> Total AUM Terdaftar: <strong>${daftar.length}</strong></div>`;
              daftar.forEach(a => {
                html += `<div class="list-group-item" style="border-radius:12px; margin-bottom:6px; border:1px solid #e2e8f0; font-weight:500; color:#334155;"><i class="bi bi-building me-2 text-primary"></i> ${a}</div>`;
              });
              c.innerHTML = html;
            }"""

new_render_daftar = """            function renderDaftarAum(daftar) {
              let c = document.getElementById('listDaftarAum');
              if (daftar.length === 0) { c.innerHTML = "<div class='text-center small text-muted py-3'>Belum ada data.</div>"; return; }
              let html = `<div class="alert alert-light border small text-center mb-3"><i class="bi bi-info-circle text-primary"></i> Total AUM Terdaftar: <strong>${daftar.length}</strong></div>`;
              daftar.forEach((a, i) => {
                let memberCount = 0;
                let topAumIdx = -1;
                if(globalRankingData && globalRankingData.topAums) {
                    topAumIdx = globalRankingData.topAums.findIndex(x => cleanString(x.aum) === cleanString(a));
                    if(topAumIdx !== -1) memberCount = globalRankingData.topAums[topAumIdx].memberList.length;
                }
                
                html += `<div class="list-group-item d-flex justify-content-between align-items-center" style="border-radius:12px; margin-bottom:6px; border:1px solid #e2e8f0; font-weight:500; color:#334155;">
                  <div><i class="bi bi-building me-2 text-primary"></i> ${a}</div>
                  <div class="badge ${memberCount > 0 ? 'bg-primary' : 'bg-secondary'} rounded-pill" style="cursor:pointer;" onclick="if(${memberCount} > 0){ showAumDetail(${topAumIdx}); document.getElementById('detailScreen').classList.remove('hidden'); } else { alert('Belum ada jamaah yang terdata hadir di AUM ini.'); }">${memberCount} Jamaah ${memberCount > 0 ? '<i class="bi bi-chevron-right ms-1"></i>' : ''}</div>
                </div>`;
              });
              c.innerHTML = html;
            }"""

content = content.replace(old_render_daftar, new_render_daftar)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated requests successfully.")
