import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update checkOnboardingAndSurvey to use pCount >= 1
old_check = "if (!surveyFilled && (pCount >= 3 || today >= deadline)) {"
new_check = "if (!surveyFilled && (pCount >= 1 || today >= deadline)) {"
content = content.replace(old_check, new_check)

old_forced = "let isForced = (today >= deadline || pCount >= 3);"
new_forced = "let isForced = (today >= deadline || pCount >= 1);"
content = content.replace(old_forced, new_forced)

# 2. Prevent presensi in openPresensiMode
old_open_presensi = """      function openPresensiMode() {
        document.getElementById('homeScreen').classList.add('hidden'); document.getElementById('presensiScreen').classList.remove('hidden'); if (navigator.mediaDevices) navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" } }).then(s => video.srcObject = s); if (navigator.geolocation) navigator.geolocation.watchPosition(updatePosisi, handleGpsError, { enableHighAccuracy: true });
        checkOnboardingAndSurvey();
      }"""
new_open_presensi = """      function openPresensiMode() {
        let surveyFilled = localStorage.getItem('has_filled_survey') === 'true';
        let pCount = parseInt(localStorage.getItem('local_presensi_count') || '0');
        if (!surveyFilled && pCount >= 1) {
            alert("Harap isi Survei Kepuasan terlebih dahulu untuk dapat melanjutkan presensi.");
            openSurveyModal(true);
            return;
        }
        document.getElementById('homeScreen').classList.add('hidden'); document.getElementById('presensiScreen').classList.remove('hidden'); if (navigator.mediaDevices) navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" } }).then(s => video.srcObject = s); if (navigator.geolocation) navigator.geolocation.watchPosition(updatePosisi, handleGpsError, { enableHighAccuracy: true });
        checkOnboardingAndSurvey();
      }"""
content = content.replace(old_open_presensi, new_open_presensi)

# 3. Update survey form style
old_rating = """              <div class="d-flex justify-content-between mt-1">
                <div class="form-check form-check-inline m-0"><input class="form-check-input" type="radio" name="rating${i}" value="1" required></div>
                <div class="form-check form-check-inline m-0"><input class="form-check-input" type="radio" name="rating${i}" value="2" required></div>
                <div class="form-check form-check-inline m-0"><input class="form-check-input" type="radio" name="rating${i}" value="3" required></div>
                <div class="form-check form-check-inline m-0"><input class="form-check-input" type="radio" name="rating${i}" value="4" required></div>
                <div class="form-check form-check-inline m-0"><input class="form-check-input" type="radio" name="rating${i}" value="5" required></div>
              </div>"""
new_rating = """              <div class="d-flex justify-content-between mt-1 text-center">
                <label class="form-check-label m-0" style="cursor:pointer;"><div class="small fw-bold text-dark" style="font-size:0.8rem;">1</div><input class="form-check-input mx-auto d-block mt-1" style="border:2px solid #94a3b8; width:1.2rem; height:1.2rem;" type="radio" name="rating${i}" value="1" required></label>
                <label class="form-check-label m-0" style="cursor:pointer;"><div class="small fw-bold text-dark" style="font-size:0.8rem;">2</div><input class="form-check-input mx-auto d-block mt-1" style="border:2px solid #94a3b8; width:1.2rem; height:1.2rem;" type="radio" name="rating${i}" value="2" required></label>
                <label class="form-check-label m-0" style="cursor:pointer;"><div class="small fw-bold text-dark" style="font-size:0.8rem;">3</div><input class="form-check-input mx-auto d-block mt-1" style="border:2px solid #94a3b8; width:1.2rem; height:1.2rem;" type="radio" name="rating${i}" value="3" required></label>
                <label class="form-check-label m-0" style="cursor:pointer;"><div class="small fw-bold text-dark" style="font-size:0.8rem;">4</div><input class="form-check-input mx-auto d-block mt-1" style="border:2px solid #94a3b8; width:1.2rem; height:1.2rem;" type="radio" name="rating${i}" value="4" required></label>
                <label class="form-check-label m-0" style="cursor:pointer;"><div class="small fw-bold text-dark" style="font-size:0.8rem;">5</div><input class="form-check-input mx-auto d-block mt-1" style="border:2px solid #94a3b8; width:1.2rem; height:1.2rem;" type="radio" name="rating${i}" value="5" required></label>
              </div>"""
content = content.replace(old_rating, new_rating)

# 4. Show survey in sidebar if not filled
old_render_menu = """    <li class="menu-item text-danger" onclick="doLogout()">
        <div class="menu-icon"><i class="bi bi-box-arrow-right"></i></div>
        <div class="menu-text">Keluar (Logout)</div>
    </li>`;"""
new_render_menu = """    <li class="menu-item text-danger" onclick="doLogout()">
        <div class="menu-icon"><i class="bi bi-box-arrow-right"></i></div>
        <div class="menu-text">Keluar (Logout)</div>
    </li>`;
        
        let surveyFilled = localStorage.getItem('has_filled_survey') === 'true';
        if (!surveyFilled) {
          menuHTML = `
          <li class="menu-item bg-light" onclick="openSurveyModal(true); toggleMenu()" style="border-radius:10px; margin-bottom:10px; border:1px solid #fcd34d;">
              <div class="menu-icon text-warning"><i class="bi bi-ui-checks-grid"></i></div>
              <div class="menu-text text-warning fw-bold">Isi Survei Kepuasan</div><i class="bi bi-chevron-right menu-chevron text-warning"></i>
          </li>` + menuHTML;
        }
"""
content = content.replace(old_render_menu, new_render_menu)

# Ensure kirimPresensi also uses >= 1 for showing the modal automatically after presensi
old_kirim = "if (!surveyFilled && pCount + 1 >= 3) {"
new_kirim = "if (!surveyFilled && pCount + 1 >= 1) {"
content = content.replace(old_kirim, new_kirim)


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("patched survey completely")
