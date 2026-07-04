import 'dart:typed_data';
import 'package:pdf/pdf.dart';
import 'package:pdf/widgets.dart' as pw;
import 'package:printing/printing.dart';
import '../../auth/data/user_model.dart';

class PdfHelper {
  static Future<void> generateAndPrintPdf({
    required UserModel user,
    required List<dynamic> historyData,
    required String startDate,
    required String endDate,
  }) async {
    final doc = pw.Document();

    doc.addPage(
      pw.Page(
        pageFormat: PdfPageFormat.a4,
        build: (pw.Context context) {
          return pw.Column(
            crossAxisAlignment: pw.CrossAxisAlignment.center,
            children: [
              pw.Text('PIMPINAN CABANG MUHAMMADIYAH', style: pw.TextStyle(fontWeight: pw.FontWeight.bold, fontSize: 14)),
              pw.Text('KEBAKKRAMAT, KARANGANYAR', style: pw.TextStyle(fontSize: 12)),
              pw.SizedBox(height: 5),
              pw.Text('Jl. Simo, Kebaksari 05/02 Kebak, Kebakkramat, Karanganyar', style: const pw.TextStyle(fontSize: 9)),
              pw.Divider(),
              pw.SizedBox(height: 10),
              pw.Text('LAPORAN PRESENSI KAJIAN AHAD PAGI', style: pw.TextStyle(fontWeight: pw.FontWeight.bold, fontSize: 12)),
              pw.Text('Periode: $startDate s.d. $endDate', style: const pw.TextStyle(fontSize: 10)),
              pw.SizedBox(height: 15),
              pw.Row(
                crossAxisAlignment: pw.CrossAxisAlignment.start,
                children: [
                  pw.Column(
                    crossAxisAlignment: pw.CrossAxisAlignment.start,
                    children: [
                      pw.Text('Nama    : ${user.nama}'),
                      pw.Text('NBM      : ${user.nbm ?? "-"}'),
                      pw.Text('AUM      : ${user.aum}'),
                    ],
                  ),
                ]
              ),
              pw.SizedBox(height: 15),
              pw.Table.fromTextArray(
                headers: ['No', 'Hari/Tanggal', 'Jam', 'Lokasi'],
                data: List.generate(historyData.length, (index) {
                  final item = historyData[index];
                  String lokasi = item['lokasi'] ?? '';
                  if (lokasi.contains('(')) {
                    lokasi = lokasi.split('(')[0].trim();
                  }
                  return [
                    (index + 1).toString(),
                    item['tanggal'] ?? '',
                    item['jam'] ?? '',
                    lokasi,
                  ];
                }),
                headerStyle: pw.TextStyle(color: PdfColors.white, fontWeight: pw.FontWeight.bold),
                headerDecoration: const pw.BoxDecoration(color: PdfColor.fromInt(0xFF0F766E)),
                cellPadding: const pw.EdgeInsets.all(5),
              ),
              pw.SizedBox(height: 40),
              pw.Row(
                mainAxisAlignment: pw.MainAxisAlignment.spaceBetween,
                children: [
                  pw.Column(
                    children: [
                      pw.Text('Mengetahui,'),
                      pw.Text('Ketua PCM Kebakkramat'),
                      pw.SizedBox(height: 40),
                      pw.Text('Ir. H. Paryono', style: pw.TextStyle(fontWeight: pw.FontWeight.bold)),
                    ]
                  ),
                  pw.Column(
                    children: [
                      pw.Text('Karanganyar, ${DateTime.now().toIso8601String().split('T')[0]}'),
                      pw.Text('Pembuat,'),
                      pw.SizedBox(height: 40),
                      pw.Text(user.nama, style: pw.TextStyle(fontWeight: pw.FontWeight.bold)),
                    ]
                  ),
                ]
              )
            ],
          );
        },
      ),
    );

    await Printing.layoutPdf(
      onLayout: (PdfPageFormat format) async => doc.save(),
    );
  }
}
