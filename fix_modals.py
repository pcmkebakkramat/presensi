html = """    <!-- PALING AKTIF MODAL -->
    <div id="leaderboardScreen" class="fullscreen-overlay hidden">
      <div class="overlay-header">
        <h6 class="m-0 fw-bold">Jamaah Paling Aktif</h6>
        <div><button class="btn btn-sm btn-danger me-2" id="btnCetakPalingAktif" onclick="cetakPalingAktif()" title="Cetak PDF"><i class="bi bi-file-earmark-pdf-fill"></i></button><button class="btn-close-custom" onclick="closeFeatureModal('leaderboardScreen')"><i class="bi bi-x"></i></button></div>
      </div>
      <div class="overlay-body">
        <div id="listPalingAktif" class="list-group">
          <div class="text-center py-4">
            <div class="spinner-border text-primary spinner-border-sm"></div> Memuat data...
          </div>
        </div>
      </div>
    </div>

    <!-- AUM TERAKTIF MODAL -->
    <div id="heatmapScreen" class="fullscreen-overlay hidden">
      <div class="overlay-header">
        <h6 class="m-0 fw-bold">AUM Teraktif</h6>
        <div><button class="btn btn-sm btn-danger me-2" id="btnCetakAumTeraktif" onclick="cetakAumTeraktif()" title="Cetak PDF"><i class="bi bi-file-earmark-pdf-fill"></i></button><button class="btn-close-custom" onclick="closeFeatureModal('heatmapScreen')"><i class="bi bi-x"></i></button></div>
      </div>
      <div class="overlay-body">
        <div id="listAumTeraktif" class="list-group">
          <div class="text-center py-4">
            <div class="spinner-border text-primary spinner-border-sm"></div> Memuat data...
          </div>
        </div>
      </div>
    </div>

    <!-- DAFTAR AUM MODAL -->
    <div id="daftarAumScreen" class="fullscreen-overlay hidden">
      <div class="overlay-header">
        <h6 class="m-0 fw-bold">Daftar AUM</h6>
        <div><button class="btn btn-sm btn-danger me-2" id="btnCetakDaftarAum" onclick="cetakDaftarAum()" title="Cetak PDF"><i class="bi bi-file-earmark-pdf-fill"></i></button><button class="btn-close-custom" onclick="closeFeatureModal('daftarAumScreen')"><i class="bi bi-x"></i></button></div>
      </div>
      <div class="overlay-body">
        <div class="alert alert-light border small text-center mb-3"><i class="bi bi-info-circle"></i> Daftar Amal Usaha Muhammadiyah yang terdaftar.</div>
        <div id="listDaftarAum" class="list-group">
          <div class="text-center py-4">
            <div class="spinner-border text-primary spinner-border-sm"></div> Memuat data...
          </div>
        </div>
      </div>
    </div>

    <!-- BADGE INFO MODAL -->
    <div id="badgeInfoScreen" class="fullscreen-overlay hidden">
      <div class="overlay-header">
        <h6 class="m-0 fw-bold">Lencana Pencapaian</h6><button class="btn-close-custom" onclick="closeFeatureModal('badgeInfoScreen')"><i class="bi bi-x"></i></button>
      </div>
      <div class="overlay-body">
        <div class="text-center mb-4 mt-3">
          <h1 class="display-1 mb-2" id="badgeModalIcon">🎖️</h1>
          <h5 class="fw-bold" id="badgeModalTitle">Lencana</h5>
          <p class="text-muted small" id="badgeModalDesc">-</p>
        </div>
        <hr>
        <h6 class="fw-bold mb-3">Tingkatan Lencana:</h6>
        <div class="d-flex align-items-center mb-3">
          <h3 class="m-0 me-3">🥉</h3>
          <div><strong>Pencari Ilmu</strong>
            <div class="small text-muted">Langkah awal yang baik, terus tingkatkan!</div>
          </div>
        </div>
        <div class="d-flex align-items-center mb-3">
          <h3 class="m-0 me-3">🥈</h3>
          <div><strong>Penggiat Kajian</strong>
            <div class="small text-muted">Anda semakin konsisten menuntut ilmu.</div>
          </div>
        </div>
        <div class="d-flex align-items-center mb-3">
          <h3 class="m-0 me-3">🥇</h3>
          <div><strong>Aktivis Dakwah</strong>
            <div class="small text-muted">Luar biasa! Separuh perjalanan telah dilalui dengan istiqomah.</div>
          </div>
        </div>
        <div class="d-flex align-items-center mb-3">
          <h3 class="m-0 me-3">💎</h3>
          <div><strong>Teladan Istiqomah</strong>
            <div class="small text-muted">MasyaAllah, Anda adalah teladan dalam memakmurkan majelis ilmu!</div>
          </div>
        </div>
      </div>
    </div>

    <!-- DETAIL MODAL (Riwayat Individu / Anggota AUM) -->
    <div id="detailScreen" class="fullscreen-overlay hidden" style="z-index: 1050;">
      <div class="overlay-header">
        <h6 class="m-0 fw-bold text-truncate" id="detailTitle" style="max-width: 250px;">Detail</h6>
        <div><button class="btn btn-sm btn-danger me-2" id="btnCetakDetail" onclick="cetakDetail()" title="Cetak PDF"><i class="bi bi-file-earmark-pdf-fill"></i></button><button class="btn-close-custom" onclick="closeFeatureModal('detailScreen')"><i class="bi bi-x"></i></button></div>
      </div>
      <div class="overlay-body">
        <div id="listDetail" class="list-group">
          <!-- Content -->
        </div>
      </div>
    </div>"""

import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_str = "    <!-- PALING AKTIF MODAL -->"
end_str = "    <script>"

start_idx = content.find(start_str)
end_idx = content.find(end_str)

if start_idx != -1 and end_idx != -1:
    new_content = content[:start_idx] + html + "\n\n" + content[end_idx:]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Modals fixed.")
else:
    print("Could not find start or end markers.")
