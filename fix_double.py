import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update kirimAbsen to disable btnKirim immediately
old_kirim = """      async function kirimAbsen() {
        var kes = document.getElementById('kesimpulan').value; if (!kes) return alert("Isi kesimpulan");
        loading(true);
        var cvs = document.getElementById('canvas'); cvs.width = video.videoWidth; cvs.height = video.videoHeight;"""

new_kirim = """      async function kirimAbsen() {
        var kes = document.getElementById('kesimpulan').value; if (!kes) return alert("Isi kesimpulan");
        var btnKirim = document.getElementById('btnKirim');
        btnKirim.disabled = true;
        btnKirim.innerHTML = '<span class="spinner-border spinner-border-sm"></span> MENGIRIM...';
        loading(true);
        var cvs = document.getElementById('canvas'); cvs.width = video.videoWidth; cvs.height = video.videoHeight;"""
content = content.replace(old_kirim, new_kirim)

# 2. Update kirimAbsen catch block to re-enable btnKirim
old_catch = """        } catch (e) { loading(false); alert(e); }
      }"""
new_catch = """        } catch (e) { 
          loading(false); alert(e); 
          var btnKirim = document.getElementById('btnKirim');
          btnKirim.disabled = false;
          btnKirim.innerHTML = 'KIRIM DATA';
        }
      }"""
content = content.replace(old_catch, new_catch)

# 3. Update kirimAbsen success block to restore btnKirim (since it might be reused without reload) and save last_presensi_date
old_success = """          if (res.status === 'success') {
            closePresensiMode(); loadDashboardData();
            let pCount = parseInt(localStorage.getItem('local_presensi_count') || '0');"""
new_success = """          if (res.status === 'success') {
            var btnKirim = document.getElementById('btnKirim');
            btnKirim.disabled = false;
            btnKirim.innerHTML = 'KIRIM DATA';
            var today = new Date();
            var todayStr = today.getFullYear() + "-" + (today.getMonth()+1) + "-" + today.getDate();
            localStorage.setItem('last_presensi_date', todayStr);
            isAlreadyPresent = true;
            validateButtonState();
            closePresensiMode(); loadDashboardData();
            let pCount = parseInt(localStorage.getItem('local_presensi_count') || '0');"""
content = content.replace(old_success, new_success)

# 4. Update checkTodayStatus to use localStorage AND history
old_check = """      function checkTodayStatus(history) {
        var today = new Date(); isAlreadyPresent = false;
        if (history.length > 0) {
          var lastRaw = new Date(history[0].tanggalRaw);
          if (lastRaw.getDate() === today.getDate() && lastRaw.getMonth() === today.getMonth() && lastRaw.getFullYear() === today.getFullYear()) isAlreadyPresent = true;
        }
        validateButtonState();
      }"""
new_check = """      function checkTodayStatus(history) {
        var today = new Date(); 
        var todayStr = today.getFullYear() + "-" + (today.getMonth()+1) + "-" + today.getDate();
        isAlreadyPresent = (localStorage.getItem('last_presensi_date') === todayStr);
        if (history.length > 0) {
          var lastRaw = new Date(history[0].tanggalRaw);
          if (lastRaw.getDate() === today.getDate() && lastRaw.getMonth() === today.getMonth() && lastRaw.getFullYear() === today.getFullYear()) {
             isAlreadyPresent = true;
             localStorage.setItem('last_presensi_date', todayStr);
          }
        }
        validateButtonState();
      }"""
content = content.replace(old_check, new_check)


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("patched double presensi")
