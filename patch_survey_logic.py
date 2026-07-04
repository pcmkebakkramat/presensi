import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update close button of infoUpdateScreen
content = content.replace("onclick=\"closeFeatureModal('infoUpdateScreen')\"", "onclick=\"closeInfoUpdateAndCheckSurvey()\"")

js_logic = """
      const susQuestions = [
        "Saya berpikir akan sering menggunakan sistem ini.",
        "Saya merasa sistem ini terlalu rumit padahal dapat dibuat lebih sederhana.",
        "Saya merasa sistem ini mudah digunakan.",
        "Saya merasa butuh bantuan dari orang teknis untuk dapat menggunakan sistem ini.",
        "Saya menemukan bahwa berbagai macam fungsi dalam sistem ini terintegrasi dengan baik.",
        "Saya merasa ada banyak hal yang tidak konsisten dalam sistem ini.",
        "Saya merasa orang kebanyakan akan dapat mempelajari sistem ini dengan cepat.",
        "Saya merasa sistem ini sangat tidak praktis/susah digunakan.",
        "Saya merasa sangat yakin dapat menggunakan sistem ini.",
        "Saya harus belajar banyak hal terlebih dahulu sebelum saya dapat menggunakan sistem ini."
      ];
      
      const ratingQuestions = [
        "Bagaimana pengalaman Anda dengan fitur 'Jamaah Paling Aktif'?",
        "Bagaimana pengalaman Anda dengan fitur 'AUM Teraktif'?",
        "Bagaimana pengalaman Anda dengan fitur 'Daftar AUM'?",
        "Bagaimana pengalaman Anda dengan fitur 'Analitik Tren'?"
      ];

      function renderSurveyForm() {
        let susHtml = '';
        susQuestions.forEach((q, i) => {
           susHtml += `
            <div class="mb-4">
              <label class="form-label small fw-bold">${i+1}. ${q}</label>
              <div class="d-flex justify-content-between text-muted" style="font-size:0.75rem;">
                <span>Sangat Tidak Setuju</span>
                <span>Sangat Setuju</span>
              </div>
              <div class="d-flex justify-content-between mt-1">
                <div class="form-check form-check-inline m-0"><input class="form-check-input" type="radio" name="sus${i}" value="1" required></div>
                <div class="form-check form-check-inline m-0"><input class="form-check-input" type="radio" name="sus${i}" value="2" required></div>
                <div class="form-check form-check-inline m-0"><input class="form-check-input" type="radio" name="sus${i}" value="3" required></div>
                <div class="form-check form-check-inline m-0"><input class="form-check-input" type="radio" name="sus${i}" value="4" required></div>
                <div class="form-check form-check-inline m-0"><input class="form-check-input" type="radio" name="sus${i}" value="5" required></div>
              </div>
            </div>`;
        });
        document.getElementById('susQuestionsContainer').innerHTML = susHtml;
        
        let ratingHtml = '';
        ratingQuestions.forEach((q, i) => {
           ratingHtml += `
            <div class="mb-4">
              <label class="form-label small fw-bold">${i+1}. ${q}</label>
              <div class="d-flex justify-content-between text-muted" style="font-size:0.75rem;">
                <span>Sangat Buruk</span>
                <span>Sangat Baik</span>
              </div>
              <div class="d-flex justify-content-between mt-1">
                <div class="form-check form-check-inline m-0"><input class="form-check-input" type="radio" name="rating${i}" value="1" required></div>
                <div class="form-check form-check-inline m-0"><input class="form-check-input" type="radio" name="rating${i}" value="2" required></div>
                <div class="form-check form-check-inline m-0"><input class="form-check-input" type="radio" name="rating${i}" value="3" required></div>
                <div class="form-check form-check-inline m-0"><input class="form-check-input" type="radio" name="rating${i}" value="4" required></div>
                <div class="form-check form-check-inline m-0"><input class="form-check-input" type="radio" name="rating${i}" value="5" required></div>
              </div>
            </div>`;
        });
        document.getElementById('ratingQuestionsContainer').innerHTML = ratingHtml;
      }
      
      function checkOnboardingAndSurvey() {
        setTimeout(() => {
          let usageCount = parseInt(localStorage.getItem('app_usage_count') || '0');
          let surveyFilled = localStorage.getItem('has_filled_survey') === 'true';
          
          if(usageCount < 3) {
            localStorage.setItem('app_usage_count', usageCount + 1);
            openFeatureModal('infoUpdateScreen');
          } else if(!surveyFilled) {
            openSurveyModal();
          }
        }, 800);
      }

      function closeInfoUpdateAndCheckSurvey() {
         closeFeatureModal('infoUpdateScreen');
         let surveyFilled = localStorage.getItem('has_filled_survey') === 'true';
         if(!surveyFilled) {
            setTimeout(() => { openSurveyModal(); }, 500);
         }
      }
      
      function openSurveyModal() {
        openFeatureModal('susSurveyScreen');
        let today = new Date();
        let deadline = new Date('2026-08-01T00:00:00+07:00');
        if (today >= deadline) {
           document.getElementById('btnNantiSurvey').style.display = 'none';
        }
      }
      
      async function submitSurveyForm(e) {
         e.preventDefault();
         const btn = document.getElementById('btnSubmitSurvey');
         btn.disabled = true;
         btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Menyimpan...';
         
         let susData = [];
         for(let i=0; i<10; i++) {
             susData.push(document.querySelector(`input[name="sus${i}"]:checked`).value);
         }
         let ratingData = [];
         for(let i=0; i<4; i++) {
             ratingData.push(document.querySelector(`input[name="rating${i}"]:checked`).value);
         }
         let text1 = document.getElementById('surveyQ1').value;
         let text2 = document.getElementById('surveyQ2').value;
         
         let payload = {
             action: 'saveSurvey',
             username: CURRENT_USER.username,
             nama: CURRENT_USER.nama,
             sus: susData,
             rating: ratingData,
             q1: text1,
             q2: text2
         };
         
         try {
             let req = await fetch(SCRIPT_URL, { method: 'POST', body: JSON.stringify(payload) });
             let res = await req.json();
             if(res.status === 'success') {
                 localStorage.setItem('has_filled_survey', 'true');
                 alert("Terima kasih! Survei Anda berhasil dikirim.");
                 closeFeatureModal('susSurveyScreen');
             } else {
                 alert("Gagal mengirim survei. Silakan coba lagi.");
             }
         } catch(err) {
             alert("Terjadi kesalahan koneksi.");
         } finally {
             btn.disabled = false;
             btn.innerHTML = 'Kirim Survei';
         }
      }
      
      // Initial render on boot
      renderSurveyForm();
"""

content = content.replace("function showDashboard() {", js_logic + "\n      function showDashboard() {")
content = content.replace("if (navigator.geolocation) navigator.geolocation.watchPosition(updatePosisi, handleGpsError, { enableHighAccuracy: true });", "if (navigator.geolocation) navigator.geolocation.watchPosition(updatePosisi, handleGpsError, { enableHighAccuracy: true });\n        checkOnboardingAndSurvey();")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("survey logic patched")
