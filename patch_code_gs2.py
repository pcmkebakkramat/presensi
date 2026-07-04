import re

file_path = '/Users/kirman/.gemini/antigravity-ide/brain/c6433901-94a9-4bfa-9cfc-84f200a00378/full_code_gs.md'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Modify getRankingData to return allUsers
old_return = """  return {
    status: 'success',
    data: {
      topUsers: topUsers,
      topAums: aumArr,
      daftarAum: daftarAum,
      trendData: trendData
    }
  };"""

new_return = """  var allUsersShort = userArr.map(function(u) { return {nama: u.nama, aum: u.aum, count: u.count}; });
  
  return {
    status: 'success',
    data: {
      topUsers: topUsers,
      allUsers: allUsersShort,
      topAums: aumArr,
      daftarAum: daftarAum,
      trendData: trendData
    }
  };"""

content = content.replace(old_return, new_return)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("patched")
