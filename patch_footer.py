import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

correct_footer = """
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
        // Kiri: Ketua PCM
        doc.text("Mengetahui,", 15, finalY);
        doc.text("Ketua PCM Kebakkramat", 15, finalY + 5);

        // Kanan: Pembuat
        doc.text(tglCetak, pageWidth - 60, finalY);
        doc.text("Pembuat,", pageWidth - 60, finalY + 5);

        // Space Tanda Tangan
        doc.text("Ir. H. Paryono", 15, finalY + 30);
        doc.setFontSize(9);
        doc.text("NBM. 1120 7223 1460 777", 15, finalY + 34);

        doc.setFontSize(10);
        doc.text(CURRENT_USER.nama, pageWidth - 60, finalY + 30);
        doc.setFontSize(9);
        var nbmText = userNBM ? userNBM : "-";
        doc.text("NBM. " + nbmText, pageWidth - 60, finalY + 34);
      }
    }
"""

start_str = "function generatePdfFooter(doc, isMassal = false) {"
end_str = "async function generatePDF() {"

start_idx = content.find(start_str)
end_idx = content.find(end_str)

if start_idx != -1 and end_idx != -1:
    new_content = content[:start_idx] + correct_footer.strip() + "\n\n    " + content[end_idx:]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
