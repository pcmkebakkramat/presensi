with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# For each modal, I need to insert </div> before <div class="overlay-body"> if it's missing.
# Wait, let's just do a string replace since the pattern is very specific.

replacements = [
    (
        '''        </div>
        <div class="overlay-body">
          <div id="listPalingAktif" class="list-group">''',
        '''        </div>
      </div>
      <div class="overlay-body">
        <div id="listPalingAktif" class="list-group">'''
    ),
    (
        '''          </div>
          <div class="overlay-body">
            <div id="listAumTeraktif" class="list-group">''',
        '''          </div>
        </div>
        <div class="overlay-body">
          <div id="listAumTeraktif" class="list-group">'''
    ),
    (
        '''            </div>
            <div class="overlay-body">
              <div class="alert alert-light border small text-center mb-3"><i class="bi bi-info-circle"></i> Daftar Amal''',
        '''            </div>
          </div>
          <div class="overlay-body">
            <div class="alert alert-light border small text-center mb-3"><i class="bi bi-info-circle"></i> Daftar Amal'''
    ),
    (
        '''              </div>
              <div class="overlay-body">
                <div id="listDetail" class="list-group">''',
        '''              </div>
            </div>
            <div class="overlay-body">
              <div id="listDetail" class="list-group">'''
    )
]

# Let's actually use a regex or just rewrite the modal sections cleanly to fix the indentation as well.
