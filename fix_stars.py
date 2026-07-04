import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update SUS HTML
old_sus = """              <div class="d-flex justify-content-between mt-1">
                <div class="form-check form-check-inline m-0"><input class="form-check-input" type="radio" name="sus${i}" value="1" required></div>
                <div class="form-check form-check-inline m-0"><input class="form-check-input" type="radio" name="sus${i}" value="2" required></div>
                <div class="form-check form-check-inline m-0"><input class="form-check-input" type="radio" name="sus${i}" value="3" required></div>
                <div class="form-check form-check-inline m-0"><input class="form-check-input" type="radio" name="sus${i}" value="4" required></div>
                <div class="form-check form-check-inline m-0"><input class="form-check-input" type="radio" name="sus${i}" value="5" required></div>
              </div>"""

new_sus = """              <div class="d-flex justify-content-between mt-1 text-center">
                <label class="form-check-label m-0" style="cursor:pointer;"><div class="small fw-bold text-dark" style="font-size:0.8rem;">1</div><input class="form-check-input mx-auto d-block mt-1" style="border:2px solid #94a3b8; width:1.2rem; height:1.2rem;" type="radio" name="sus${i}" value="1" required></label>
                <label class="form-check-label m-0" style="cursor:pointer;"><div class="small fw-bold text-dark" style="font-size:0.8rem;">2</div><input class="form-check-input mx-auto d-block mt-1" style="border:2px solid #94a3b8; width:1.2rem; height:1.2rem;" type="radio" name="sus${i}" value="2" required></label>
                <label class="form-check-label m-0" style="cursor:pointer;"><div class="small fw-bold text-dark" style="font-size:0.8rem;">3</div><input class="form-check-input mx-auto d-block mt-1" style="border:2px solid #94a3b8; width:1.2rem; height:1.2rem;" type="radio" name="sus${i}" value="3" required></label>
                <label class="form-check-label m-0" style="cursor:pointer;"><div class="small fw-bold text-dark" style="font-size:0.8rem;">4</div><input class="form-check-input mx-auto d-block mt-1" style="border:2px solid #94a3b8; width:1.2rem; height:1.2rem;" type="radio" name="sus${i}" value="4" required></label>
                <label class="form-check-label m-0" style="cursor:pointer;"><div class="small fw-bold text-dark" style="font-size:0.8rem;">5</div><input class="form-check-input mx-auto d-block mt-1" style="border:2px solid #94a3b8; width:1.2rem; height:1.2rem;" type="radio" name="sus${i}" value="5" required></label>
              </div>"""
content = content.replace(old_sus, new_sus)

# 2. Update Feature Rating HTML (Star Rating)
old_rating = """            <div class="mb-4">
              <label class="form-label small fw-bold">${i + 1}. ${q}</label>
              <div class="d-flex justify-content-between text-muted" style="font-size:0.75rem;">
                <span>Sangat Buruk</span>
                <span>Sangat Baik</span>
              </div>
              <div class="d-flex justify-content-between mt-1 text-center">
                <label class="form-check-label m-0" style="cursor:pointer;"><div class="small fw-bold text-dark" style="font-size:0.8rem;">1</div><input class="form-check-input mx-auto d-block mt-1" style="border:2px solid #94a3b8; width:1.2rem; height:1.2rem;" type="radio" name="rating${i}" value="1" required></label>
                <label class="form-check-label m-0" style="cursor:pointer;"><div class="small fw-bold text-dark" style="font-size:0.8rem;">2</div><input class="form-check-input mx-auto d-block mt-1" style="border:2px solid #94a3b8; width:1.2rem; height:1.2rem;" type="radio" name="rating${i}" value="2" required></label>
                <label class="form-check-label m-0" style="cursor:pointer;"><div class="small fw-bold text-dark" style="font-size:0.8rem;">3</div><input class="form-check-input mx-auto d-block mt-1" style="border:2px solid #94a3b8; width:1.2rem; height:1.2rem;" type="radio" name="rating${i}" value="3" required></label>
                <label class="form-check-label m-0" style="cursor:pointer;"><div class="small fw-bold text-dark" style="font-size:0.8rem;">4</div><input class="form-check-input mx-auto d-block mt-1" style="border:2px solid #94a3b8; width:1.2rem; height:1.2rem;" type="radio" name="rating${i}" value="4" required></label>
                <label class="form-check-label m-0" style="cursor:pointer;"><div class="small fw-bold text-dark" style="font-size:0.8rem;">5</div><input class="form-check-input mx-auto d-block mt-1" style="border:2px solid #94a3b8; width:1.2rem; height:1.2rem;" type="radio" name="rating${i}" value="5" required></label>
              </div>
            </div>"""

new_rating = """            <div class="mb-4 border p-3" style="border-radius:15px; background:#fff;">
              <label class="form-label small fw-bold text-center w-100 mb-1">${i + 1}. ${q}</label>
              <div class="star-rating mt-2">
                <input type="radio" id="star5_${i}" name="rating${i}" value="5" required /><label for="star5_${i}" title="Sangat Baik"><i class="bi bi-star-fill"></i></label>
                <input type="radio" id="star4_${i}" name="rating${i}" value="4" required /><label for="star4_${i}" title="Baik"><i class="bi bi-star-fill"></i></label>
                <input type="radio" id="star3_${i}" name="rating${i}" value="3" required /><label for="star3_${i}" title="Cukup"><i class="bi bi-star-fill"></i></label>
                <input type="radio" id="star2_${i}" name="rating${i}" value="2" required /><label for="star2_${i}" title="Buruk"><i class="bi bi-star-fill"></i></label>
                <input type="radio" id="star1_${i}" name="rating${i}" value="1" required /><label for="star1_${i}" title="Sangat Buruk"><i class="bi bi-star-fill"></i></label>
              </div>
              <div class="d-flex justify-content-between text-muted px-2 mt-1" style="font-size:0.7rem;">
                <span>Sangat Buruk</span>
                <span>Sangat Baik</span>
              </div>
            </div>"""
content = content.replace(old_rating, new_rating)

# 3. Add Star Rating CSS
css = """
    <style>
      .star-rating {
        display: flex;
        flex-direction: row-reverse;
        justify-content: center;
        gap: 5px;
      }
      .star-rating input { display: none; }
      .star-rating label { cursor: pointer; color: #cbd5e1; font-size: 2.2rem; margin: 0; transition: color 0.2s; }
      .star-rating input:checked ~ label,
      .star-rating label:hover,
      .star-rating label:hover ~ label { color: #f59e0b; }
    </style>
  """
content = content.replace("</head>", css + "</head>")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("patched stars")
