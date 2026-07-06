import re

with open('full_code_gs.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update getRiwayat
old_riwayat_loop = """  var hasil = []; var foto = ""; var lastDateRaw = null; var userUniqueDates = new Set();
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
  if(foto) { try{ var b=DriveApp.getFileById(foto).getBlob(); foto=Utilities.base64Encode(b.getBytes()); }catch(e){foto=""} }"""

new_riwayat_loop = """  var userUniqueDates = new Set();
  var dictEarliest = {}; 
  var fStart = start ? new Date(start) : null; var fEnd = end ? new Date(end) : null; if(fEnd) fEnd.setHours(23,59,59);
  var maxRec = limit ? parseInt(limit) : 500; 

  for(var i=1; i<rows.length; i++) {
    if(rows[i][1] == nama) {
       var d = new Date(rows[i][0]);
       var dateStr = Utilities.formatDate(d, "Asia/Jakarta", "yyyy-MM-dd");
       userUniqueDates.add(dateStr);
       
       if(!dictEarliest[dateStr]) {
          var recordFoto = "";
          if(rows[i][6]) { try{ var id=rows[i][6].match(/[-\w]{25,}/); if(id) recordFoto=id[0]; }catch(e){} }
          
          dictEarliest[dateStr] = {
             tanggalRaw: d, 
             tanggal: formatTanggalIndo(d), 
             jam: Utilities.formatDate(d, "Asia/Jakarta", "HH:mm") + " WIB", 
             kegiatan: rows[i][3], 
             lokasi: rows[i][5],
             foto: recordFoto
          };
       }
    }
  }
  
  var sortedDates = Array.from(userUniqueDates).sort().reverse();
  var hasil = [];
  var foto = "";
  var lastDateRaw = null;
  
  for(var j=0; j<sortedDates.length; j++) {
     var ds = sortedDates[j];
     var rec = dictEarliest[ds];
     
     if (j === 0) {
        lastDateRaw = rec.tanggalRaw;
        foto = rec.foto;
     }
     
     var showRecord = true;
     if(fStart && rec.tanggalRaw < fStart) showRecord = false;
     if(fEnd && rec.tanggalRaw > fEnd) showRecord = false;
     
     if (showRecord && hasil.length < maxRec) {
        hasil.push({
           tanggalRaw: rec.tanggalRaw,
           tanggal: rec.tanggal,
           jam: rec.jam,
           kegiatan: rec.kegiatan,
           lokasi: rec.lokasi
        });
     }
  }
  if(foto) { try{ var b=DriveApp.getFileById(foto).getBlob(); foto=Utilities.base64Encode(b.getBytes()); }catch(e){foto=""} }"""

content = content.replace(old_riwayat_loop, new_riwayat_loop)

# 2. Update getRankingData
old_ranking_loop = """  for(var i=1; i<rows.length; i++) {
    var dateVal = rows[i][0];
    var nama = rows[i][1];
    var aum = rows[i][2];
    
    if(!nama) continue; 
    
    var timeMs = new Date(dateVal).getTime();
    
    if(!userStats[nama]) {
      userStats[nama] = { nama: nama, count: 0, aum: aum, firstTime: timeMs, history: [] };
    }
    userStats[nama].count++;"""

new_ranking_loop = """  for(var i=1; i<rows.length; i++) {
    var dateVal = rows[i][0];
    var nama = rows[i][1];
    var aum = rows[i][2];
    
    if(!nama) continue; 
    
    var timeMs = new Date(dateVal).getTime();
    var dateStr = Utilities.formatDate(new Date(dateVal), "Asia/Jakarta", "yyyy-MM-dd");
    
    if(!userStats[nama]) {
      userStats[nama] = { nama: nama, count: 0, aum: aum, firstTime: timeMs, history: [], _seenDates: {} };
    }
    
    if(userStats[nama]._seenDates[dateStr]) continue;
    userStats[nama]._seenDates[dateStr] = true;
    
    userStats[nama].count++;"""

content = content.replace(old_ranking_loop, new_ranking_loop)

with open('full_code_gs.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("patched deduplication")
