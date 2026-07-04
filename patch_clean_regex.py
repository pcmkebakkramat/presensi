with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_clean = """            function cleanString(str) {
              if (!str) return "";
              let s = str.trim();
              s = s.replace(/^[`'"]+/, '');
              s = s.replace(/\\s+/g, ' ');
              // Fallback spesifik
              if (/^[`'"]*\\s*T\\s*K\\s+A\\s*i\\s*s\\s*y\\s*i\\s*y\\s*a\\s*h\\s+K\\s*e\\s*b\\s*a\\s*k/.test(s)) return "TK Aisyiyah Kebak";
              if (/^[`'"]*\\s*K\\s*B\\s+A\\s*i\\s*s\\s*y\\s*i\\s*y\\s*a\\s*h\\s+W\\s*a\\s*r\\s*u/.test(s)) return "KB Aisyiyah Waru";
              if (/^[`'"]*\\s*M\\s*I\\s*M\\s+K\\s*a\\s*l\\s*i\\s*w\\s*u\\s*l\\s*u\\s*h/.test(s)) return "MIM Kaliwuluh";
              return s.trim();
            }"""

new_clean = """            function cleanString(str) {
              if (!str) return "";
              let s = str.trim();
              s = s.replace(/^[`'"]+/, ''); // strip leading quotes
              s = s.replace(/\\s+/g, ' '); // collapse spaces
              
              let stripped = s.replace(/[^a-zA-Z0-9]/g, '').toLowerCase();
              
              if (stripped.includes('tkaisyiyahkebak')) return 'TK Aisyiyah Kebak';
              if (stripped.includes('kbaisyiyahwaru')) return 'KB Aisyiyah Waru';
              if (stripped.includes('mimkaliwuluh')) return 'MIM Kaliwuluh';
              
              return s.trim();
            }"""

if old_clean in content:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content.replace(old_clean, new_clean))
    print("Replaced successfully")
else:
    print("Could not find old cleanString.")
