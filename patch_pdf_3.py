with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

pdf_logic = """
    // --- PDF GENERATOR FUNCTION ---
    function generatePdfHeader(doc) {
      return new Promise((resolve, reject) => {
        const imgLogo = new Image();
        imgLogo.src = 'https://raw.githubusercontent.com/kangmrogram/pcmkebakkramat/refs/heads/main/icon-512.png';
        imgLogo.onload = function () {
          doc.addImage(imgLogo, 'PNG', 15, 10, 20, 20);
          doc.setFont("Helvetica", "bold");
          doc.setFontSize(14);
          doc.text("PIMPINAN CABANG MUHAMMADIYAH", 40, 18);
          doc.setFontSize(12);
          doc.text("KEBAKKRAMAT, KARANGANYAR", 40, 24);
          doc.setFont("Helvetica", "normal");
          doc.setFontSize(9);
          doc.text("Jl. Simo, Kebaksari 05/02 Kebak, Kebakkramat, Karanganyar, Jawa Tengah, 57762", 40, 30);
          doc.setLineWidth(0.5);
          doc.line(15, 35, doc.internal.pageSize.getWidth() - 15, 35);
          resolve();
        };
        imgLogo.onerror = function () {
          alert("Gagal memuat logo untuk PDF. Pastikan koneksi internet lancar.");
          reject();
        };
      });
    }

    function generatePdfFooter(doc, isMassal = false) {
      let finalY = doc.lastAutoTable.finalY + 15;
      const pageWidth = doc.internal.pageSize.getWidth();
      if (finalY > 250) {
        doc.addPage();
        finalY = 20;
      }

      var tglCetak = "Karanganyar, " + formatTanggalIndoSimple(new Date());

      if (isMassal) {
        // Hanya ketua PCM di kanan
        doc.text(tglCetak, pageWidth - 15, finalY, { align: "right" });
        doc.text("Mengetahui,", pageWidth - 15, finalY + 5, { align: "right" });
        doc.text("Ketua PCM Kebakkramat", pageWidth - 15, finalY + 10, { align: "right" });
        doc.text("Ir. H. Paryono", pageWidth - 15, finalY + 30, { align: "right" });
        doc.setFontSize(9);
        doc.text("NBM. 1120 7223 1460 777", pageWidth - 15, finalY + 34, { align: "right" });
      } else {
        // Ketua PCM Kanan, Pembuat di kiri
        doc.text(tglCetak, pageWidth - 15, finalY, { align: "right" });
        doc.text("Mengetahui,", pageWidth - 15, finalY + 5, { align: "right" });
        doc.text("Ketua PCM Kebakkramat", pageWidth - 15, finalY + 10, { align: "right" });
        
        doc.text("Ir. H. Paryono", pageWidth - 15, finalY + 30, { align: "right" });
        doc.setFontSize(9);
        doc.text("NBM. 1120 7223 1460 777", pageWidth - 15, finalY + 34, { align: "right" });
      }
    }

    async function generatePDF() {
      if (!CURRENT_USER || reportData.length === 0) {
        alert("Data riwayat kosong atau belum dimuat. Silakan tekan tombol cari terlebih dahulu.");
        return;
      }

      // Animasi tombol cetak
      const btnCetak = document.querySelector('button[onclick="generatePDF()"]');
      const originalHTML = btnCetak.innerHTML;
      btnCetak.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
      btnCetak.disabled = true;

      const { jsPDF } = window.jspdf;
      const doc = new jsPDF();
      const pageWidth = doc.internal.pageSize.getWidth();

      try {
        await generatePdfHeader(doc);

        doc.setFont("Helvetica", "bold");
        doc.setFontSize(12);
        doc.text("LAPORAN PRESENSI INDIVIDU", pageWidth / 2, 45, { align: "center" });

        var tglAwal = document.getElementById('filterStart').value;
        var tglAkhir = document.getElementById('filterEnd').value;
        var periodeStr = "";
        if (tglAwal && tglAkhir) {
          periodeStr = formatTanggalIndoSimple(tglAwal) + " s.d. " + formatTanggalIndoSimple(tglAkhir);
        } else {
          var today = new Date();
          var firstDay = new Date(today.getFullYear(), 0, 1);
          periodeStr = formatTanggalIndoSimple(firstDay) + " s.d. " + formatTanggalIndoSimple(today);
        }

        doc.setFont("Helvetica", "normal");
        doc.setFontSize(10);
        doc.text("Periode: " + periodeStr, pageWidth / 2, 51, { align: "center" });

        doc.text("Nama", 15, 65); doc.text(": " + CURRENT_USER.nama, 40, 65);
        var nbmText = userNBM ? userNBM : "-";
        doc.text("NBM", 15, 70); doc.text(": " + nbmText, 40, 70);
        doc.text("AUM", 15, 75); doc.text(": " + CURRENT_USER.aum, 40, 75);

        var statCount = document.getElementById('statCountText').innerText;
        var statPercent = document.getElementById('statPercentText').innerText;
        doc.text("Total Hadir", 15, 80); doc.text(": " + statCount + " (" + statPercent + ")", 40, 80);

        var tableBody = reportData.map((item, index) => [
          index + 1,
          item.tanggal,
          item.jam,
          item.lokasi.split('(')[0]
        ]);

        doc.autoTable({
          startY: 87,
          head: [['No', 'Hari/Tanggal', 'Jam', 'Lokasi']],
          body: tableBody,
          theme: 'grid',
          headStyles: { fillColor: [15, 118, 110], textColor: 255, fontStyle: 'bold' },
          styles: { fontSize: 10, font: "Helvetica", cellPadding: 2 },
          columnStyles: {
            0: { cellWidth: 10, halign: 'center' },
            1: { cellWidth: 50 },
            2: { cellWidth: 30, halign: 'center' },
            3: { cellWidth: 'auto' }
          }
        });

        generatePdfFooter(doc, false);
        doc.save("Laporan_Presensi_" + CURRENT_USER.nama.replace(/\\s+/g, '_') + ".pdf");
      } catch(e) {
          console.error(e);
      } finally {
          btnCetak.innerHTML = originalHTML;
          btnCetak.disabled = false;
      }
    }

    async function cetakPalingAktif() {
      const btnCetak = document.getElementById('btnCetakPalingAktif');
      const originalHTML = btnCetak.innerHTML;
      btnCetak.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
      btnCetak.disabled = true;

      const { jsPDF } = window.jspdf;
      const doc = new jsPDF();
      const pageWidth = doc.internal.pageSize.getWidth();
      
      try {
        await generatePdfHeader(doc);
        
        doc.setFont("Helvetica", "bold");
        doc.setFontSize(12);
        doc.text("LAPORAN JAMAAH PALING AKTIF", pageWidth / 2, 45, { align: "center" });
        doc.setFont("Helvetica", "normal");
        doc.setFontSize(10);
        doc.text("Per Tanggal: " + formatTanggalIndoSimple(new Date()), pageWidth / 2, 51, { align: "center" });

        var tableBody = cachedRankData.map((item, index) => [
          index + 1,
          item.nama,
          item.aum,
          item.total + "x",
          formatTanggalIndoSimple(item.terakhirHadir)
        ]);

        doc.autoTable({
          startY: 60,
          head: [['No', 'Nama Jamaah', 'Asal AUM', 'Hadir', 'Terakhir Hadir']],
          body: tableBody,
          theme: 'grid',
          headStyles: { fillColor: [15, 118, 110] },
          styles: { fontSize: 9 }
        });

        generatePdfFooter(doc, true);
        doc.save("Jamaah_Paling_Aktif.pdf");
      } finally {
        btnCetak.innerHTML = originalHTML;
        btnCetak.disabled = false;
      }
    }

    async function cetakAumTeraktif() {
      const btnCetak = document.getElementById('btnCetakAumTeraktif');
      const originalHTML = btnCetak.innerHTML;
      btnCetak.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
      btnCetak.disabled = true;

      const { jsPDF } = window.jspdf;
      const doc = new jsPDF();
      const pageWidth = doc.internal.pageSize.getWidth();
      
      try {
        await generatePdfHeader(doc);
        
        doc.setFont("Helvetica", "bold");
        doc.setFontSize(12);
        doc.text("LAPORAN AUM TERAKTIF", pageWidth / 2, 45, { align: "center" });
        doc.setFont("Helvetica", "normal");
        doc.setFontSize(10);
        doc.text("Per Tanggal: " + formatTanggalIndoSimple(new Date()), pageWidth / 2, 51, { align: "center" });

        var tableBody = cachedAumData.map((item, index) => [
          index + 1,
          item.aum,
          item.totalHadir + "x",
          item.jumlahJamaah + " Org",
          item.persentase + "%"
        ]);

        doc.autoTable({
          startY: 60,
          head: [['No', 'Nama AUM', 'Total Hadir', 'Jml Jamaah', 'Persentase']],
          body: tableBody,
          theme: 'grid',
          headStyles: { fillColor: [15, 118, 110] },
          styles: { fontSize: 9 }
        });

        generatePdfFooter(doc, true);
        doc.save("AUM_Teraktif.pdf");
      } finally {
        btnCetak.innerHTML = originalHTML;
        btnCetak.disabled = false;
      }
    }

    async function cetakDaftarAum() {
      const btnCetak = document.getElementById('btnCetakDaftarAum');
      const originalHTML = btnCetak.innerHTML;
      btnCetak.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
      btnCetak.disabled = true;

      const { jsPDF } = window.jspdf;
      const doc = new jsPDF();
      const pageWidth = doc.internal.pageSize.getWidth();
      
      try {
        await generatePdfHeader(doc);
        
        doc.setFont("Helvetica", "bold");
        doc.setFontSize(12);
        doc.text("DAFTAR AUM DAN JUMLAH JAMAAH", pageWidth / 2, 45, { align: "center" });
        doc.setFont("Helvetica", "normal");
        doc.setFontSize(10);
        doc.text("Per Tanggal: " + formatTanggalIndoSimple(new Date()), pageWidth / 2, 51, { align: "center" });
        doc.text("Total AUM: " + cachedAumList.length, 15, 60);

        var tableBody = cachedAumList.map((item, index) => [
          index + 1,
          item.aum,
          item.jumlahJamaah + " Orang"
        ]);

        doc.autoTable({
          startY: 65,
          head: [['No', 'Nama AUM', 'Jumlah Jamaah']],
          body: tableBody,
          theme: 'grid',
          headStyles: { fillColor: [15, 118, 110] },
          styles: { fontSize: 10 }
        });

        generatePdfFooter(doc, true);
        doc.save("Daftar_AUM.pdf");
      } finally {
        btnCetak.innerHTML = originalHTML;
        btnCetak.disabled = false;
      }
    }

    async function cetakDetail() {
      if (!currentDetailData || !currentDetailType) return;
      
      const btnCetak = document.getElementById('btnCetakDetail');
      const originalHTML = btnCetak.innerHTML;
      btnCetak.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
      btnCetak.disabled = true;

      const { jsPDF } = window.jspdf;
      const doc = new jsPDF();
      const pageWidth = doc.internal.pageSize.getWidth();
      
      try {
        await generatePdfHeader(doc);
        
        doc.setFont("Helvetica", "bold");
        doc.setFontSize(12);
        
        if (currentDetailType === 'user') {
          doc.text("DETAIL KEHADIRAN JAMAAH", pageWidth / 2, 45, { align: "center" });
          doc.setFont("Helvetica", "normal");
          doc.setFontSize(10);
          doc.text("Nama: " + currentDetailData.nama, 15, 55);
          doc.text("AUM: " + currentDetailData.aum, 15, 60);
          doc.text("Total Hadir: " + currentDetailData.total + "x", 15, 65);

          var tableBody = currentDetailData.history.map((item, index) => [
            index + 1,
            item.tanggal,
            item.jam,
            item.lokasi
          ]);

          doc.autoTable({
            startY: 72,
            head: [['No', 'Tanggal', 'Jam', 'Lokasi']],
            body: tableBody,
            theme: 'grid',
            headStyles: { fillColor: [15, 118, 110] },
            styles: { fontSize: 9 }
          });
          
          generatePdfFooter(doc, true);
          doc.save("Detail_Jamaah_" + currentDetailData.nama.replace(/\\s+/g, '_') + ".pdf");
          
        } else if (currentDetailType === 'aum') {
          doc.text("DETAIL JAMAAH AUM TERAKTIF", pageWidth / 2, 45, { align: "center" });
          doc.setFont("Helvetica", "normal");
          doc.setFontSize(10);
          doc.text("AUM: " + currentDetailData.aum, 15, 55);
          doc.text("Total Hadir (Akumulasi): " + currentDetailData.totalHadir + "x", 15, 60);

          var tableBody = currentDetailData.jamaahList.map((item, index) => [
            index + 1,
            item.nama,
            item.hadir + "x"
          ]);

          doc.autoTable({
            startY: 67,
            head: [['No', 'Nama Jamaah', 'Jumlah Hadir']],
            body: tableBody,
            theme: 'grid',
            headStyles: { fillColor: [15, 118, 110] },
            styles: { fontSize: 10 }
          });
          
          generatePdfFooter(doc, true);
          doc.save("Detail_AUM_" + currentDetailData.aum.replace(/\\s+/g, '_') + ".pdf");
        }
      } finally {
        btnCetak.innerHTML = originalHTML;
        btnCetak.disabled = false;
      }
    }
"""

start_str = "// --- PDF GENERATOR FUNCTION ---"
end_str = "function formatTanggalIndoSimple"

start_idx = content.find(start_str)
end_idx = content.find(end_str)

if start_idx != -1 and end_idx != -1:
    new_content = content[:start_idx] + pdf_logic + "\n    " + content[end_idx:]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
        
