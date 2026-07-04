
            // --- KONFIGURASI URL SERVER ---
            const SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyY74AHkvY7WOg3ZgN_Iq8joHRcmW9O6wvy_cq3LGiKZLgS7ZzMEjR411g9DSe5YcS3lg/exec";
            const MAX_RADIUS = 500;
            const DAFTAR_LOKASI = [
              { nama: "Masjid Abdul Aziz (SMP Muhammadiyah 8 Kebakkramat)", lat: -7.520470615403366, lng: 110.9065007512984, start: 600, end: 730 },
              { nama: "Gedung Dakwah PDM Karanganyar", lat: -7.586223863399417, lng: 110.91830297060768, start: 600, end: 730 },
              { nama: "Masjid Al Mukarromah, Karanganyar", lat: -7.5991158597467505, lng: 110.95277542273423, start: 600, end: 730 },
              { nama: "SMP Muhammadiyah 2 Karanganyar", lat: -7.59240065605104, lng: 110.95609234835774, start: 600, end: 730 },
              { nama: "Masjid Raya Al Falah Sragen", lat: -7.42851997638584, lng: 111.01776973992412, start: 730, end: 900 },
              { nama: "Kantor Desa Ngadiluwih, Matesih, Karanganyar", lat: -7.633272545502858, lng: 110.99996825526591, start: 600, end: 730 },
              { nama: "Lokasi Testing", lat: -7.716564379562363, lng: 110.59027731779902, start: 600, end: 730 },
              { nama: "Masjid Al Ikhlas Botok, Kerjo, Karanganyar", lat: -7.518997596395203, lng: 111.04124429999999, start: 600, end: 730 },
              { nama: "SMP Muhammadiyah 3 Karangpandan", lat: -7.6205906058938355, lng: 111.06234704232911, start: 600, end: 730 },
              { nama: "SMP Muhammadiyah 10 Surakarta", lat: -7.552680549665942, lng: 110.78133119965328, start: 600, end: 730 },
              { nama: "Masjid Yamp - Jumapolo, Karanganyar", lat: -7.7049863364494815, lng: 111.00101258835446, start: 600, end: 730 },
              { nama: "PPM Imam Syuhodo, Polokarto, Sukoharjo", lat: -7.622615604552016, lng: 110.89220351349366, start: 600, end: 730 },
              { nama: "Masjid Al Mukarromah, Karanganyar", lat: -7.599104240456491, lng: 110.95243712436272, start: 600, end: 730 },
              { nama: "MI Muhammadiyah Karanganyar", lat: -7.6032248341532735, lng: 110.95023672883546, start: 600, end: 730 },
              { nama: "SMK Muhammadiyah 1 Gondangrejo", lat: -7.473988689857501, lng: 110.8076632018481, start: 600, end: 730 },
              { nama: "SMP Muhammadiyah 9 Jaten", lat: -7.56493493777303, lng: 110.86863152827858, start: 600, end: 730 }
            ];

            var CURRENT_USER = null;
            var LIST_NAMA_DB = []; var LIST_AUM_DB = [];
            var CURRENT_PICKER_TYPE = "";
            var video = document.getElementById('camera');
            var latUser = 0, lngUser = 0, lokasiString = "", jarakUser = 0, namaLokasiTerdekat = "";
            var isAlreadyPresent = false, isTimeValid = false, isLocationValid = false;
            var gpsErrorMsg = "";
            var activeStartTime = 600;
            var activeEndTime = 730;

            // DATA GLOBAL UNTUK PDF
            var reportData = [];
            var currentDetailData = null;
            var currentDetailType = "";
            var userNBM = "";

            window.onload = function () {
              try {
                checkSession();
                loadDbOptions();
                setInterval(validateButtonState, 1000);
              } catch (e) { console.log(e); }
            };


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
                doc.save("Laporan_Presensi_" + CURRENT_USER.nama.replace(/\s+/g, '_') + ".pdf");
              } catch (e) {
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
                if(!globalRankingData) return;
                var globalTotalStr = document.getElementById('statCountText').innerText.split(" dari ")[1] || "1";
                var globalTotal = parseInt(globalTotalStr) || 1;
                var firstTime = Math.min(...globalRankingData.topUsers.map(u => u.firstTime));
                var titleStr = "Per Tanggal: " + formatTanggalIndoSimple(new Date()) + " (Total " + globalTotal + " Kegiatan sejak " + formatTanggalIndoSimple(firstTime) + ")";
                doc.text(titleStr, pageWidth / 2, 51, { align: "center" });
              var tableBody = globalRankingData.topUsers.map((item, index) => [
                  index + 1,
                  cleanString(item.nama),
                  cleanString(item.aum),
                  item.count + "x",
                  Math.round((item.count / globalTotal) * 100) + "%"
                ]);

                doc.autoTable({
                  startY: 60,
                  head: [['No', 'Nama Jamaah', 'Asal AUM', 'Hadir', 'Persentase']],
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
                if(!globalRankingData) return;
                var globalTotalStr = document.getElementById('statCountText').innerText.split(" dari ")[1] || "1";
                var globalTotal = parseInt(globalTotalStr) || 1;
                var firstTime = Math.min(...globalRankingData.topUsers.map(u => u.firstTime));
                var titleStr = "Per Tanggal: " + formatTanggalIndoSimple(new Date()) + " (Total " + globalTotal + " Kegiatan sejak " + formatTanggalIndoSimple(firstTime) + ")";
                doc.text(titleStr, pageWidth / 2, 51, { align: "center" });
              var tableBody = globalRankingData.topAums.map((item, index) => [
                  index + 1,
                  cleanString(item.aum),
                  item.count + "x",
                  item.memberList.length + " Org",
                  item.memberList.length > 0 ? cleanString(item.memberList[0].nama) : "-"
                ]);

                doc.autoTable({
                  startY: 60,
                  head: [['No', 'Nama AUM', 'Total Hadir', 'Jml Jamaah', 'Paling Aktif']],
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
                doc.text("Total AUM: " + globalRankingData.daftarAum.length, 15, 60);

                if(!globalRankingData) return;
              var tableBody = globalRankingData.daftarAum.map((item, index) => {
                var c = 0;
                var found = globalRankingData.topAums.find(a => cleanString(a.aum) === cleanString(item));
                if (found) c = found.memberList.length;
                return [
                  index + 1,
                  cleanString(item),
                  c + " Orang"
                ];
              });

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
                  doc.save("Detail_Jamaah_" + currentDetailData.nama.replace(/\s+/g, '_') + ".pdf");

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
                  doc.save("Detail_AUM_" + currentDetailData.aum.replace(/\s+/g, '_') + ".pdf");
                }
              } finally {
                btnCetak.innerHTML = originalHTML;
                btnCetak.disabled = false;
              }
            }

            function formatTanggalIndoSimple(dateInput) {
              if (!dateInput) return "";
              var d = new Date(dateInput);
              var bulanIndo = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"];
              return d.getDate() + " " + bulanIndo[d.getMonth()] + " " + d.getFullYear();
            }

            // --- SYSTEM FUNCTIONS ---
            function toggleMenu() {
              var menu = document.getElementById('mainMenu');
              var backdrop = document.getElementById('menuBackdrop');
              if (menu.classList.contains('show')) {
                menu.classList.remove('show');
                backdrop.classList.remove('show');
              } else {
                menu.classList.add('show');
                backdrop.classList.add('show');
              }
            }

            function openPicker(type) {
              CURRENT_PICKER_TYPE = type;
              document.getElementById('pickerTitle').innerText = (type === 'nama') ? "Pilih Nama" : "Pilih Asal AUM";
              document.getElementById('pickerSearch').value = "";
              renderPickerList("");
              document.getElementById('pickerModal').classList.remove('hidden');
            }
            function closePicker() { document.getElementById('pickerModal').classList.add('hidden'); }

            function renderPickerList(filter) {
              var container = document.getElementById('pickerListContainer'); container.innerHTML = "";
              var source = (CURRENT_PICKER_TYPE === 'nama') ? LIST_NAMA_DB : LIST_AUM_DB;
              var filtered = source.filter(item => item.toLowerCase().includes(filter.toLowerCase()));
              if (filtered.length === 0) { container.innerHTML = "<div class='text-center text-muted mt-3'>Tidak ditemukan</div>"; return; }
              filtered.forEach(item => {
                var div = document.createElement('div'); div.className = "picker-item";
                div.innerHTML = `<strong>${item}</strong>`; div.onclick = function () { selectPickerItem(item); };
                container.appendChild(div);
              });
            }
            function filterPicker() { renderPickerList(document.getElementById('pickerSearch').value); }
            function selectPickerItem(value) {
              if (CURRENT_PICKER_TYPE === 'nama') {
                document.getElementById('regNama').value = value;
                document.getElementById('textRegNama').innerText = value;
                document.getElementById('textRegNama').classList.remove('picker-placeholder');
                document.getElementById('textRegNama').classList.add('picker-value');
              } else {
                document.getElementById('regAum').value = value;
                document.getElementById('textRegAum').innerText = value;
                document.getElementById('textRegAum').classList.remove('picker-placeholder');
                document.getElementById('textRegAum').classList.add('picker-value');
              }
              closePicker();
            }

            function togglePassword(inputId, icon) {
              var input = document.getElementById(inputId);
              if (input.type === "password") { input.type = "text"; icon.classList.replace("bi-eye-slash", "bi-eye"); icon.classList.add("active"); }
              else { input.type = "password"; icon.classList.replace("bi-eye", "bi-eye-slash"); icon.classList.remove("active"); }
            }

            function validateUsername(input) {
              input.value = input.value.toLowerCase();
              var errorSpan = document.getElementById(input.id + 'Error');
              if (input.value.includes(" ")) { if (errorSpan) { errorSpan.classList.remove('hidden'); input.parentElement.classList.add('error'); } }
              else { if (errorSpan) { errorSpan.classList.add('hidden'); input.parentElement.classList.remove('error'); } }
            }

            function getNearestLocationName(lat, lng) {
              if (!lat || !lng) return "Lokasi Tidak Diketahui";
              var closestName = "Lokasi Tidak Diketahui"; var minDist = Infinity;
              DAFTAR_LOKASI.forEach(loc => { var d = calcDist(lat, lng, loc.lat, loc.lng); if (d < minDist) { minDist = d; closestName = loc.nama; } });
              return closestName;
            }

            function openInfoModal() { document.getElementById('infoModal').classList.remove('hidden'); }
            function closeInfoModal() { document.getElementById('infoModal').classList.add('hidden'); }

            async function openProfile() {
              loading(true);
              try {
                let req = await fetch(SCRIPT_URL, { method: 'POST', body: JSON.stringify({ action: 'getProfile', username: CURRENT_USER.username }) });
                let res = await req.json(); loading(false);
                if (res.status === 'success') {
                  var d = res.data;
                  // Simpan NBM untuk keperluan Report
                  userNBM = d.nbm || "-";

                  document.getElementById('profNama').value = d.nama;
                  var selAum = document.getElementById('profAum'); selAum.innerHTML = "";
                  LIST_AUM_DB.forEach(a => { var opt = document.createElement('option'); opt.value = a; opt.text = a; if (a == d.aum) opt.selected = true; selAum.add(opt); });
                  document.getElementById('profJk').value = d.jk; document.getElementById('profNbm').value = d.nbm;
                  document.getElementById('profAlamat').value = d.alamat; document.getElementById('profTempat').value = d.tempat_lahir;
                  document.getElementById('profTgl').value = d.tgl_lahir; document.getElementById('profEmail').value = d.email;
                  document.getElementById('profHp').value = d.hp;
                  document.getElementById('homeScreen').classList.add('hidden'); document.getElementById('profileScreen').classList.remove('hidden');
                } else { alert(res.message); }
              } catch (e) { loading(false); alert("Gagal: " + e); }
            }

            function closeProfile() { document.getElementById('profileScreen').classList.add('hidden'); document.getElementById('homeScreen').classList.remove('hidden'); }

            async function saveProfile() {
              var data = { username: CURRENT_USER.username, nama: document.getElementById('profNama').value, aum: document.getElementById('profAum').value, jk: document.getElementById('profJk').value, nbm: document.getElementById('profNbm').value, alamat: document.getElementById('profAlamat').value, tempat_lahir: document.getElementById('profTempat').value, tgl_lahir: document.getElementById('profTgl').value, email: document.getElementById('profEmail').value, hp: document.getElementById('profHp').value };
              loading(true);
              try {
                let req = await fetch(SCRIPT_URL, { method: 'POST', body: JSON.stringify({ action: 'updateProfile', data: data }) });
                let res = await req.json(); loading(false); alert(res.message);
                if (res.status === 'success') {
                  CURRENT_USER.nama = data.nama; CURRENT_USER.aum = data.aum;
                  userNBM = data.nbm; // Update NBM lokal juga
                  localStorage.setItem("PCM_USER", JSON.stringify(CURRENT_USER));
                  document.getElementById('dashGreetingName').innerText = data.nama.toLowerCase(); document.getElementById('dashGreetingAum').innerText = data.aum || "-";
                  closeProfile();
                }
              } catch (e) { loading(false); alert(e); }
            }

            function openChangePassword() { document.getElementById('homeScreen').classList.add('hidden'); document.getElementById('passwordScreen').classList.remove('hidden'); }
            function closeChangePassword() { document.getElementById('passwordScreen').classList.add('hidden'); document.getElementById('homeScreen').classList.remove('hidden'); }

            async function savePassword() {
              var p1 = document.getElementById('passNew').value; var p2 = document.getElementById('passConfirm').value;
              if (!p1 || p1 !== p2) return alert("Password tidak cocok / kosong");
              loading(true);
              try {
                let req = await fetch(SCRIPT_URL, { method: 'POST', body: JSON.stringify({ action: 'changePassword', data: { username: CURRENT_USER.username, newPass: p1 } }) });
                let res = await req.json(); loading(false); alert(res.message); if (res.status === 'success') { closeChangePassword(); doLogout(); }
              } catch (e) { loading(false); alert(e); }
            }

            function validateButtonState() {
              if (!CURRENT_USER) return;
              var now = new Date(); var day = now.getDay(); var h = now.getHours(); var m = now.getMinutes(); var timeVal = h * 100 + m;

              if (day === 0 && timeVal >= activeStartTime && timeVal <= activeEndTime) {
                isTimeValid = true;
              } else {
                isTimeValid = false;
              }

              var formatTime = (num) => {
                var s = num.toString().padStart(3, '0');
                if (num < 1000) s = "0" + num;
                return s.substring(0, 2) + ":" + s.substring(2);
              };

              var btn = document.getElementById('btnStartAbsen'); var msg = document.getElementById('dashboardMsg');
              btn.classList.remove('btn-primary', 'btn-secondary'); btn.classList.remove('btn-danger'); msg.style.display = 'none'; msg.className = "";

              if (isAlreadyPresent) {
                btn.disabled = true; btn.innerHTML = "<i class='bi bi-check2-circle'></i> SUDAH PRESENSI"; btn.classList.add('btn-secondary');
              }
              else if (!isTimeValid) {
                btn.disabled = true; btn.innerHTML = "<i class='bi bi-clock-history'></i> PRESENSI DITUTUP"; btn.classList.add('btn-secondary');
                msg.innerHTML = `<b>Jadwal Kajian Di Sini:</b><br>Ahad ${formatTime(activeStartTime)} - ${formatTime(activeEndTime)} WIB.`;
                msg.style.display = 'block';
              }
              else if (gpsErrorMsg !== "") {
                btn.disabled = true; btn.innerHTML = "<i class='bi bi-geo-alt'></i> AKTIFKAN GPS"; btn.classList.add('btn-secondary'); msg.innerHTML = `<i class="bi bi-exclamation-triangle"></i> <b>${gpsErrorMsg}</b><br>Mohon aktifkan lokasi.`; msg.style.display = 'block'; msg.classList.add('msg-danger');
              }
              else if (latUser === 0 && lngUser === 0) {
                btn.disabled = true; btn.innerHTML = "<div class='spinner-border spinner-border-sm'></div> Mencari GPS..."; btn.classList.add('btn-secondary');
              }
              else if (!isLocationValid) {
                btn.disabled = true; btn.innerHTML = "<i class='bi bi-geo-alt'></i> LOKASI TIDAK SESUAI"; btn.classList.add('btn-secondary'); msg.innerHTML = "<b>Anda jauh dari lokasi kajian.</b><br>Silakan mendekat."; msg.style.display = 'block';
              }
              else {
                btn.disabled = false; btn.innerHTML = '<i class="bi bi-fingerprint" style="font-size:1.2rem;"></i> PRESENSI KAJIAN'; btn.classList.add('btn-primary');
              }
            }


            function cleanString(str) {
              if (!str) return "";
              let s = str.trim();
              s = s.replace(/^[`'"]+/, ''); // strip leading quotes
              s = s.replace(/\s+/g, ' '); // collapse spaces
              
              let stripped = s.replace(/[^a-zA-Z0-9]/g, '').toLowerCase();
              
              if (stripped.includes('tkaisyiyahkebak')) return 'TK Aisyiyah Kebak';
              if (stripped.includes('kbaisyiyahwaru')) return 'KB Aisyiyah Waru';
              if (stripped.includes('mimkaliwuluh')) return 'MIM Kaliwuluh';
              
              return s.trim();
            }

            async function loadDashboardData() {
              var start = document.getElementById('filterStart').value;
              var end = document.getElementById('filterEnd').value;
              try {
                let req = await fetch(SCRIPT_URL, { method: 'POST', body: JSON.stringify({ action: 'getReport', nama: CURRENT_USER.nama, start: start, end: end }) });
                let res = await req.json();
                if (CURRENT_USER && CURRENT_USER.nama) {
                  document.getElementById('dashGreetingName').innerText = CURRENT_USER.nama.toLowerCase();
                  document.getElementById('dashGreetingAum').innerText = CURRENT_USER.aum || "-";

                  let hour = new Date().getHours();
                  let timeG = "Semangat Malam";
                  if (hour < 10) timeG = "Semangat Pagi";
                  else if (hour < 15) timeG = "Semangat Siang";
                  else if (hour < 18) timeG = "Semangat Sore";
                  document.getElementById('dashGreetingTime').innerText = "Assalamu'alaikum, " + timeG;
                }

                document.getElementById('dashLastDate').innerText = res.lastPresensi;

                if (res.stats) {
                  document.getElementById('statCountText').innerText = res.stats.userTotal + " dari " + res.stats.globalTotal;
                  document.getElementById('statPercentText').innerText = res.stats.percent + "%";

                  setTimeout(() => { document.getElementById('statProgressBar').style.width = res.stats.percent + "%"; }, 100);

                  let streakText = "Yuk rajin ikut kajian!";
                  if (res.stats.percent >= 80) streakText = "Istiqomah: Sangat Aktif";
                  else if (res.stats.percent >= 50) streakText = "Terus Tingkatkan Kehadiran";
                  document.getElementById('dashStreak').innerHTML = `<i class="bi bi-fire text-warning"></i> <span>${streakText}</span>`;

                  let badgeIcon = "🥉"; let badgeTitle = "Pencari Ilmu"; let badgeDesc = "Langkah awal yang baik, terus tingkatkan!";
                  if (res.stats.percent >= 75) { badgeIcon = "💎"; badgeTitle = "Teladan Istiqomah"; badgeDesc = "MasyaAllah, Anda adalah teladan dalam memakmurkan majelis ilmu!"; }
                  else if (res.stats.percent >= 50) { badgeIcon = "🥇"; badgeTitle = "Aktivis Dakwah"; badgeDesc = "Luar biasa! Separuh perjalanan telah dilalui dengan istiqomah."; }
                  else if (res.stats.percent >= 25) { badgeIcon = "🥈"; badgeTitle = "Penggiat Kajian"; badgeDesc = "Anda semakin konsisten menuntut ilmu."; }

                  let lencanaEl = document.getElementById('dashBadgeLencana');
                  if (lencanaEl) { lencanaEl.innerText = badgeIcon; lencanaEl.style.display = "inline-block"; }

                  let modalIcon = document.getElementById('badgeModalIcon');
                  if (modalIcon) {
                    modalIcon.innerText = badgeIcon;
                    document.getElementById('badgeModalTitle').innerText = badgeTitle;
                    document.getElementById('badgeModalDesc').innerText = badgeDesc;
                  }
                }

                // SIMPAN DATA UNTUK PDF
                reportData = res.history;

                checkTodayStatus(res.history); renderHistory(res.history);

                // Background load user details for NBM
                if (!userNBM) {
                  fetch(SCRIPT_URL, { method: 'POST', body: JSON.stringify({ action: 'getProfile', username: CURRENT_USER.username }) })
                    .then(r => r.json()).then(d => { if (d.status === 'success') userNBM = d.data.nbm; });
                }

                // Muat Data Ranking di Latar Belakang
                loadRankingData();

              } catch (e) { }
            }

            let globalRankingData = null;

            async function loadRankingData() {
              try {
                let req = await fetch(SCRIPT_URL, { method: 'POST', body: JSON.stringify({ action: 'getRanking' }) });
                let res = await req.json();
                if (res.status === 'success') {
                  globalRankingData = res.data;
                  renderPalingAktif(res.data.topUsers);
                  renderAumTeraktif(res.data.topAums);
                  renderDaftarAum(res.data.daftarAum);
                }
              } catch (e) {
                console.error("Gagal memuat ranking:", e);
              }
            }

            function renderPalingAktif(users) {
              let c = document.getElementById('listPalingAktif');
              if (users.length === 0) { c.innerHTML = "<div class='text-center small text-muted py-3'>Belum ada data.</div>"; return; }
              let html = "";
              users.forEach((u, i) => {
                let medal = "";
                if (i === 0) medal = "🥇"; else if (i === 1) medal = "🥈"; else if (i === 2) medal = "🥉"; else medal = `<span style="display:inline-block; width:24px; text-align:center; font-weight:bold; color:#64748b;">${i + 1}</span>`;
                html += `<div class="list-group-item d-flex justify-content-between align-items-center" style="border-radius:12px; margin-bottom:8px; border:1px solid #e2e8f0; border-left:4px solid ${i < 3 ? 'var(--primary)' : '#cbd5e1'};">
              <div class="d-flex align-items-center gap-3">
                  <div style="font-size:1.3rem;">${medal}</div>
                  <div><div class="fw-bold text-dark text-capitalize">${u.nama.toLowerCase()}</div><div class="small text-muted" style="font-size:0.75rem;"><i class="bi bi-geo-alt-fill"></i> ${u.aum}</div></div>
              </div>
              <div class="badge bg-primary rounded-pill px-3 py-2" style="cursor:pointer;" onclick="showUserDetail(${i})">${u.count}x <i class="bi bi-chevron-right ms-1"></i></div>
          </div>`;
              });
              c.innerHTML = html;
            }

            function renderAumTeraktif(aums) {
              let c = document.getElementById('listAumTeraktif');
              if (aums.length === 0) { c.innerHTML = "<div class='text-center small text-muted py-3'>Belum ada data.</div>"; return; }
              let html = "";
              aums.forEach((a, i) => {
                let medal = "";
                if (i === 0) medal = "🏆"; else if (i === 1) medal = "🥈"; else if (i === 2) medal = "🥉"; else medal = `<span style="display:inline-block; width:24px; text-align:center; font-weight:bold; color:#64748b;">${i + 1}</span>`;
                html += `<div class="list-group-item d-flex justify-content-between align-items-center" style="border-radius:12px; margin-bottom:8px; border:1px solid #e2e8f0;">
              <div class="d-flex align-items-center gap-3">
                  <div style="font-size:1.3rem;">${medal}</div>
                  <div>
                      <div class="fw-bold text-dark">${a.aum}</div>
                      <div class="small text-muted" style="font-size:0.75rem;"><i class="bi bi-people-fill text-info"></i> ${a.memberList ? a.memberList.length : 0} Jamaah</div>
                  </div>
              </div>
              <div class="badge bg-success rounded-pill px-3 py-2" style="cursor:pointer;" onclick="showAumDetail(${i})">${a.count}x <i class="bi bi-chevron-right ms-1"></i></div>
          </div>`;
              });
              c.innerHTML = html;
            }

                        function showUserDetailByName(nama) {
              if (!globalRankingData) return;
              let idx = globalRankingData.topUsers.findIndex(u => cleanString(u.nama) === cleanString(nama));
              if (idx !== -1) {
                showUserDetail(idx);
              } else {
                alert("Detail riwayat lengkap untuk jamaah ini belum termuat di memori utama (bukan Top 20).");
              }
            }

            function showUserDetail(index) {
              if (!globalRankingData) return;
              let user = globalRankingData.topUsers[index];
              if (!user) return;

                            document.getElementById('detailTitle').innerText = cleanString(user.nama);
              
              currentDetailType = 'user';
              currentDetailData = {
                  nama: cleanString(user.nama),
                  aum: cleanString(user.aum),
                  total: user.count,
                  history: user.history.map(h => ({
                      tanggal: h.tglStr,
                      jam: h.waktu,
                      lokasi: h.lokasi
                  }))
              };
              let c = document.getElementById('listDetail');

              if (!user.history || user.history.length === 0) {
                c.innerHTML = "<div class='text-center small text-muted py-3'>Detail belum tersedia. Silakan update Backend GAS Anda.</div>";
              } else {
                // Urutkan riwayat dari yang paling baru
                if (user.history.length > 0 && typeof user.history[0] === 'object') {
                  user.history.sort((a, b) => b.tglRaw - a.tglRaw);
                }

                let html = `<div class="alert alert-light border small text-center mb-3">
           Total Kehadiran: <strong>${user.count}x</strong><br>
           <span class="text-muted" style="font-size:0.75rem;"><i class="bi bi-building"></i> ${user.aum}</span>
        </div>`;
                user.history.forEach(item => {
                  if (typeof item === 'string') {
                    html += `<div class="list-group-item py-2" style="border-radius:8px; margin-bottom:4px; font-size:0.85rem;">
                <i class="bi bi-calendar-check me-2 text-primary"></i> ${item}
              </div>`;
                  } else {
                    html += `<div class="list-group-item py-2" style="border-radius:8px; margin-bottom:4px; font-size:0.85rem;">
                <div class="fw-bold text-dark"><i class="bi bi-calendar-check me-1 text-primary"></i> ${item.tglStr}</div>
                <div class="text-muted" style="font-size:0.75rem; margin-top:2px;"><i class="bi bi-clock me-1 text-warning"></i> ${item.waktu}</div>
                <div class="text-muted text-truncate" style="font-size:0.75rem; margin-top:2px;"><i class="bi bi-geo-alt-fill me-1 text-danger"></i> ${item.lokasi}</div>
              </div>`;
                  }
                });
                c.innerHTML = html;
              }

              document.getElementById('detailScreen').classList.remove('hidden');
            }

            
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

            function showAumDetail(index) {
              if (!globalRankingData) return;
              let aum = globalRankingData.topAums[index];
              if (!aum) return;

                            document.getElementById('detailTitle').innerText = "Detail AUM: " + cleanString(aum.aum);
              
              currentDetailType = 'aum';
              currentDetailData = {
                  aum: cleanString(aum.aum),
                  totalHadir: aum.count,
                  jamaahList: aum.memberList.map(m => ({
                      nama: cleanString(m.nama),
                      hadir: m.count
                  }))
              };
              let c = document.getElementById('listDetail');

              if (!aum.memberList || aum.memberList.length === 0) {
                c.innerHTML = "<div class='text-center small text-muted py-3'>Detail belum tersedia. Silakan update Backend GAS Anda.</div>";
              } else {
                let html = `<div class="alert alert-light border small text-center mb-3">
            Total Kehadiran Jamaah: <strong>${aum.count}x</strong><br>
            Jumlah Anggota Aktif: <strong>${aum.memberList.length}</strong> Orang
        </div>`;
                aum.memberList.forEach((m, idx) => {
                  html += `<div class="list-group-item d-flex justify-content-between align-items-center py-2" style="border-radius:8px; margin-bottom:4px; font-size:0.85rem;">
                <div class="text-truncate" style="max-width:75%;"><span class="fw-bold me-2" style="color:#64748b;">${idx + 1}.</span> <span class="text-capitalize">${m.nama.toLowerCase()}</span></div>
                <div class="badge bg-primary rounded-pill" style="cursor:pointer;" onclick="fetchAndShowUserDetail('${m.nama.replace(/'/g, "\'")}', this)">${m.count}x <i class="bi bi-chevron-right ms-1"></i></div>
              </div>`;
                });
                c.innerHTML = html;
              }

              document.getElementById('detailScreen').classList.remove('hidden');
            }

            function renderDaftarAum(daftar) {
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
            }

            let historyPage = 1;
            const historyPerPage = 5;
            let currentHistoryList = [];

            function checkTodayStatus(history) {
              var today = new Date(); isAlreadyPresent = false;
              if (history.length > 0) {
                var lastRaw = new Date(history[0].tanggalRaw);
                if (lastRaw.getDate() === today.getDate() && lastRaw.getMonth() === today.getMonth() && lastRaw.getFullYear() === today.getFullYear()) isAlreadyPresent = true;
              }
              validateButtonState();
            }

            function renderHistory(list) {
              currentHistoryList = list;
              historyPage = 1;
              displayHistoryPage();
            }

            function displayHistoryPage() {
              var c = document.getElementById('historyList'); c.innerHTML = "";
              var pagination = document.getElementById('historyPagination');
              if (currentHistoryList.length === 0) {
                c.innerHTML = "<div class='text-center small text-muted'>Belum ada riwayat.</div>";
                pagination.style.setProperty("display", "none", "important");
                return;
              }

              var startIdx = (historyPage - 1) * historyPerPage;
              var endIdx = Math.min(startIdx + historyPerPage, currentHistoryList.length);
              var pageList = currentHistoryList.slice(startIdx, endIdx);

              pageList.forEach(i => {
                var displayName = i.lokasi;
                var coordsMatch = i.lokasi.match(/(-?\d+\.\d+),\s*(-?\d+\.\d+)/);
                if (coordsMatch && coordsMatch.length === 3) { displayName = getNearestLocationName(parseFloat(coordsMatch[1]), parseFloat(coordsMatch[2])); }
                else { if (displayName.includes('(')) displayName = displayName.split('(')[0].trim(); }
                var html = `<div class="history-item"><div><div class="hist-date">${i.tanggal}</div><div class="hist-loc"><i class="bi bi-geo-alt-fill"></i> ${displayName}</div></div><div class="badge bg-light text-dark border">${i.jam}</div></div>`;
                c.innerHTML += html;
              });

              var totalPages = Math.ceil(currentHistoryList.length / historyPerPage);
              if (totalPages > 1) {
                pagination.style.setProperty("display", "flex", "important");
                document.getElementById('historyPageInfo').innerText = "Hal " + historyPage + " dari " + totalPages;
                document.getElementById('btnPrevHistory').disabled = (historyPage === 1);
                document.getElementById('btnNextHistory').disabled = (historyPage === totalPages);
              } else {
                pagination.style.setProperty("display", "none", "important");
              }
            }

            function changeHistoryPage(dir) {
              historyPage += dir;
              displayHistoryPage();
            }

            function formatTanggalIndoJS(d) {
              var h = ["Ahad", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]; var b = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"];
              return h[d.getDay()] + ", " + d.getDate() + " " + b[d.getMonth()] + " " + d.getFullYear();
            }

            async function doLogin() {
              var u = document.getElementById('loginUser').value; var p = document.getElementById('loginPass').value;
              if (!u || !p) return alert("Isi data");
              if (u.includes(" ")) return alert("Username tidak boleh ada spasi");
              loading(true);
              try {
                let req = await fetch(SCRIPT_URL, { method: 'POST', body: JSON.stringify({ action: 'login', data: { username: u, password: p } }) });
                let res = await req.json(); loading(false);
                if (res.status === 'success') {
                  CURRENT_USER = { username: res.username, nama: res.nama, aum: res.aum, role: res.role };
                  localStorage.setItem("PCM_USER", JSON.stringify(CURRENT_USER)); showDashboard();
                  if (navigator.geolocation) navigator.geolocation.watchPosition(updatePosisi, handleGpsError, { enableHighAccuracy: true });
                } else alert(res.message);
              } catch (e) { loading(false); alert(e); }
            }

            async function doRegister() {
              var n = document.getElementById('regNama').value; var a = document.getElementById('regAum').value; var u = document.getElementById('regUser').value; var p = document.getElementById('regPass').value;
              if (!n || !a || !u || !p) return alert("Lengkapi data");
              if (u.includes(" ")) return alert("Username tidak boleh ada spasi");
              loading(true);
              try {
                let req = await fetch(SCRIPT_URL, { method: 'POST', body: JSON.stringify({ action: 'register', data: { username: u, password: p, nama: n, aum: a } }) });
                let res = await req.json(); loading(false); alert(res.message); if (res.status === 'success') showLogin();
              } catch (e) { loading(false); alert(e); }
            }

            async function kirimAbsen() {
              var kes = document.getElementById('kesimpulan').value; if (!kes) return alert("Isi kesimpulan");
              loading(true);
              var cvs = document.getElementById('canvas'); cvs.width = video.videoWidth; cvs.height = video.videoHeight;
              var ctx = cvs.getContext('2d'); ctx.save(); ctx.translate(cvs.width, 0); ctx.scale(-1, 1); ctx.drawImage(video, 0, 0); ctx.restore();
              var d = new Date(); var dateStr = formatTanggalIndoJS(d); var timeStr = d.toLocaleTimeString('id-ID', { hour12: false }) + " WIB";
              ctx.fillStyle = "rgba(0,0,0,0.5)"; ctx.fillRect(0, cvs.height - 80, cvs.width, 80);
              ctx.font = "bold 16px sans-serif"; ctx.fillStyle = "white";
              ctx.fillText(dateStr + " " + timeStr, 20, cvs.height - 50); ctx.fillText(namaLokasiTerdekat + " (" + jarakUser + "m)", 20, cvs.height - 25);
              var base64 = cvs.toDataURL("image/png").replace(/^data:image\/(png|jpg);base64,/, "");
              try {
                let req = await fetch(SCRIPT_URL, { method: 'POST', body: JSON.stringify({ action: 'savePresensi', data: { nama: CURRENT_USER.nama, aum: CURRENT_USER.aum, kegiatan: "Pengajian - " + dateStr, kesimpulan: kes, lokasiString: lokasiString, lat: latUser, lng: lngUser, image: base64 } }) });
                let res = await req.json(); loading(false); alert(res.message); if (res.status === 'success') { closePresensiMode(); loadDashboardData(); }
              } catch (e) { loading(false); alert(e); }
            }

            function checkSession() { var stored = localStorage.getItem("PCM_USER"); if (stored) { CURRENT_USER = JSON.parse(stored); showDashboard(); } else showLogin(); }
            function showLogin() {
              document.getElementById('authScreen').classList.remove('hidden');
              document.getElementById('homeScreen').classList.add('hidden');
              document.getElementById('formLogin').classList.remove('hidden');
              document.getElementById('formRegister').classList.add('hidden');
            }
            function showRegister() { document.getElementById('formLogin').classList.add('hidden'); document.getElementById('formRegister').classList.remove('hidden'); }

            function showDashboard() {
              document.getElementById('authScreen').classList.add('hidden');
              document.getElementById('homeScreen').classList.remove('hidden');
              document.getElementById('dashGreetingName').innerText = CURRENT_USER.nama.toLowerCase();
              document.getElementById('dashGreetingAum').innerText = CURRENT_USER.aum || "-";
              renderMenu();
              loadDashboardData();
              if (navigator.geolocation) navigator.geolocation.watchPosition(updatePosisi, handleGpsError, { enableHighAccuracy: true });
            }

            function renderMenu() {
              var role = CURRENT_USER.role || 'karyawan';
              var menuHTML = '';

              menuHTML += `
    <li class="menu-item" onclick="openProfile(); toggleMenu()">
        <div class="menu-icon"><i class="bi bi-person-circle"></i></div>
        <div class="menu-text">Profil Saya</div><i class="bi bi-chevron-right menu-chevron"></i>
    </li>
    <li class="menu-item" onclick="openChangePassword(); toggleMenu()">
        <div class="menu-icon"><i class="bi bi-key-fill"></i></div>
        <div class="menu-text">Ganti Password</div><i class="bi bi-chevron-right menu-chevron"></i>
    </li>`;

              if (role === 'admin') {
                menuHTML += `
        <li class="menu-item" onclick="window.location.href='admin.html'">
            <div class="menu-icon" style="background:#dbeafe; color:#1e40af"><i class="bi bi-calendar-plus-fill"></i></div>
            <div class="menu-text">Kelola Jadwal</div><i class="bi bi-chevron-right menu-chevron"></i>
        </li>
        <li class="menu-item" onclick="window.location.href='presensi.html'">
            <div class="menu-icon" style="background:#dcfce7; color:#15803d"><i class="bi bi-camera-fill"></i></div>
            <div class="menu-text">Presensi Kegiatan</div><i class="bi bi-chevron-right menu-chevron"></i>
        </li>`;
              }

              if (role === 'pengurus') {
                menuHTML += `
        <li class="menu-item" onclick="window.location.href='presensi.html'">
            <div class="menu-icon" style="background:#fce7f3; color:#9d174d"><i class="bi bi-camera-fill"></i></div>
            <div class="menu-text">Presensi Kegiatan</div><i class="bi bi-chevron-right menu-chevron"></i>
        </li>`;
              }

              menuHTML += `
    <li class="menu-item" onclick="openInfoModal(); toggleMenu()">
        <div class="menu-icon"><i class="bi bi-question-circle-fill"></i></div>
        <div class="menu-text">Panduan & Instalasi</div><i class="bi bi-chevron-right menu-chevron"></i>
    </li>
    <li class="menu-item logout" onclick="doLogout()">
        <div class="menu-icon"><i class="bi bi-box-arrow-right"></i></div>
        <div class="menu-text">Keluar Aplikasi</div>
    </li>`;

              document.getElementById('menuListContainer').innerHTML = menuHTML;
            }

            function doLogout() { localStorage.removeItem("PCM_USER"); CURRENT_USER = null; showLogin(); }
            function openPresensiMode() { document.getElementById('homeScreen').classList.add('hidden'); document.getElementById('presensiScreen').classList.remove('hidden'); if (navigator.mediaDevices) navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" } }).then(s => video.srcObject = s); if (navigator.geolocation) navigator.geolocation.watchPosition(updatePosisi, handleGpsError, { enableHighAccuracy: true }); }
            function closePresensiMode() { if (video.srcObject) video.srcObject.getTracks().forEach(t => t.stop()); document.getElementById('presensiScreen').classList.add('hidden'); document.getElementById('homeScreen').classList.remove('hidden'); }

            async function loadDbOptions() {
              try {
                let r = await fetch(SCRIPT_URL, { method: 'POST', body: JSON.stringify({ action: 'getOptions' }) });
                let d = await r.json();
                if (d.status === 'success') {
                  LIST_NAMA_DB = d.nama; LIST_AUM_DB = d.aum;
                }
              } catch (e) { }
            }

            function handleGpsError(err) {
              console.warn('GPS Error:', err.code);
              if (err.code == 1) gpsErrorMsg = "Izin Lokasi Ditolak.";
              else if (err.code == 2) gpsErrorMsg = "GPS Mati / Tidak Terdeteksi.";
              else if (err.code == 3) gpsErrorMsg = "Waktu Habis Mencari GPS.";
              else gpsErrorMsg = "Error GPS Tidak Diketahui.";
              isLocationValid = false; latUser = 0; lngUser = 0;
              validateButtonState();
            }

            function updatePosisi(pos) {
              gpsErrorMsg = "";
              latUser = pos.coords.latitude; lngUser = pos.coords.longitude; lokasiString = latUser + "," + lngUser;

              var closest = Infinity, locObj = null;

              DAFTAR_LOKASI.forEach(l => {
                var d = calcDist(latUser, lngUser, l.lat, l.lng);
                if (d < closest) { closest = d; locObj = l; }
              });

              jarakUser = Math.round(closest);

              if (locObj) {
                namaLokasiTerdekat = locObj.nama;
                activeStartTime = locObj.start;
                activeEndTime = locObj.end;
              }

              isLocationValid = (jarakUser <= MAX_RADIUS);

              var statBox = document.getElementById('statusLokasiBox'); var btnKirim = document.getElementById('btnKirim');

              if (isLocationValid) {
                btnKirim.disabled = false;
                statBox.className = "alert alert-success py-2 small mb-3";
                statBox.innerHTML = `<i class="bi bi-geo-alt-fill"></i> ${namaLokasiTerdekat} (${jarakUser}m)`;
              } else {
                btnKirim.disabled = true;
                statBox.className = "alert alert-danger py-2 small mb-3";
                statBox.innerHTML = `<i class="bi bi-x-circle"></i> Kejauhan: ${jarakUser}m`;
              }

              validateButtonState();
            }
            function calcDist(lat1, lon1, lat2, lon2) { var R = 6371000, dLat = (lat2 - lat1) * Math.PI / 180, dLon = (lon2 - lon1) * Math.PI / 180; var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * Math.sin(dLon / 2) * Math.sin(dLon / 2); return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a)); }
            function loading(show) { document.getElementById('loading').classList.toggle('hidden', !show); }

            function openBadgeInfo() { openFeatureModal('badgeInfoScreen'); }
            function openFeatureModal(id) {
              document.getElementById('homeScreen').classList.add('hidden');
              document.getElementById(id).classList.remove('hidden');
            }
            function closeFeatureModal(id) {
              document.getElementById(id).classList.add('hidden');
              document.getElementById('homeScreen').classList.remove('hidden');
            }
          