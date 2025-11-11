# Quickstart — Customer Feedback Portal
Generated: 2025-11-07

Prerequisites:
- Python 3.10+ installed
- Windows PowerShell (recommended) or bash

1. Create virtual environment and install minimal dependencies
```powershell
cd c:\10_workplace\AI_SK_CustomerFeedbackForm\CFF2
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install flask pytest black flake8 coverage
```

2. Initialize DB (example using sqlite)
```powershell
python - <<'PY'
import sqlite3, pathlib
root = pathlib.Path(r'c:\10_workplace\AI_SK_CustomerFeedbackForm\CFF2')
conn = sqlite3.connect(str(root / 'feedback.db'))
with open(str(root / '.specify/db/migrations/001_create_feedback_table.sql'),'r',encoding='utf-8') as f:
    conn.executescript(f.read())
conn.commit()
conn.close()
PY
```

3. Create initial operator account (one-off script)
```powershell
python - <<'PY'
import sqlite3, hashlib, os
from werkzeug.security import generate_password_hash
conn = sqlite3.connect('feedback.db')
c = conn.cursor()
# Example: create operator; change username/password after first login
c.execute("INSERT INTO operator (username,password_hash,display_name) VALUES (?, ?, ?)",
          ('operator','" + generate_password_hash('change-me') + "', 'Operator'))
conn.commit()
conn.close()
PY
```

4. Run dev server
```powershell
set FLASK_APP=app.py
set FLASK_ENV=development
flask run --port 5000
```

5. Run tests and lint
```powershell
pytest --maxfail=1 --disable-warnings -q
black --check .
flake8
```

Notes:
- Production: serve with a WSGI server behind a reverse proxy; ensure secure session cookie settings and HTTPS.
- CI: add GitHub Actions job to run black, flake8, pytest and fail the build on any issues.
