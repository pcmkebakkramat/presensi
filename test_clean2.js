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

console.log(cleanString("` M I M   K a l i w u l u h"));
console.log(cleanString("` K B   A i s y i y a h   W a r u"));
console.log(cleanString("` T K   A i s y i y a h   K e b a k"));
console.log(cleanString("`MIM Kaliwuluh"));
console.log(cleanString("`KB Aisyiyah Waru"));
