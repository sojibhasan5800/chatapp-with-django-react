<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Real-Time Chat Application — Django + React</title>

  <!-- Simple styling for clean HR-friendly layout -->
  <style>
    :root{
      --bg:#0f1724; --card:#0b1220; --muted:#94a3b8; --accent:#60a5fa; --glass: rgba(255,255,255,0.03);
      --maxw:900px;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
      color:#e6eef8;
    }
    html,body{height:100%;margin:0;background:linear-gradient(180deg,#071129 0%, #041024 100%);-webkit-font-smoothing:antialiased;}
    .wrap{max-width:var(--maxw);margin:36px auto;padding:28px;background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));border-radius:12px;box-shadow:0 8px 30px rgba(2,6,23,0.8);border:1px solid rgba(255,255,255,0.03);}
    header{display:flex;align-items:center;gap:18px;margin-bottom:18px;}
    .logo{width:72px;height:72px;border-radius:12px;background:linear-gradient(135deg,var(--accent),#7c3aed);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:22px;color:#021124;}
    h1{margin:0;font-size:22px}
    p.lead{margin:6px 0 0;color:var(--muted)}
    .badges{display:flex;gap:8px;margin-top:12px;flex-wrap:wrap}
    .section{margin-top:20px;padding:18px;border-radius:10px;background:linear-gradient(180deg,var(--glass),transparent);border:1px solid rgba(255,255,255,0.02)}
    h2{margin:0 0 8px;font-size:16px;color:var(--accent)}
    ul{margin:8px 0 0 20px;color:var(--muted)}
    pre{background:#071225;padding:14px;border-radius:8px;overflow:auto;color:#cde7ff;font-size:13px}
    code{font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, "Roboto Mono", monospace}
    .cols{display:grid;grid-template-columns:1fr 1fr;gap:14px}
    .full{grid-column:1/-1}
    .contacts{display:flex;gap:12px;align-items:center}
    a{color:var(--accent);text-decoration:none}
    .muted{color:var(--muted);font-size:14px}
    .screenshot-placeholder{height:180px;border-radius:8px;border:2px dashed rgba(255,255,255,0.03);display:flex;align-items:center;justify-content:center;color:var(--muted);background:linear-gradient(180deg, rgba(255,255,255,0.01), transparent)}
    footer{margin-top:18px;padding-top:12px;border-top:1px solid rgba(255,255,255,0.02);text-align:center;color:var(--muted);font-size:13px}
    @media (max-width:700px){.cols{grid-template-columns:1fr}.logo{width:56px;height:56px}}
  </style>
</head>
<body>
  <div class="wrap" role="main">
    <header>
      <div class="logo">Chat</div>
      <div>
        <h1>💬 Real-Time Chat Application</h1>
        <p class="lead"><strong>Django (Backend)</strong> + <strong>React (Frontend)</strong> — Real-time messaging, online & typing indicators, JWT auth.</p>
        <div class="badges">
          <!-- Shields badges (displayed as images via shields.io) -->
          <img alt="Python" src="https://img.shields.io/badge/Python-3.8%2B-blue?style=flat&logo=python" />
          <img alt="Django" src="https://img.shields.io/badge/Django-5.x-green?style=flat&logo=django" />
          <img alt="React" src="https://img.shields.io/badge/React-18.x-61DBFB?style=flat&logo=react&logoColor=black" />
          <img alt="Redis" src="https://img.shields.io/badge/Redis-required-E83A25?style=flat&logo=redis" />
          <img alt="PostgreSQL" src="https://img.shields.io/badge/Postgres-optional-316192?style=flat&logo=postgresql" />
          <img alt="WebSocket" src="https://img.shields.io/badge/WebSocket-%E2%9C%93-6EE7B7?style=flat" />
        </div>
      </div>
    </header>

    <section class="section">
      <h2>🚀 Overview</h2>
      <p class="muted">This repository contains a complete Real-Time Chat System using Django (Channels + Daphne) for the backend and React for the frontend. It supports WebSocket-based messaging, authentication (JWT), online/typing indicators, message persistence, and a responsive UI.</p>
    </section>

    <div class="cols">
      <section class="section">
        <h2>✨ Key Features — Backend</h2>
        <ul>
          <li><strong>WebSocket Integration:</strong> Django Channels for realtime connections.</li>
          <li><strong>Redis:</strong> Message broker & channel layer for async events.</li>
          <li><strong>Daphne:</strong> ASGI server to handle WebSocket + HTTP traffic.</li>
          <li><strong>Message Persistence:</strong> PostgreSQL / SQLite via Django ORM.</li>
          <li><strong>Authentication:</strong> Token/JWT based secure auth.</li>
          <li><strong>Online & Typing Indicators:</strong> Real-time presence & typing updates.</li>
          <li><strong>Role-based Access:</strong> Users only access their conversations.</li>
        </ul>
      </section>

      <section class="section">
        <h2>✨ Key Features — Frontend</h2>
        <ul>
          <li><strong>Real-Time Updates:</strong> WebSocket client for instant messaging.</li>
          <li><strong>Responsive UI:</strong> Clean interface built with React.</li>
          <li><strong>Online Status:</strong> View active users in a conversation.</li>
          <li><strong>Typing Indicators:</strong> Live feedback when someone types.</li>
          <li><strong>JWT Auth:</strong> Secure login & session handling.</li>
          <li><strong>Error Handling:</strong> Graceful network/server fallback.</li>
        </ul>
      </section>

      <section class="section full">
        <h2>📂 Project Structure</h2>
        <pre><code>
Backend/
├─ chatsystemproj/        # Django project (settings, asgi.py, urls)
├─ chatapp/               # App: models, views, routing, consumers
├─ consumers.py           # WebSocket consumers (messages, typing, presence)
├─ requirements.txt
Frontend/
├─ frontend/              # React app
│  ├─ src/
│  │  ├─ components/
│  │  │  ├─ Conversation.jsx
│  │  │  ├─ ChatList.jsx
│  │  │  ├─ Login.jsx
│  │  │  └─ Register.jsx
│  │  ├─ auth.js
│  │  └─ index.css
        </code></pre>
      </section>

      <section class="section">
        <h2>⚙️ Getting Started — Prerequisites</h2>
        <ul>
          <li>Python 3.8+</li>
          <li>Node.js 14+</li>
          <li>Redis (for Channels layer)</li>
          <li>PostgreSQL (recommended) or SQLite (local)</li>
        </ul>
      </section>

      <section class="section">
        <h2>🔧 Backend Setup</h2>
        <pre><code>
# Create virtual environment
python -m venv env

# Activate it
# Windows:
.\env\Scripts\activate
# macOS / Linux:
source env/bin/activate

# Move to Django project
cd chatsystemproj

# Install deps
pip install -r requirements.txt

# Migrate DB
python manage.py migrate

# Start development server
python manage.py runserver

# Start Daphne (for WebSocket support)
daphne -b 0.0.0.0 -p 8000 chatsystemproj.asgi:application
        </code></pre>
      </section>

      <section class="section">
        <h2>🔧 Frontend Setup</h2>
        <pre><code>
# Move to frontend
cd frontend

# Install node modules
npm install

# Run dev server
npm run dev
        </code></pre>
      </section>

      <section class="section full">
        <h2>🔑 Core Components</h2>
        <div class="cols">
          <div>
            <h3 class="muted">Backend</h3>
            <ul>
              <li><strong>WebSocket Consumers:</strong> Broadcast messages, typing events, presence updates.</li>
              <li><strong>REST API:</strong> Fetch conversations, create messages, user auth.</li>
            </ul>
          </div>
          <div>
            <h3 class="muted">Frontend</h3>
            <ul>
              <li><strong>WebSocket Client:</strong> Connects to Channels; handles incoming/outgoing events.</li>
              <li><strong>Message List + UI:</strong> Sent vs received styling, scrolling, timestamps.</li>
              <li><strong>Typing Indicator:</strong> Shows who is typing in the conversation.</li>
            </ul>
          </div>
        </div>
      </section>

      <section class="section">
        <h2>💡 Future Enhancements</h2>
        <ul>
          <li>Message deletion / edit</li>
          <li>Read receipts (seen/unseen)</li>
          <li>Group chat support</li>
          <li>File / image attachments</li>
        </ul>
      </section>

      <section class="section full">
        <h2>📸 Screenshots</h2>
        <div class="screenshot-placeholder">Add UI screenshots here (PNG/JPG). Screenshot images help HR visualize the product.</div>
      </section>

      <section class="section full">
        <h2>👨‍💻 Developed By</h2>
        <div style="display:flex;align-items:center;gap:14px;justify-content:space-between;flex-wrap:wrap">
          <div>
            <strong>Md Sojib Hasan</strong><br>
            Full-Stack Developer — Django &amp; React<br>
            <div class="contacts" style="margin-top:8px">
              <a href="https://github.com/sojibhasan5800" target="_blank" rel="noopener">GitHub</a> •
              <a href="https://www.linkedin.com/in/sojibhasan5800" target="_blank" rel="noopener">LinkedIn</a> •
              <a href="mailto:sojibhasan5800@gmail.com">sojibhasan5800@gmail.com</a>
            </div>
          </div>
          <div class="muted" style="text-align:right">Want this README as markdown instead? You can convert this HTML to markdown or keep as preview file for HRs.</div>
        </div>
      </section>
    </div>

    <footer>
      <div>© <span id="year"></span> Real-Time Chat Application — Built with Django & React</div>
    </footer>
  </div>

  <script>
    // small script for year
    document.getElementById('year').textContent = new Date().getFullYear();
  </script>
</body>
</html>
