```javascript
// --- KONFIGURASI ---
var FOLDER_ID = '1KLD3DbL6UpPMyuUOpcLLl9DxKGR4PJoD'; 
var SHEET_PRESENSI = 'Sheet1'; 
var SHEET_DATA = 'DataAnggota';
var SHEET_AKUN = 'DataAkun'; 
var RADIUS_METER = 500; 

var DAFTAR_LOKASI = [
   { nama: "Masjid Abdul Aziz (SMP Muhammadiyah 8 Kebakkramat)", lat: -7.520470615403366, lng: 110.9065007512984 },
    { nama: "Gedung Dakwah PDM Karanganyar", lat: -7.586223863399417, lng: 110.91830297060768 },
    { nama: "Masjid Al Mukarromah, Karanganyar", lat: -7.5991158597467505, lng: 110.95277542273423 },
    { nama: "SMP Muhammadiyah 2 Karanganyar", lat: -7.59240065605104, lng: 110.95609234835774 },
    { nama: "Masjid Raya Al Falah Sragen", lat: -7.42851997638584, lng: 111.01776973992412 },
    { nama: "Kantor Desa Ngadiluwih, Matesih, Karanganyar", lat: -7.633272545502858, lng: 110.99996825526591 },
    { nama: "Lokasi Testing", lat: -7.716564379562363, lng: 110.59027731779902 },
    // LOKASI BARU
    { nama: "Catering Pandu", lat: -7.500030621538215, lng: 110.90614961162527 },
    { nama: "Hapsari Handayani", lat: -7.5137745006634935, lng: 110.912900811742 },
    //tambah lokasi baru , , 
    { nama: "Masjid Al Ikhlas Botok, Kerjo, Karanganyar", lat: -7.518997596395203, lng: 111.04124429999999 },
    { nama: "SMP Muhammadiyah 3 Karangpandan", lat: -7.6205906058938355, lng: 111.06234704232911 },
    { nama: "SMP Muhammadiyah 10 Surakarta", lat: -7.552680549665942, lng: 110.78133119965328 },
    { nama: "Masjid Yamp - Jumapolo, Karanganyar", lat: -7.7049863364494815, lng: 111.00101258835446},
    { nama: "PPM Imam Syuhodo, Polokarto, Sukoharjo", lat: -7.622615604552016, lng: 110.89220351349366},
    { nama: "Masjid Al Mukarromah, Karanganyar", lat: -7.599104240456491, lng: 110.95243712436272},
    { nama: "MI Muhammadiyah Karanganyar", lat: -7.6032248341532735, lng: 110.95023672883546, start: 600, end: 730},
    { nama: "SMK Muhammadiyah 1 Gondangrejo", lat: -7.473988689857501, lng: 110.8076632018481, start: 600, end: 730},
    { nama: "SMP Muhammadiyah 9 Jaten", lat: -7.56493493777303, lng: 110.86863152827858, start: 600, end: 730} 
];

// --- UPDATE FUNGSI doGet (ROUTING HALAMAN) ---
function doGet(e) {
  var page = e.parameter.page;
  
  if (page == 'admin') {
    return HtmlService.createTemplateFromFile('admin').evaluate()
      .setTitle("Admin & Pengurus PCM")
      .addMetaTag('viewport', 'width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0');
  } else {
    return HtmlService.createTemplateFromFile('index').evaluate()
      .setTitle("Presensi Kajian AUM")
      .addMetaTag('viewport', 'width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0');
  }
}

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.tryLock(10000); 
  try {
    var params = JSON.parse(e.postData.contents);
    var action = params.action;
    var result = {};
    if (action === 'getOptions') result = getDataOptions();
    else if (action === 'register') result = doRegister(params.data);
    else if (action === 'login') result = doLogin(params.data);
    else if (action === 'savePresensi') result = processForm(params.data);
    else if (action === 'getReport') result = getRiwayat(params.nama, params.start, params.end, params.limit);
    else if (action === 'getProfile') result = getUserProfile(params.username);
    else if (action === 'updateProfile') result = updateUserProfile(params.data);
    else if (action === 'changePassword') result = changePassword(params.data);
    else if (action === 'getRanking') result = getRankingData();
    else if (['getEvents', 'saveEvent', 'updateEvent', 'deleteEvent', 'submitEventPresence'].includes(action)) {
      result = processEventRequest(params);
    }
    
    return responseJSON(result);
  } catch (err) { return responseJSON({ status: 'error', message: err.toString() }); } 
  finally { lock.releaseLock(); }
}

function responseJSON(data) { return ContentService.createTextOutput(JSON.stringify(data)).setMimeType(ContentService.MimeType.JSON); }

// --- UPDATE REGISTER (DEFAULT ROLE KARYAWAN) ---
function doRegister(data) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(SHEET_AKUN);
  var dataAkun = sheet.getDataRange().getValues();
  var inputUser = String(data.username).toLowerCase().trim();
  if (inputUser.indexOf(" ") >= 0) return { status: 'error', message: 'Username tidak boleh mengandung spasi!' };

  for(var i=1; i<dataAkun.length; i++) {
    var dbUser = String(dataAkun[i][0]).toLowerCase().trim();
    if(dbUser == inputUser) return { status: 'error', message: 'Username sudah digunakan!' };
    if(dataAkun[i][2] == data.nama) return { status: 'error', message: 'Nama ini sudah terdaftar!' };
  }
  
  // Tambah 'karyawan' di kolom terakhir (Role)
  sheet.appendRow(["'" + inputUser, "'" + data.password, data.nama, data.aum, "", "", "", "", "", "", "", "karyawan"]);
  return { status: 'success', message: 'Registrasi Berhasil! Silakan Login.' };
}

// --- UPDATE DO LOGIN (AMBIL ROLE) ---
function doLogin(data) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_AKUN);
  var rows = sheet.getDataRange().getValues();
  var inputUser = String(data.username).toLowerCase().trim();
  var inputPass = String(data.password); // Password case sensitive

  for(var i=1; i<rows.length; i++) {
    var dbUser = String(rows[i][0]).toLowerCase().trim();
    var dbPass = String(rows[i][1]);

    if(dbUser == inputUser && dbPass == inputPass) {
      // Ambil Role di Kolom L (Index 11) -> Default 'karyawan' jika kosong
      var role = rows[i][11] ? String(rows[i][11]).toLowerCase() : 'karyawan';
      
      return { 
        status: 'success', 
        username: dbUser, 
        nama: rows[i][2], 
        aum: rows[i][3],
        role: role // Kirim Role ke Frontend
      };
    }
  }
  return { status: 'error', message: 'Username atau Password salah!' };
}

function getUserProfile(username) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_AKUN);
  var rows = sheet.getDataRange().getValues();
  var targetUser = String(username).toLowerCase().trim();
  for(var i=1; i<rows.length; i++) {
    if(String(rows[i][0]).toLowerCase().trim() == targetUser) {
      return {
        status: 'success',
        data: {
          username: rows[i][0], nama: rows[i][2], aum: rows[i][3],
          jk: rows[i][4]||"", alamat: rows[i][5]||"", nbm: rows[i][6]||"",
          tempat_lahir: rows[i][7]||"", tgl_lahir: rows[i][8]?Utilities.formatDate(new Date(rows[i][8]),"Asia/Jakarta","yyyy-MM-dd"):"",
          email: rows[i][9]||"", hp: rows[i][10]||""
        }
      };
    }
  }
  return { status: 'error', message: 'User tidak ditemukan' };
}

function updateUserProfile(data) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(SHEET_AKUN);
  var rows = sheet.getDataRange().getValues();
  var targetUser = String(data.username).toLowerCase().trim();
  
  for(var i=1; i<rows.length; i++) {
    if(String(rows[i][0]).toLowerCase().trim() == targetUser) {
      var rowIdx = i + 1;
      
      var oldName = rows[i][2]; // Kolom C (Index 2) adalah Nama
      var newName = data.nama;

      sheet.getRange(rowIdx, 3).setValue(newName);
      sheet.getRange(rowIdx, 4).setValue(data.aum);
      sheet.getRange(rowIdx, 5).setValue(data.jk);
      sheet.getRange(rowIdx, 6).setValue(data.alamat);
      sheet.getRange(rowIdx, 7).setValue("'"+data.nbm);
      sheet.getRange(rowIdx, 8).setValue(data.tempat_lahir);
      sheet.getRange(rowIdx, 9).setValue(data.tgl_lahir);
      sheet.getRange(rowIdx, 10).setValue(data.email);
      sheet.getRange(rowIdx, 11).setValue("'"+data.hp);
      
      if (oldName !== newName) {
         updateNamaDiHistory(oldName, newName);
      }

      return { status: 'success', message: 'Profil diperbarui & Data lama disinkronkan!' };
    }
  }
  return { status: 'error', message: 'Gagal update: User tidak ditemukan' };
}

function updateNamaDiHistory(oldName, newName) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_PRESENSI);
  var range = sheet.getRange("B:B"); 
  range.createTextFinder(oldName).matchEntireCell(true).replaceAllWith(newName);
}

function changePassword(data) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_AKUN);
  var rows = sheet.getDataRange().getValues();
  var targetUser = String(data.username).toLowerCase().trim();
  for(var i=1; i<rows.length; i++) {
    if(String(rows[i][0]).toLowerCase().trim() == targetUser) {
      sheet.getRange(i+1, 2).setValue("'" + data.newPass);
      return { status: 'success', message: 'Password berhasil diubah!' };
    }
  }
  return { status: 'error', message: 'User tidak ditemukan' };
}

function getDataOptions() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_DATA);
  var lastRow = sheet.getLastRow();
  if (lastRow < 1) return { status: 'success', nama: [], aum: [] };
  var rawNama = sheet.getRange(1, 1, lastRow, 1).getValues().flat();
  var rawAum = sheet.getRange(1, 2, lastRow, 1).getValues().flat();
  var listNama = rawNama.filter(String).sort((a,b) => a.toLowerCase().localeCompare(b.toLowerCase()));
  var uniqueAum = [...new Set(rawAum.filter(String))].sort();
  return { status: 'success', nama: listNama, aum: uniqueAum };
}

function processForm(data) {
  var lokasiValid = false; var lokasiTerdeteksi = ""; var jarakTerdekat = 999999;
  for (var i = 0; i < DAFTAR_LOKASI.length; i++) {
    var d = hitungJarak(data.lat, data.lng, DAFTAR_LOKASI[i].lat, DAFTAR_LOKASI[i].lng);
    if (d < jarakTerdekat) jarakTerdekat = d;
    if (d <= RADIUS_METER) { lokasiValid = true; lokasiTerdeteksi = DAFTAR_LOKASI[i].nama; break; }
  }
  if (!lokasiValid) return { status: 'error', message: 'Kejauhan! Jarak: ' + Math.round(jarakTerdekat) + 'm' };
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_PRESENSI);
    var folder = DriveApp.getFolderById(FOLDER_ID);
    var imageBlob = Utilities.newBlob(Utilities.base64Decode(data.image), 'image/png', data.nama + "_" + new Date().getTime() + ".png");
    var file = folder.createFile(imageBlob);
    sheet.appendRow([new Date(), data.nama, data.aum, data.kegiatan, data.kesimpulan, lokasiTerdeteksi + " ("+data.lokasiString+")", file.getUrl()]);
    return { status: 'success', message: '✅ Presensi Sukses di ' + lokasiTerdeteksi };
  } catch (e) { return { status: 'error', message: 'Gagal: ' + e.toString() }; }
}

function getRiwayat(nama, start, end, limit) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(SHEET_PRESENSI);
  var sheetData = ss.getSheetByName(SHEET_DATA); 
  var aumUser = "-";
  var dataAnggota = sheetData.getDataRange().getValues();
  for(var i=0; i<dataAnggota.length; i++) { if(dataAnggota[i][0] == nama) { aumUser = dataAnggota[i][1]; break; } }
  
  var rows = sheet.getDataRange().getValues();
  var globalUniqueDates = new Set();
  for(var i=1; i<rows.length; i++) { if(rows[i][0]) { var dG = new Date(rows[i][0]); globalUniqueDates.add(Utilities.formatDate(dG, "Asia/Jakarta", "yyyy-MM-dd")); } }
  var totalGlobalEvents = globalUniqueDates.size;
  
  var hasil = []; var foto = ""; var lastDateRaw = null; var userUniqueDates = new Set();
  var fStart = start ? new Date(start) : null; var fEnd = end ? new Date(end) : null; if(fEnd) fEnd.setHours(23,59,59);
  
  var maxRec = limit ? parseInt(limit) : 500; 

  for(var i=rows.length-1; i>=1; i--) { 
    if(rows[i][1] == nama) {
       var d = new Date(rows[i][0]); userUniqueDates.add(Utilities.formatDate(d, "Asia/Jakarta", "yyyy-MM-dd"));
       if(!foto && rows[i][6]) { try{ var id=rows[i][6].match(/[-\w]{25,}/); if(id) foto=id[0]; lastDateRaw=d; }catch(e){} }
       
       var showRecord = true; 
       if(fStart && d < fStart) showRecord = false; 
       if(fEnd && d > fEnd) showRecord = false;
       
       if(showRecord && hasil.length < maxRec) {
          hasil.push({ tanggalRaw: d, tanggal: formatTanggalIndo(d), jam: Utilities.formatDate(d, "Asia/Jakarta", "HH:mm") + " WIB", kegiatan: rows[i][3], lokasi: rows[i][5] });
       }
    }
  }
  if(foto) { try{ var b=DriveApp.getFileById(foto).getBlob(); foto=Utilities.base64Encode(b.getBytes()); }catch(e){foto=""} }
  var lastPresensiStr = lastDateRaw ? formatTanggalIndo(lastDateRaw) : "-";
  var percent = totalGlobalEvents > 0 ? Math.round((userUniqueDates.size / totalGlobalEvents) * 100) : 0;
  return { status: 'success', history: hasil, aum: aumUser, fotoTerbaru: foto, lastPresensi: lastPresensiStr, stats: { userTotal: userUniqueDates.size, globalTotal: totalGlobalEvents, percent: percent } };
}

function hitungJarak(lat1, lon1, lat2, lon2) {
  var R = 6371000, dLat = (lat2-lat1)*Math.PI/180, dLon = (lon2-lon1)*Math.PI/180;
  var a = Math.sin(dLat/2)*Math.sin(dLat/2) + Math.cos(lat1*Math.PI/180)*Math.cos(lat2*Math.PI/180) * Math.sin(dLon/2)*Math.sin(dLon/2);
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
}

function formatTanggalIndo(dateObj) {
  var hariArr = ["Ahad", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"];
  var bulanArr = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"];
  var d = new Date(dateObj);
  return hariArr[d.getDay()] + ", " + d.getDate() + " " + bulanArr[d.getMonth()] + " " + d.getFullYear();
}

function getRankingData() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(SHEET_PRESENSI);
  var rows = sheet.getDataRange().getValues();
  
  var userStats = {};
  var aumStats = {};
  
  for(var i=1; i<rows.length; i++) {
    var dateVal = rows[i][0];
    var nama = rows[i][1];
    var aum = rows[i][2];
    
    if(!nama) continue; 
    
    var timeMs = new Date(dateVal).getTime();
    
    if(!userStats[nama]) {
      userStats[nama] = { nama: nama, count: 0, aum: aum, firstTime: timeMs, history: [] };
    }
    userStats[nama].count++;
    
    if(timeMs < userStats[nama].firstTime) {
      userStats[nama].firstTime = timeMs;
    }
    
    try {
      var dStr = formatTanggalIndo(dateVal);
      var wStr = Utilities.formatDate(new Date(dateVal), "Asia/Jakarta", "HH:mm") + " WIB";
      var lokasiString = rows[i][5] ? rows[i][5].toString() : "-"; 
      
      userStats[nama].history.push({ 
          tglRaw: timeMs, 
          tglStr: dStr, 
          waktu: wStr, 
          lokasi: lokasiString 
      });
    } catch(e) {
      userStats[nama].history.push({ 
          tglRaw: timeMs, 
          tglStr: new Date(dateVal).toLocaleDateString(), 
          waktu: "", 
          lokasi: "-" 
      });
    }
    
    if(aum) {
      if(!aumStats[aum]) {
        aumStats[aum] = { aum: aum, count: 0, members: {} };
      }
      aumStats[aum].count++;
      if(!aumStats[aum].members[nama]) {
        aumStats[aum].members[nama] = 0;
      }
      aumStats[aum].members[nama]++;
    }
  }
  
  var userArr = [];
  for (var key in userStats) { userArr.push(userStats[key]); }
  
  var aumArr = [];
  for (var k in aumStats) { 
    var memArr = [];
    for(var m in aumStats[k].members) {
      memArr.push({ nama: m, count: aumStats[k].members[m] });
    }
    memArr.sort(function(a,b) { return b.count - a.count; });
    aumStats[k].memberList = memArr;
    
    delete aumStats[k].members;
    aumArr.push(aumStats[k]); 
  }
  
  userArr.sort(function(a, b) {
    if (b.count !== a.count) return b.count - a.count;
    return a.firstTime - b.firstTime;
  });
  
  aumArr.sort(function(a, b) {
    return b.count - a.count;
  });
  
  var topUsers = userArr.slice(0, 20);
  
  var options = getDataOptions();
  var daftarAum = options.aum; 
  
  // ==========================================
  // FITUR BARU: ANALITIK TREN
  // Mengelompokkan data berdasarkan tanggal
  // ==========================================
  var trendMap = {};
  for(var i=1; i<rows.length; i++) {
    var rawTgl = rows[i][0]; 
    if(!rawTgl) continue;
    var tglKunci = "";
    if (rawTgl instanceof Date) {
      var y = rawTgl.getFullYear();
      var m = ("0" + (rawTgl.getMonth() + 1)).slice(-2);
      var d = ("0" + rawTgl.getDate()).slice(-2);
      tglKunci = y + "-" + m + "-" + d; 
    } else {
      tglKunci = String(rawTgl).split(" ")[0]; 
    }
    
    if(tglKunci && tglKunci !== "undefined" && tglKunci !== "") {
      if(!trendMap[tglKunci]) trendMap[tglKunci] = 0;
      trendMap[tglKunci]++;
    }
  }

  var trendData = [];
  for (var key in trendMap) {
    trendData.push({
      tanggal: key,
      jumlah: trendMap[key]
    });
  }
  
  trendData.sort(function(a, b) {
    return new Date(a.tanggal) - new Date(b.tanggal);
  });
  
  return {
    status: 'success',
    data: {
      topUsers: topUsers,
      topAums: aumArr,
      daftarAum: daftarAum,
      trendData: trendData
    }
  };
}

```