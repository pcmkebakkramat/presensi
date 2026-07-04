import re

file_path = '/Users/kirman/.gemini/antigravity-ide/brain/c6433901-94a9-4bfa-9cfc-84f200a00378/full_code_gs.md'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "else if (action === 'getRanking') result = getRankingData();",
    "else if (action === 'getRanking') result = getRankingData();\n    else if (action === 'saveSurvey') result = doSaveSurvey(params);"
)

save_survey_fn = """
function doSaveSurvey(params) {
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName("Survey");
    if (!sheet) {
      sheet = ss.insertSheet("Survey");
      var headers = ["Timestamp", "Username", "Nama Lengkap"];
      for(var i=1; i<=10; i++) headers.push("SUS " + i);
      for(var i=1; i<=4; i++) headers.push("Rating Fitur " + i);
      headers.push("Tanggapan Q1", "Tanggapan Q2");
      sheet.appendRow(headers);
      sheet.getRange(1, 1, 1, headers.length).setFontWeight("bold");
    }
    
    var rowData = [new Date(), params.username, params.nama];
    if(params.sus && params.sus.length) rowData = rowData.concat(params.sus);
    else for(var i=0; i<10; i++) rowData.push("");
    
    if(params.rating && params.rating.length) rowData = rowData.concat(params.rating);
    else for(var i=0; i<4; i++) rowData.push("");
    
    rowData.push(params.q1 || "");
    rowData.push(params.q2 || "");
    
    sheet.appendRow(rowData);
    return { status: 'success', message: 'Survey saved successfully' };
  } catch (e) {
    return { status: 'error', message: e.toString() };
  }
}
"""

content = content.replace("```\n\n", save_survey_fn + "\n```\n\n", 1)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("full_code_gs.md patched")
