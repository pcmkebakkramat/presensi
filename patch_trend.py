with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Chart.js to <head>
if "chart.js" not in content.lower():
    content = content.replace(
        '</head>',
        '  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>\n</head>'
    )

# 2. Add Button in main buttons area
# The buttons area looks like:
# <div class="d-grid gap-2 mb-3">
#   <button class="btn btn-outline-primary" onclick="showFeatureModal('leaderboardScreen')"><i class="bi bi-trophy"></i> Jamaah Paling Aktif</button>
#   <button class="btn btn-outline-success" onclick="showFeatureModal('heatmapScreen')"><i class="bi bi-building"></i> AUM Teraktif</button>
#   <button class="btn btn-outline-info" onclick="showFeatureModal('daftarAumScreen')"><i class="bi bi-list-check"></i> Daftar AUM</button>
# </div>
btn_html = """          <button class="btn btn-outline-primary" onclick="showFeatureModal('leaderboardScreen')"><i class="bi bi-trophy"></i> Jamaah Paling Aktif</button>
          <button class="btn btn-outline-success" onclick="showFeatureModal('heatmapScreen')"><i class="bi bi-building"></i> AUM Teraktif</button>
          <button class="btn btn-outline-info" onclick="showFeatureModal('daftarAumScreen')"><i class="bi bi-list-check"></i> Daftar AUM</button>
          <button class="btn btn-outline-warning text-dark" onclick="showFeatureModal('trendScreen')"><i class="bi bi-graph-up-arrow"></i> Analitik Tren</button>"""

if "<button class=\"btn btn-outline-info\" onclick=\"showFeatureModal('daftarAumScreen')\"><i class=\"bi bi-list-check\"></i> Daftar AUM</button>" in content:
    content = content.replace(
        '''          <button class="btn btn-outline-primary" onclick="showFeatureModal('leaderboardScreen')"><i class="bi bi-trophy"></i> Jamaah Paling Aktif</button>
          <button class="btn btn-outline-success" onclick="showFeatureModal('heatmapScreen')"><i class="bi bi-building"></i> AUM Teraktif</button>
          <button class="btn btn-outline-info" onclick="showFeatureModal('daftarAumScreen')"><i class="bi bi-list-check"></i> Daftar AUM</button>''',
        btn_html
    )

# 3. Create trendScreen modal
modal_html = """
    <!-- MODAL TREND -->
    <div id="trendScreen" class="fullscreen-overlay hidden">
      <div class="overlay-header">
        <h6 class="m-0 fw-bold">Analitik Tren Kehadiran</h6>
        <div>
          <button class="btn btn-sm btn-danger me-2" id="btnCetakTrend" onclick="cetakTrend()" title="Cetak PDF"><i class="bi bi-printer-fill"></i></button>
          <button class="btn-close-custom" onclick="closeFeatureModal('trendScreen')"><i class="bi bi-x"></i></button>
        </div>
      </div>
      <div class="overlay-body" style="background:#f8fafc;">
        <div class="container py-3">
          <!-- Insights Cards -->
          <div class="row g-2 mb-3">
            <div class="col-4">
              <div class="card border-0 shadow-sm text-center h-100" style="border-radius:12px;">
                <div class="card-body p-2">
                  <div class="text-muted" style="font-size:0.7rem;">RATA-RATA</div>
                  <div class="fw-bold text-primary" style="font-size:1.1rem;" id="trendAvg">-</div>
                </div>
              </div>
            </div>
            <div class="col-4">
              <div class="card border-0 shadow-sm text-center h-100" style="border-radius:12px;">
                <div class="card-body p-2">
                  <div class="text-muted" style="font-size:0.7rem;">REKOR (PEAK)</div>
                  <div class="fw-bold text-success" style="font-size:1.1rem;" id="trendPeak">-</div>
                </div>
              </div>
            </div>
            <div class="col-4">
              <div class="card border-0 shadow-sm text-center h-100" style="border-radius:12px;">
                <div class="card-body p-2">
                  <div class="text-muted" style="font-size:0.7rem;">STATUS TREN</div>
                  <div class="fw-bold" style="font-size:0.9rem; padding-top:4px;" id="trendStatus">-</div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Chart -->
          <div class="card border-0 shadow-sm" style="border-radius:12px;">
            <div class="card-body p-2">
              <canvas id="trendChart" style="width:100%; height:300px;"></canvas>
            </div>
          </div>
          
          <div class="alert alert-info mt-3 small" style="border-radius:10px;">
            <i class="bi bi-info-circle-fill"></i> Grafik ini menunjukkan fluktuasi total jamaah yang hadir di setiap kegiatan pengajian dari waktu ke waktu.
          </div>
        </div>
      </div>
    </div>
"""
if 'id="trendScreen"' not in content:
    content = content.replace('    <!-- MODAL DAFTAR AUM -->', modal_html + '\n    <!-- MODAL DAFTAR AUM -->')

# 4. JavaScript logic (renderTrendChart and cetakTrend)
js_logic = """
            let trendChartInstance = null;

            function renderTrendChart() {
              if (!globalRankingData || !globalRankingData.trendData || globalRankingData.trendData.length === 0) {
                 document.getElementById('trendAvg').innerText = "0";
                 document.getElementById('trendPeak').innerText = "0";
                 document.getElementById('trendStatus').innerText = "-";
                 return;
              }
              
              let tData = globalRankingData.trendData;
              let labels = [];
              let dataPoints = [];
              let total = 0;
              let maxVal = 0;
              let maxDate = "";
              
              tData.forEach(d => {
                 let dObj = new Date(d.tanggal);
                 let labelStr = d.tanggal;
                 if(!isNaN(dObj.getTime())) {
                     labelStr = dObj.toLocaleDateString('id-ID', {day: 'numeric', month:'short'});
                 }
                 labels.push(labelStr);
                 dataPoints.push(d.jumlah);
                 
                 total += d.jumlah;
                 if(d.jumlah > maxVal) {
                     maxVal = d.jumlah;
                     maxDate = labelStr;
                 }
              });
              
              let avg = Math.round(total / tData.length);
              document.getElementById('trendAvg').innerText = avg;
              document.getElementById('trendPeak').innerHTML = maxVal + "<br><span style='font-size:0.6rem;font-weight:normal;'>" + maxDate + "</span>";
              
              let statusHtml = "<span class='text-secondary'>-</span>";
              if (tData.length >= 2) {
                 let current = tData[tData.length-1].jumlah;
                 let previous = tData[tData.length-2].jumlah;
                 if(current > previous) {
                     let pct = Math.round(((current - previous)/previous)*100);
                     statusHtml = `<span class="text-success"><i class="bi bi-arrow-up"></i> ${pct}%</span>`;
                 } else if (current < previous) {
                     let pct = Math.round(((previous - current)/previous)*100);
                     statusHtml = `<span class="text-danger"><i class="bi bi-arrow-down"></i> ${pct}%</span>`;
                 } else {
                     statusHtml = `<span class="text-secondary"><i class="bi bi-dash"></i> Stabil</span>`;
                 }
              }
              document.getElementById('trendStatus').innerHTML = statusHtml;

              const ctx = document.getElementById('trendChart').getContext('2d');
              
              if(trendChartInstance) {
                  trendChartInstance.destroy();
              }
              
              let gradient = ctx.createLinearGradient(0, 0, 0, 300);
              gradient.addColorStop(0, 'rgba(14, 165, 233, 0.4)');
              gradient.addColorStop(1, 'rgba(14, 165, 233, 0.0)');
              
              trendChartInstance = new Chart(ctx, {
                  type: 'line',
                  data: {
                      labels: labels,
                      datasets: [{
                          label: 'Total Kehadiran',
                          data: dataPoints,
                          borderColor: '#0ea5e9',
                          backgroundColor: gradient,
                          borderWidth: 2,
                          pointBackgroundColor: '#ffffff',
                          pointBorderColor: '#0ea5e9',
                          pointRadius: 4,
                          pointHoverRadius: 6,
                          fill: true,
                          tension: 0.4
                      }]
                  },
                  options: {
                      responsive: true,
                      maintainAspectRatio: false,
                      plugins: {
                          legend: { display: false },
                          tooltip: {
                              callbacks: {
                                  label: function(context) { return context.raw + ' Jamaah'; }
                              }
                          }
                      },
                      scales: {
                          y: { beginAtZero: true, grid: { color: '#f1f5f9' } },
                          x: { grid: { display: false } }
                      }
                  }
              });
            }

            async function cetakTrend() {
              const btnCetak = document.getElementById('btnCetakTrend');
              const originalHTML = btnCetak.innerHTML;
              btnCetak.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
              btnCetak.disabled = true;

              try {
                const { jsPDF } = window.jspdf;
                const doc = new jsPDF('landscape'); // Landscape better for graphs
                const pageWidth = doc.internal.pageSize.getWidth();

                await generatePdfHeader(doc);

                doc.setFont("Helvetica", "bold");
                doc.setFontSize(12);
                doc.text("LAPORAN ANALITIK TREN KEHADIRAN", pageWidth / 2, 45, { align: "center" });
                
                let avg = document.getElementById('trendAvg').innerText;
                let peak = document.getElementById('trendPeak').innerText.replace(/\\n/g, ' - ');
                
                doc.setFont("Helvetica", "normal");
                doc.setFontSize(10);
                doc.text(`Rata-rata Kehadiran: ${avg} Jamaah  |  Rekor Tertinggi: ${peak}`, pageWidth / 2, 52, { align: "center" });

                // Get image from canvas
                const canvas = document.getElementById('trendChart');
                const imgData = canvas.toDataURL('image/png', 1.0);
                
                // Draw image on PDF (calculate aspect ratio)
                const imgProps = doc.getImageProperties(imgData);
                const pdfWidth = pageWidth - 30; // 15mm margins
                const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;
                
                doc.addImage(imgData, 'PNG', 15, 60, pdfWidth, pdfHeight);
                
                doc.save('Analitik_Tren_Kehadiran.pdf');
              } catch(e) {
                alert("Gagal mencetak: " + e);
              } finally {
                btnCetak.innerHTML = originalHTML;
                btnCetak.disabled = false;
              }
            }
"""

if "function renderTrendChart" not in content:
    content = content.replace(
        "            function renderDaftarAum(daftar) {",
        js_logic + "\n            function renderDaftarAum(daftar) {"
    )

# 5. Call renderTrendChart in getRankingData success block
if "renderDaftarAum(globalRankingData.daftarAum);" in content and "renderTrendChart();" not in content:
    content = content.replace(
        "renderDaftarAum(globalRankingData.daftarAum);",
        "renderDaftarAum(globalRankingData.daftarAum);\n                  renderTrendChart();"
    )

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Trend Analytics implemented.")
