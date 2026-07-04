import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix showAllJamaah by setting currentDetailData
old_show_all = "currentDetailType = 'allJamaah';"
new_show_all = "currentDetailType = 'allJamaah';\n         currentDetailData = { total: users.length };"
content = content.replace(old_show_all, new_show_all)

# 2. Remove global loading screen HTML
loading_html = """  <!-- GLOBAL LOADING OVERLAY -->
  <div id="globalLoadingScreen" class="fullscreen-overlay hidden"
    style="z-index: 2000; background: rgba(255,255,255,0.9);">
    <div class="d-flex flex-column justify-content-center align-items-center h-100">
      <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;" role="status"></div>
      <h6 class="mt-3 fw-bold text-dark">Mempersiapkan Data...</h6>
      <p class="small text-muted">Sedang mengambil rekapitulasi terbaru dari server</p>
    </div>
  </div>"""
content = content.replace(loading_html, "")

# 3. Remove global loading screen JS
js_show_loading = "document.getElementById('globalLoadingScreen').classList.remove('hidden');"
content = content.replace(js_show_loading, "")

js_hide_loading = """        } finally {
          document.getElementById('globalLoadingScreen').classList.add('hidden');
        }"""
content = content.replace(js_hide_loading, "        }")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("fixed cetak and loading")
