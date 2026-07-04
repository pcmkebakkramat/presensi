import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add print button to Leaderboard (Paling Aktif)
content = content.replace(
    '<h6 class="m-0 fw-bold">Jamaah Paling Aktif</h6><button class="btn-close-custom"',
    '<h6 class="m-0 fw-bold">Jamaah Paling Aktif</h6>\n        <div><button class="btn btn-sm btn-danger me-2" id="btnCetakPalingAktif" onclick="cetakPalingAktif()" title="Cetak PDF"><i class="bi bi-file-earmark-pdf-fill"></i></button><button class="btn-close-custom"'
)

# 2. Add print button to Heatmap (AUM Teraktif)
content = content.replace(
    '<h6 class="m-0 fw-bold">AUM Teraktif</h6><button class="btn-close-custom"',
    '<h6 class="m-0 fw-bold">AUM Teraktif</h6>\n        <div><button class="btn btn-sm btn-danger me-2" id="btnCetakAumTeraktif" onclick="cetakAumTeraktif()" title="Cetak PDF"><i class="bi bi-file-earmark-pdf-fill"></i></button><button class="btn-close-custom"'
)

# 3. Add print button to Daftar AUM (Assuming it has a modal)
# Let's check what the modal is called
content = content.replace(
    '<h6 class="m-0 fw-bold">Daftar AUM</h6><button class="btn-close-custom"',
    '<h6 class="m-0 fw-bold">Daftar AUM</h6>\n        <div><button class="btn btn-sm btn-danger me-2" id="btnCetakDaftarAum" onclick="cetakDaftarAum()" title="Cetak PDF"><i class="bi bi-file-earmark-pdf-fill"></i></button><button class="btn-close-custom"'
)

# 4. Add print button to Detail Screen
content = content.replace(
    '<h6 class="m-0 fw-bold text-truncate" id="detailTitle" style="max-width: 250px;">Detail</h6>\n        <button class="btn-close-custom"',
    '<h6 class="m-0 fw-bold text-truncate" id="detailTitle" style="max-width: 250px;">Detail</h6>\n        <div><button class="btn btn-sm btn-danger me-2" id="btnCetakDetail" onclick="cetakDetail()" title="Cetak PDF"><i class="bi bi-file-earmark-pdf-fill"></i></button><button class="btn-close-custom"'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
