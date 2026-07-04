import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_logic = """
      function checkOnboardingAndSurvey() {
        setTimeout(() => {
          let usageCount = parseInt(localStorage.getItem('app_usage_count') || '0');
          let surveyFilled = localStorage.getItem('has_filled_survey') === 'true';
          let pCount = parseInt(localStorage.getItem('local_presensi_count') || '0');
          let today = new Date();
          let deadline = new Date('2026-08-01T00:00:00+07:00');
          
          if (!surveyFilled && (pCount >= 3 || today >= deadline)) {
             // Harus isi survey dulu, tidak bisa pakai aplikasi
             openSurveyModal(false);
          } else if (usageCount < 3) {
            localStorage.setItem('app_usage_count', usageCount + 1);
            openFeatureModal('infoUpdateScreen');
          }
        }, 800);
      }

      function closeInfoUpdateAndCheckSurvey() {
        closeFeatureModal('infoUpdateScreen');
        // Jangan munculkan survey di sini sesuai instruksi: "jangan munculkan survey langsung setelah pop up info update ditutup"
      }

      function openSurveyModal(isLogout) {
        openFeatureModal('susSurveyScreen');
        let today = new Date();
        let deadline = new Date('2026-08-01T00:00:00+07:00');
        let pCount = parseInt(localStorage.getItem('local_presensi_count') || '0');
        
        let isForced = (today >= deadline || pCount >= 3);
        let btnNanti = document.getElementById('btnNantiSurvey');
        
        if (isForced) {
          btnNanti.style.display = 'none';
        } else {
          btnNanti.style.display = 'inline-block';
          btnNanti.onclick = function() {
            closeFeatureModal('susSurveyScreen');
            if (isLogout) {
               localStorage.removeItem("PCM_USER"); CURRENT_USER = null; showLogin();
            }
          };
        }
      }
"""

content = re.sub(
    r"function checkOnboardingAndSurvey\(\) \{.*?\n      function openSurveyModal\(\) \{.*?\n        \}\n      \}",
    new_logic.strip(),
    content,
    flags=re.DOTALL
)

# Update doLogout
content = content.replace(
    """function doLogout() { localStorage.removeItem("PCM_USER"); CURRENT_USER = null; showLogin(); }""",
    """function doLogout() { 
        let surveyFilled = localStorage.getItem('has_filled_survey') === 'true';
        if (!surveyFilled) {
            openSurveyModal(true);
        } else {
            localStorage.removeItem("PCM_USER"); CURRENT_USER = null; showLogin(); 
        }
      }"""
)

# Update savePresensi to increment local_presensi_count and show survey
content = content.replace(
    "let res = await req.json(); loading(false); alert(res.message); if (res.status === 'success') { closePresensiMode(); loadDashboardData(); }",
    """let res = await req.json(); loading(false); alert(res.message); 
          if (res.status === 'success') { 
            closePresensiMode(); loadDashboardData(); 
            let pCount = parseInt(localStorage.getItem('local_presensi_count') || '0');
            localStorage.setItem('local_presensi_count', pCount + 1);
            let surveyFilled = localStorage.getItem('has_filled_survey') === 'true';
            if (!surveyFilled) {
               setTimeout(() => { openSurveyModal(false); }, 1000);
            }
          }"""
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("patched")
