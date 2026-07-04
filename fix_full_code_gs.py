import re

with open('full_code_gs.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add action === 'saveSurvey' handling
old_dopost = "else if (action === 'getRanking') result = getRankingData();"
new_dopost = "else if (action === 'getRanking') result = getRankingData();\n    else if (action === 'saveSurvey') result = saveSurvey(params);"
content = content.replace(old_dopost, new_dopost)

# 2. Add function saveSurvey(params)
save_survey_fn = """
function saveSurvey(params) {
  try {
    var ss = SpreadsheetApp.openById(FOLDER_ID);
    var sheet = ss.getSheetByName("Survey");
    if (!sheet) {
      sheet = ss.insertSheet("Survey");
      sheet.appendRow([
        "Timestamp", "Username", "Nama", 
        "SUS_1", "SUS_2", "SUS_3", "SUS_4", "SUS_5", 
        "SUS_6", "SUS_7", "SUS_8", "SUS_9", "SUS_10",
        "Rating_Aktif", "Rating_AUM", "Rating_Daftar", "Rating_Tren",
        "Komentar_Q1", "Komentar_Q2"
      ]);
    }
    
    var row = [
      new Date(),
      params.username,
      params.nama
    ];
    
    // SUS data (10 items)
    if(params.sus && params.sus.length) {
      for(var i=0; i<10; i++) row.push(params.sus[i] || "");
    } else {
      for(var i=0; i<10; i++) row.push("");
    }
    
    // Rating data (4 items)
    if(params.rating && params.rating.length) {
      for(var i=0; i<4; i++) row.push(params.rating[i] || "");
    } else {
      for(var i=0; i<4; i++) row.push("");
    }
    
    row.push(params.q1 || "");
    row.push(params.q2 || "");
    
    sheet.appendRow(row);
    return { status: 'success', message: 'Survei berhasil disimpan.' };
  } catch (e) {
    return { status: 'error', message: e.toString() };
  }
}
"""
content = content.replace("function getRankingData() {", save_survey_fn + "\n\nfunction getRankingData() {")

with open('full_code_gs.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("patched full_code_gs")
