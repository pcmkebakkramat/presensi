import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

modals_html = """
    <!-- INFO UPDATE MODAL -->
    <div id="infoUpdateScreen" class="fullscreen-overlay hidden" style="z-index: 1045;">
      <div class="overlay-header">
        <h6 class="m-0 fw-bold">Info Pembaruan Aplikasi</h6>
        <button class="btn-close-custom" onclick="closeFeatureModal('infoUpdateScreen')"><i class="bi bi-x"></i></button>
      </div>
      <div class="overlay-body bg-light">
        <div class="container-fluid py-3">
          <div class="text-center mb-4">
            <i class="bi bi-stars text-warning" style="font-size:3rem;"></i>
            <h5 class="fw-bold mt-2">Selamat Datang di Versi Baru!</h5>
            <p class="text-muted small">Kami telah menyematkan 4 fitur canggih untuk mempermudah Anda.</p>
          </div>
          <div class="list-group">
            <div class="list-group-item border-0 shadow-sm mb-2" style="border-radius:12px;">
              <h6 class="fw-bold text-warning"><i class="bi bi-person-lines-fill me-2"></i>Jamaah Paling Aktif</h6>
              <p class="mb-0 small text-muted">Melihat daftar jamaah dengan presensi terbanyak. Apresiasi bagi mereka yang istiqomah!</p>
            </div>
            <div class="list-group-item border-0 shadow-sm mb-2" style="border-radius:12px;">
              <h6 class="fw-bold text-info"><i class="bi bi-buildings-fill me-2"></i>AUM Teraktif</h6>
              <p class="mb-0 small text-muted">Mengetahui Instansi / AUM mana yang mengirimkan jamaah terbanyak ke pengajian.</p>
            </div>
            <div class="list-group-item border-0 shadow-sm mb-2" style="border-radius:12px;">
              <h6 class="fw-bold text-danger"><i class="bi bi-list-stars me-2"></i>Daftar AUM</h6>
              <p class="mb-0 small text-muted">Pusat database untuk memantau jumlah jamaah yang terdaftar di masing-masing AUM.</p>
            </div>
            <div class="list-group-item border-0 shadow-sm mb-2" style="border-radius:12px;">
              <h6 class="fw-bold" style="color: #856404;"><i class="bi bi-graph-up-arrow me-2"></i>Analitik Tren</h6>
              <p class="mb-0 small text-muted">Memantau fluktuasi partisipasi jamaah dari waktu ke waktu secara real-time via grafik cerdas.</p>
            </div>
          </div>
          <button class="btn btn-primary w-100 mt-4 fw-bold" style="border-radius:12px;" onclick="closeFeatureModal('infoUpdateScreen')">Mulai Gunakan</button>
        </div>
      </div>
    </div>

    <!-- KUESIONER SUS MODAL -->
    <div id="susSurveyScreen" class="fullscreen-overlay hidden" style="z-index: 1060; background:#f8fafc;">
      <div class="overlay-header">
        <h6 class="m-0 fw-bold">Evaluasi Sistem (Wajib)</h6>
        <button class="btn-close-custom" id="btnNantiSurvey" onclick="closeFeatureModal('susSurveyScreen')">Nanti</button>
      </div>
      <div class="overlay-body">
        <div class="container-fluid py-3">
          <div class="alert alert-info small mb-4 shadow-sm" style="border-radius:12px;">
            <i class="bi bi-info-circle-fill"></i> <b>Tidak Ada Penalti!</b><br>
            Pengisian kuesioner ini sama sekali tidak mempengaruhi akun Anda. Kami mohon Anda menjawab secara <b>jujur</b> sesuai dengan apa yang Anda rasakan untuk perbaikan sistem ini ke depannya.
          </div>
          
          <form id="surveyForm" onsubmit="submitSurveyForm(event)">
            <h6 class="fw-bold text-primary mb-3 border-bottom pb-2">Bagian 1: Usability Scale (SUS)</h6>
            <div id="susQuestionsContainer"></div>
            
            <h6 class="fw-bold text-primary mb-3 mt-4 border-bottom pb-2">Bagian 2: Rating Fitur Baru</h6>
            <div id="ratingQuestionsContainer"></div>
            
            <h6 class="fw-bold text-primary mb-3 mt-4 border-bottom pb-2">Bagian 3: Feedback Terbuka</h6>
            <div class="mb-3">
              <label class="form-label small fw-bold">1. Tuliskan pengalaman Anda menggunakan sistem baru, apakah menyukai atau tidak, sampaikan sesuai dengan apa yang Anda rasakan.</label>
              <textarea class="form-control" id="surveyQ1" rows="3" required style="border-radius:10px;"></textarea>
            </div>
            <div class="mb-4">
              <label class="form-label small fw-bold">2. Berikan saran dan masukan, termasuk keluhan, untuk menjadikan sistem (aplikasi) ini lebih baik.</label>
              <textarea class="form-control" id="surveyQ2" rows="3" required style="border-radius:10px;"></textarea>
            </div>
            
            <button type="submit" id="btnSubmitSurvey" class="btn btn-primary w-100 fw-bold mb-4" style="border-radius:12px; padding:12px;">Kirim Survei</button>
          </form>
        </div>
      </div>
    </div>
"""

# Inject before badgeInfoScreen
content = content.replace("<!-- BADGE INFO MODAL -->", modals_html + "\n    <!-- BADGE INFO MODAL -->")

# Add to Main Menu (under Panduan)
menu_html = """
    <li class="menu-item" onclick="openInfoModal(); toggleMenu()">
        <div class="menu-icon"><i class="bi bi-question-circle-fill"></i></div>
        <div class="menu-text">Panduan & Instalasi</div><i class="bi bi-chevron-right menu-chevron"></i>
    </li>
    <li class="menu-item" onclick="openFeatureModal('infoUpdateScreen'); toggleMenu()">
        <div class="menu-icon bg-warning-light text-warning"><i class="bi bi-stars"></i></div>
        <div class="menu-text">Info Pembaruan Baru</div><i class="bi bi-chevron-right menu-chevron"></i>
    </li>"""

content = content.replace("""    <li class="menu-item" onclick="openInfoModal(); toggleMenu()">
        <div class="menu-icon"><i class="bi bi-question-circle-fill"></i></div>
        <div class="menu-text">Panduan & Instalasi</div><i class="bi bi-chevron-right menu-chevron"></i>
    </li>""", menu_html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("index HTML patched")
