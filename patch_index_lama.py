import re

with open('index-lama.html', 'r', encoding='utf-8') as f:
    content = f.read()

popup_html = """
<!-- MIGRATION POPUP -->
<div id="migrationModal" class="hidden" style="position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.8);z-index:99999;display:flex;align-items:center;justify-content:center;padding:20px;">
  <div style="background:#fff;border-radius:20px;padding:25px;max-width:400px;width:100%;text-align:center;box-shadow:0 10px 25px rgba(0,0,0,0.2);">
    <i class="bi bi-rocket-takeoff-fill text-primary" style="font-size:3rem;margin-bottom:10px;display:block;"></i>
    <h5 class="fw-bold mb-3">Sistem Baru Telah Hadir!</h5>
    <p class="text-muted small mb-3">
      Kami telah mengembangkan sistem presensi kajian AUM yang baru dengan fitur yang jauh lebih canggih, seperti: <br>
      <b>Jamaah Paling Aktif, AUM Teraktif, Daftar AUM, dan Analitik Tren!</b>
    </p>
    <div class="alert alert-warning small text-start p-2 mb-3">
      <i class="bi bi-info-circle-fill"></i> <b>Info Penting:</b><br>
      Anda tidak perlu daftar ulang! Username dan Password Anda <b>sama persis</b> seperti yang Anda gunakan di sistem ini.
    </div>
    <p class="text-danger small mb-4 fw-bold">
      Sistem lama ini akan dinonaktifkan pada <b>1 Agustus 2026</b>. Mohon segera beralih sebelum batas waktu tersebut!
    </p>
    <a href="https://pcmkebakkramat.github.io/presensi" class="btn btn-primary w-100 mb-2 fw-bold" style="border-radius:12px;">Buka Sistem Baru Sekarang</a>
    <button id="btnTutupMigration" onclick="document.getElementById('migrationModal').classList.add('hidden')" class="btn btn-light w-100" style="border-radius:12px;">Tutup & Gunakan Sistem Lama</button>
  </div>
</div>
<script>
  window.addEventListener('load', function() {
    var today = new Date();
    var deadline = new Date('2026-08-01T00:00:00+07:00');
    var modal = document.getElementById('migrationModal');
    var btnTutup = document.getElementById('btnTutupMigration');
    
    // Show modal automatically
    setTimeout(function() {
      modal.classList.remove('hidden');
      if (today >= deadline) {
        // Hide close button if past deadline
        btnTutup.style.display = 'none';
      }
    }, 500);
  });
</script>
</body>
"""

content = content.replace("</body>", popup_html)

with open('index-lama.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("index-lama patched")
