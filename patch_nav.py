with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix Truncation in detailScreen Title
content = content.replace(
    '<h6 class="m-0 fw-bold text-truncate" id="detailTitle" style="max-width: 250px;">Detail</h6>',
    '<h6 class="m-0 fw-bold" id="detailTitle" style="width: 75%; white-space: normal; line-height: 1.3; font-size: 0.95rem;">Detail</h6>'
)

# 2. Change detailScreen close button action
content = content.replace(
    '''<button class="btn-close-custom" onclick="closeFeatureModal('detailScreen')"><i class="bi bi-x"></i></button>''',
    '''<button class="btn-close-custom" onclick="closeDetailScreen()"><i class="bi bi-x"></i></button>'''
)

# 3. Add window.currentAumIndex and closeDetailScreen logic
nav_logic = """
            var currentAumIndex = null;

            function closeDetailScreen() {
                if (currentDetailType === 'user' && currentAumIndex !== null) {
                    showAumDetail(currentAumIndex);
                } else {
                    closeFeatureModal('detailScreen');
                    currentAumIndex = null;
                }
            }
"""

if "var currentDetailType =" in content:
    content = content.replace(
        "var currentDetailType = \"\";",
        "var currentDetailType = \"\";\n" + nav_logic
    )

# 4. Update showAumDetail to set currentAumIndex
if "function showAumDetail(index) {" in content:
    content = content.replace(
        "function showAumDetail(index) {",
        "function showAumDetail(index) {\n              currentAumIndex = index;"
    )

# 5. Update showUserDetail to clear currentAumIndex
if "function showUserDetail(index) {" in content:
    content = content.replace(
        "function showUserDetail(index) {",
        "function showUserDetail(index) {\n              currentAumIndex = null;"
    )

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Navigation stack patched.")
