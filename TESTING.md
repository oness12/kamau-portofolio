Playwright tests for Portfolio

Prerequisites
- Node.js (v16+ recommended)
- Python (to run the Flask app) and dependencies installed (see `requirements.txt`)

Install & run
1. Install dev deps and Playwright browsers:

```bash
npm install
npx playwright install
```

2. Start the Flask app in a separate terminal (default host/port used in tests):

```bash
python app.py
# or if you use flask CLI
# set FLASK_APP=app.py
# flask run
```

3. Run tests (headless):

```bash
npm test
```

4. Run tests in headed mode (useful for debugging):

```bash
npm run test:headed
```

Notes
- The tests target `http://127.0.0.1:5000` by default; change `BASE_URL` env var to override.
- If your app uses a different startup command, update `tests/playwright.config.js` or start the server manually before running tests.
 
Environment variables
- To change the admin PIN or the Flask secret key for production, set these env vars before starting the app:

```bash
export ADMIN_PIN=8154
export SECRET_KEY="your-production-secret"
# On Windows (PowerShell):
# $env:ADMIN_PIN = '8154'
# $env:SECRET_KEY = 'your-production-secret'
```

Keep secrets out of source control and use secure environment management for deployed environments.
