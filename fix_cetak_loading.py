import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add allJamaah to cetakDetail
old_cetak = """            generatePdfFooter(doc, true);
            doc.save("Detail_AUM_" + currentDetailData.aum.replace(/\s+/g, '_') + ".pdf");
          }
        } finally {"""

new_cetak = """            generatePdfFooter(doc, true);
            doc.save("Detail_AUM_" + currentDetailData.aum.replace(/\s+/g, '_') + ".pdf");
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
          }
        } finally {"""
content = content.replace(old_cetak, new_cetak)

# 2. Add loading spinner to Dashboard
old_dash_header = '<h6 class="m-0 fw-bold">Rekapitulasi Global</h6>'
new_dash_header = '<h6 class="m-0 fw-bold">Rekapitulasi Global <span id="dashLoading" class="spinner-border spinner-border-sm text-primary ms-2 hidden"></span></h6>'
content = content.replace(old_dash_header, new_dash_header)

old_load_dash = """      async function loadDashboardData() {
        var start = document.getElementById('filterStart').value;
        var end = document.getElementById('filterEnd').value;
        try {"""
new_load_dash = """      async function loadDashboardData() {
        let loader = document.getElementById('dashLoading');
        if(loader) loader.classList.remove('hidden');
        var start = document.getElementById('filterStart').value;
        var end = document.getElementById('filterEnd').value;
        try {"""
content = content.replace(old_load_dash, new_load_dash)

old_load_catch = """        } catch (e) {
          console.error("Gagal memuat ranking:", e);
        }
      }"""
new_load_catch = """        } catch (e) {
          console.error("Gagal memuat ranking:", e);
        } finally {
          let loader = document.getElementById('dashLoading');
          if(loader) loader.classList.add('hidden');
        }
      }"""
content = content.replace(old_load_catch, new_load_catch)


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("patched")
