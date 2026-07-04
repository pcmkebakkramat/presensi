function cleanString(str) {
  if (!str) return "";
  let s = str.trim();
  s = s.replace(/^[`'"]+/, '');
  s = s.replace(/\s+/g, ' ');
  console.log("After replace:", s);
  
  if (/^[`'"]*\s*T\s*K\s+A\s*i\s*s\s*y\s*i\s*y\s*a\s*h\s+K\s*e\s*b\s*a\s*k/i.test(s)) return "TK Aisyiyah Kebak";
  if (/^[`'"]*\s*K\s*B\s+A\s*i\s*s\s*y\s*i\s*y\s*a\s*h\s+W\s*a\s*r\s*u/i.test(s)) return "KB Aisyiyah Waru";
  if (/^[`'"]*\s*M\s*I\s*M\s+K\s*a\s*l\s*i\s*w\s*u\s*l\s*u\s*h/i.test(s)) return "MIM Kaliwuluh";
  return s.trim();
}

console.log(cleanString("` M I M   K a l i w u l u h"));
console.log(cleanString("` K B   A i s y i y a h   W a r u"));
console.log(cleanString("` T K   A i s y i y a h   K e b a k"));
