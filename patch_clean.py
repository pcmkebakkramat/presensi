with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

clean_string_logic = """
    function cleanString(str) {
      if (!str) return "";
      let s = str.trim();
      s = s.replace(/^[`'"]+/, '');
      s = s.replace(/\\s+/g, ' ');
      // Fallback spesifik
      if (/^[`'"]*\\s*T\\s*K\\s+A\\s*i\\s*s\\s*y\\s*i\\s*y\\s*a\\s*h\\s+K\\s*e\\s*b\\s*a\\s*k/.test(s)) return "TK Aisyiyah Kebak";
      if (/^[`'"]*\\s*K\\s*B\\s+A\\s*i\\s*s\\s*y\\s*i\\s*y\\s*a\\s*h\\s+W\\s*a\\s*r\\s*u/.test(s)) return "KB Aisyiyah Waru";
      if (/^[`'"]*\\s*M\\s*I\\s*M\\s+K\\s*a\\s*l\\s*i\\s*w\\s*u\\s*l\\s*u\\s*h/.test(s)) return "MIM Kaliwuluh";
      return s.trim();
    }
"""

content = content.replace("async function loadDashboardData()", clean_string_logic + "\n    async function loadDashboardData()")
content = content.replace('item[6] || "-"', 'cleanString(item[6]) || "-"')
content = content.replace('u[6]', 'cleanString(u[6])')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
