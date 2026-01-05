import os
import zipfile

# -------------------------------------------------------------------------
# FILE CONTENT DEFINITIONS
# -------------------------------------------------------------------------

# 1. README.md
readme_content = """# Gold Guard Network Defense 🛡️

A heuristic-based network threat neutralizer and automated filter assembler. 
This system uses entropic randomization to detect anomalies and compiles 
firewall rules in real-time.

## Features
- **Active Threat Response**: Auto-quarantine of high-entropy payloads.
- **Visual Telemetry**: Real-time canvas-based spectrograms and heatmaps.
- **Rule Forge**: Python-based logic for compiling network policies from neutralized threats.

## Setup
1. Unzip the archive.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the server: `python app.py`
4. Navigate to `http://localhost:5000`
"""

# 2. requirements.txt
requirements_content = """flask==3.0.0
numpy==1.26.0
"""

# 3. app.py (Flask Server)
app_py_content = """from flask import Flask, render_template, jsonify
import sys
import os

# Ensure src module can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.threat_engine import ThreatEngine
from src.rule_forge import RuleForge

app = Flask(__name__)
engine = ThreatEngine()
forge = RuleForge()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/forge')
def filter_assembler():
    return render_template('forge.html')

@app.route('/api/threat/spawn')
def api_spawn():
    threat = engine.spawn_threat()
    return jsonify(threat)

@app.route('/api/rule/compile', methods=['POST', 'GET'])
def api_compile():
    # Simulating a threat passed to the compiler
    dummy_threat = engine.spawn_threat()
    rule = forge.compile_rule(dummy_threat)
    return jsonify(rule)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
"""

# 4. src/__init__.py
init_py_content = ""

# 5. src/threat_engine.py
threat_engine_content = """import random
import uuid
import time

class ThreatEngine:
    THREAT_TYPES = ['Virus', 'Phishing Link', 'Trojan', 'Ransomware', 'Malware', 'Spyware', 'Exploit']
    CODENAMES = ['PAYLOAD', 'INJECT', 'CLICK_FRAUD', 'DROPBEAR', 'NIGHTCRAWL', 'SILENT_NOMAD', 'GOLDEN_EGG']

    @staticmethod
    def generate_ip():
        return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

    @staticmethod
    def generate_payload(length=32):
        return ' '.join([f"{random.randint(0, 255):02x}" for _ in range(length)])

    def spawn_threat(self):
        threat_id = str(uuid.uuid4())[:8].upper()
        t_type = random.choice(self.THREAT_TYPES)
        name = random.choice(self.CODENAMES)
        base_score = random.randint(10, 98)
        
        return {
            "id": threat_id,
            "name": name,
            "type": t_type,
            "score": base_score,
            "src": self.generate_ip(),
            "dst": "192.168.1.100",
            "payload": self.generate_payload(),
            "timestamp": time.time(),
            "status": "active"
        }
"""

# 6. src/rule_forge.py
rule_forge_content = """import uuid
import random

class RuleForge:
    def __init__(self):
        self.rules_db = []

    def compile_rule(self, threat_data):
        sig_fragment = threat_data['payload'][:12].replace(' ', '').upper()
        signature = f"SIG_{sig_fragment}_{uuid.uuid4().hex[:4].upper()}"

        rule = {
            "rule_id": f"R-{uuid.uuid4().hex[:4].upper()}",
            "match": {
                "type": threat_data['type'],
                "signature": signature,
                "source_ip": threat_data['src']
            },
            "action": "DROP",
            "priority": random.randint(100, 999),
            "created_at": "timestamp_now"
        }
        
        self.rules_db.append(rule)
        return rule
"""

# 7. templates/index.html (Source: entropic randomizer.html)
# We use raw strings r''' ''' to handle the HTML/JS content safely
html_index_content = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>ENTROPIC RANDOMIZER</title>
<style>
  :root{ --bg:#000; --panel:#0b0b0b; --gold:#ffcc33; --muted:#3b2e00; --glass:rgba(255,204,51,0.04); --danger:#ff4444; font-family:Inter,system-ui,Segoe UI,Roboto,Arial; }
  html,body{height:100%;margin:0;background:linear-gradient(180deg,#000 0%, #070601 60%);color:var(--gold);}
  .app{padding:14px;display:grid;grid-template-columns:320px 1fr 420px;grid-template-rows:72px 1fr;gap:12px;height:100vh;box-sizing:border-box}
  header{grid-column:1/-1;display:flex;align-items:center;gap:12px;padding:12px;border-radius:10px;background:linear-gradient(90deg, rgba(255,204,51,0.03), rgba(255,204,51,0.01));border:1px solid rgba(255,204,51,0.06)}
  .brand h1{margin:0;font-size:18px}
  .panel{background:linear-gradient(180deg, rgba(255,204,51,0.02), rgba(255,204,51,0.01));border:1px solid rgba(255,204,51,0.04);padding:12px;border-radius:10px}
  .left{overflow:auto}
  .entropy-meter{height:180px;display:flex;flex-direction:column;align-items:center;justify-content:center}
  .gauge{width:160px;height:160px;border-radius:50%;background:conic-gradient(var(--gold) 0deg, rgba(255,204,51,0.06) 120deg, rgba(0,0,0,0.6) 240deg);display:flex;align-items:center;justify-content:center;box-shadow:0 8px 40px rgba(255,204,51,0.02) inset}
  .gauge .val{font-size:22px;font-weight:700;color:#fff}
  .small{font-size:12px;color:#d9c37a}

  .filter-ui{display:flex;flex-direction:column;gap:8px;margin-top:12px}
  .filter-row{display:flex;gap:8px;align-items:center}
  .chip{padding:6px 8px;border-radius:8px;border:1px solid rgba(255,204,51,0.06);background:rgba(255,204,51,0.02);font-size:12px}

  .center{display:grid;grid-template-rows:1fr 220px;gap:12px}
  .canvas-wrap{display:flex;gap:12px}
  canvas{border-radius:8px;background:linear-gradient(180deg, rgba(0,0,0,0.3), rgba(0,0,0,0.6));}
  .hexdump{font-family:monospace;background:linear-gradient(180deg, rgba(255,204,51,0.02), rgba(255,204,51,0.01));padding:10px;border-radius:8px;height:220px;overflow:auto;color:#e9d99b;font-size:12px}

  .right{display:flex;flex-direction:column;gap:12px;overflow:auto}
  .streams{display:flex;flex-direction:column;gap:8px}
  .stream{height:72px;border-radius:8px;padding:8px;font-family:monospace;background:linear-gradient(180deg, rgba(255,204,51,0.01), rgba(255,204,51,0.02));border:1px solid rgba(255,204,51,0.04);}

  .network-map{height:260px;border-radius:8px;overflow:hidden}
  .threats{display:flex;flex-direction:column;gap:8px}
  .threat{display:flex;justify-content:space-between;align-items:center;padding:8px;border-radius:8px;background:linear-gradient(180deg, rgba(0,0,0,0.18), rgba(0,0,0,0.28));border:1px solid rgba(255,204,51,0.04);font-family:monospace}
  .status{font-weight:700;padding:6px 8px;border-radius:6px}
  .status.active{background:rgba(255,68,68,0.12);color:var(--danger);border:1px solid rgba(255,68,68,0.12)}
  .status.killed{background:rgba(255,204,51,0.12);color:var(--gold);border:1px solid rgba(255,204,51,0.12)}

  footer{grid-column:1/-1;font-size:12px;color:#b79a3b;display:flex;justify-content:space-between;align-items:center}
  body::after{content:"";position:fixed;inset:0;pointer-events:none;background-image:linear-gradient(0deg, rgba(255,204,51,0.02) 1px, transparent 1px),linear-gradient(90deg, rgba(255,204,51,0.02) 1px, transparent 1px);background-size:160px 160px,160px 160px;opacity:0.08}
  @media (max-width:1100px){.app{grid-template-columns:1fr;grid-template-rows:72px auto auto;}}
</style>
</head>
<body>
<div class="app">
  <header>
    <div style="display:flex;align-items:center;gap:12px">
      <svg width="44" height="44" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="1" y="1" width="22" height="22" rx="4" stroke="#ffcc33" stroke-opacity="0.18" stroke-width="1.6"/><path d="M5 12h14M12 5v14" stroke="#ffcc33" stroke-width="1.6" stroke-linecap="round"/></svg>
    </div>
    <div class="brand">
      <h1>ENTROPIC NEUTRALIZER</h1>
      <div style="font-size:12px;color:#d9c37a">Active threat response</div>
    </div>
    <div style="margin-left:auto;display:flex;gap:10px;align-items:center">
      <div class="chip">Mode: AUTO-QUARANTINE</div>
      <div class="chip">Policy: AGGRESSIVE</div>
      <div class="chip">Threat Pool • live</div>
    </div>
  </header>
  <aside class="left panel">
    <div class="entropy-meter">
      <div class="gauge" id="gauge"><div class="val" id="gaugeVal">--%</div></div>
      <div class="small">Entropy collected</div>
    </div>
    <div class="filter-ui">
      <div style="font-size:13px;color:#f0db9a">Auto Threat Filter</div>
      <div class="filter-row"><div class="chip">SRC: any</div><div class="chip">DST: any</div></div>
      <div class="filter-row"><div class="chip">PROTO: HTTP/SMTP/FILE</div><div class="chip">SCAN: signature + heuristic</div></div>
      <div style="margin-top:8px;font-size:12px;color:#e3d49c">Recent Actions</div>
      <div style="display:flex;flex-direction:column;gap:6px;margin-top:6px">
        <div style="font-size:12px;color:#e9d99b" id="recent1">- Initializing scanners...</div>
        <div style="font-size:12px;color:#e9d99b" id="recent2">- Network probes active</div>
      </div>
    </div>
  </aside>
  <main class="center">
    <div style="display:flex;gap:12px;align-items:stretch">
      <div class="panel" style="flex:1;min-width:420px;position:relative;overflow:hidden">
        <canvas id="specCanvas" width="880" height="360" style="display:block"></canvas>
        <canvas id="explodeCanvas" width="880" height="360" style="position:absolute;left:0;top:0;pointer-events:none"></canvas>
      </div>
      <div style="width:360px;display:flex;flex-direction:column;gap:12px">
        <div class="panel" style="height:160px;display:flex;flex-direction:column;gap:6px;">
          <div style="display:flex;justify-content:space-between;align-items:center"><strong>Active Threats</strong><div style="font-size:12px;color:#e8d48a" id="threatCount">--</div></div>
          <div class="threats" id="threatList" style="overflow:auto;max-height:110px"></div>
        </div>
        <div class="panel" style="height:160px;display:flex;flex-direction:column;">
          <strong style="font-size:13px">Quarantine Queue</strong>
          <div id="queue" style="margin-top:8px;font-family:monospace;color:#e9d99b;min-height:80px">(empty)</div>
        </div>
      </div>
    </div>
    <div style="display:flex;gap:12px">
      <div class="panel hexdump" style="flex:1">
        <div style="display:flex;justify-content:space-between;align-items:center"><strong>Threat Feed (sample payloads)</strong><div style="font-size:12px;color:#e8d48a" id="poolSize">-- items</div></div>
        <pre id="feed" style="margin-top:8px;white-space:pre-wrap;line-height:1.2;color:#f6e9b1"></pre>
      </div>
      <div class="panel" style="width:320px;display:flex;flex-direction:column;gap:8px;">
        <div style="display:flex;justify-content:space-between;align-items:center"><strong>Threat Types</strong><div style="font-size:12px;color:#e8d48a" id="typeLabel">--</div></div>
        <canvas id="pieKill" width="320" height="160"></canvas>
      </div>
    </div>
  </main>
  <aside class="right panel">
    <div style="display:flex;justify-content:space-between;align-items:center"><strong>Incident Timeline</strong><div style="font-size:12px;color:#e8d48a">actions • auto</div></div>
    <div style="margin-top:8px;overflow:auto;max-height:300px;font-family:monospace;color:#e9d99b" id="timeline">- system boot</div>
    <div style="margin-top:12px">
      <button id="panic" style="background:transparent;border:1px solid rgba(255,204,51,0.08);padding:8px 10px;border-radius:8px;color:var(--gold);cursor:pointer">TRIGGER FULL SWEEP</button>
    </div>
  </aside>
  <footer>
    <div>active neutralizer</div>
    <div id="time" style="opacity:0.8"></div>
  </footer>
</div>
<script>
// We can now fetch real data from our Python backend or use simulation
const rand = (a=0,b=1)=>Math.random()*(b-a)+a; const rint = (a,b)=>Math.floor(rand(a,b+1));
const threats = [];
const threatTypes = ['Virus','Phishing Link','Trojan','Ransomware','Malware','Spyware','Exploit'];

const threatList = document.getElementById('threatList');
const threatCount = document.getElementById('threatCount');
const queueEl = document.getElementById('queue');
const feed = document.getElementById('feed');
const timeline = document.getElementById('timeline');
const pieKill = document.getElementById('pieKill'); const pkctx = pieKill.getContext('2d');
const specCanvas = document.getElementById('specCanvas'); const sctx = specCanvas.getContext('2d');
const explodeCanvas = document.getElementById('explodeCanvas'); const ectx = explodeCanvas.getContext('2d');

// Particles
let particles = [];
function spawnExplosion(x,y,color){
  for(let i=0;i<40;i++){ particles.push({x,y,vx:rand(-3,3),vy:rand(-4,1),life:rand(30,80),col:color}); }
}
function updateParticles(){ ectx.clearRect(0,0,explodeCanvas.width,explodeCanvas.height); for(let i=particles.length-1;i>=0;i--){ const p=particles[i]; p.x += p.vx; p.y += p.vy; p.vy += 0.12; p.life--; ectx.globalAlpha = Math.max(0, p.life/80); ectx.fillStyle = p.col; ectx.fillRect(p.x,p.y,2,2); if(p.life<=0) particles.splice(i,1); } ectx.globalAlpha=1; }

function createThreat(){
    // Use the backend API
    fetch('/api/threat/spawn').then(r=>r.json()).then(t=>{
        threats.push(t); pushFeed(t); renderThreats();
    });
}

function pushFeed(t){ const line = `[${new Date(t.timestamp*1000).toLocaleTimeString()}] DETECTED ${t.type} ${t.name} @ ${t.src} -> ${t.dst} • score=${t.score}%\n${t.payload}\n\n`; feed.textContent = line + feed.textContent; timeline.innerHTML = `- ${new Date().toLocaleTimeString()} DETECTED ${t.type} ${t.id}<br>` + timeline.innerHTML; }

function renderThreats(){ threatList.innerHTML=''; threats.slice().reverse().forEach(t=>{ const el = document.createElement('div'); el.className='threat'; el.innerHTML = `<div style="display:flex;flex-direction:column"><div style="font-size:13px">${t.name} (${t.id})</div><div style="font-size:11px;color:#d9c37a">${t.type} • ${t.src}</div></div><div style="display:flex;flex-direction:column;align-items:flex-end"><div class="status ${t.status=='active'?'active':'killed'}">${t.status.toUpperCase()}</div><div style="font-size:11px;color:#e9d99b;margin-top:6px">${t.score}%</div></div>`; threatList.appendChild(el); }); threatCount.textContent = threats.filter(t=>t.status==='active').length + ' / ' + threats.length; }

function neutralize(){
    const active = threats.filter(t=>t.status==='active');
    if(active.length===0) return;
    active.sort((a,b)=>b.score-a.score); const t = active[0];
    t.status='killed';
    renderThreats();
    queueEl.textContent = `QUARANTINED: ${t.name} (${t.id}) — ${t.type}`;
    // Notify Backend (Forge)
    fetch('/api/rule/compile', {method:'POST'});
    
    const rect = specCanvas.getBoundingClientRect(); const x = rand(100, rect.width-100); const y = rand(40, rect.height-40); spawnExplosion(x,y,'rgba(255,204,51,0.95)');
}

function drawSpec(){ const w=specCanvas.width, h=specCanvas.height; sctx.fillStyle='rgba(0,0,0,0.14)'; sctx.fillRect(0,0,w,h); const img = sctx.getImageData(2,0,w-2,h); sctx.putImageData(img,0,0); for(let y=0;y<h;y++){ const intensity = Math.floor(60 + 140 * Math.random()*Math.abs(Math.sin(y/20 + Date.now()/800))); sctx.fillStyle = `rgba(${intensity},${Math.floor(intensity*0.85)},${Math.floor(intensity*0.3)},0.9)`; sctx.fillRect(w-2,y,2,1); } }

function drawPie(){ pkctx.clearRect(0,0,pieKill.width,pieKill.height); const cx = pieKill.width/2, cy=pieKill.height/2, r=60; const counts = {}; threatTypes.forEach(t=>counts[t]=0); threats.forEach(t=>{ if(t.status==='killed') counts[t.type]++; }); const vals = threatTypes.map(t=>counts[t]); const total = vals.reduce((a,b)=>a+b,0) || 1; let start = -Math.PI/2; for(let i=0;i<threatTypes.length;i++){ const ang = (vals[i]/total)*(Math.PI*2); pkctx.beginPath(); pkctx.moveTo(cx,cy); pkctx.arc(cx,cy,r,start,start+ang); pkctx.closePath(); pkctx.fillStyle = `rgba(255,204,51,${0.06 + (i/12)})`; pkctx.fill(); start += ang; } }

setInterval(()=>{ if(Math.random()<0.8) createThreat(); if(Math.random()<0.55) neutralize(); renderThreats(); drawPie(); }, 900);
function loop(){ drawSpec(); updateParticles(); requestAnimationFrame(loop); }
loop();

// dpi fix
function fixDPI(canvas){ const dpr = window.devicePixelRatio || 1; const rect = canvas.getBoundingClientRect(); canvas.width = rect.width * dpr; canvas.height = rect.height * dpr; const ctx = canvas.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0); }
[specCanvas, explodeCanvas, pieKill].forEach(c=>{ c.style.width = c.width + 'px'; c.style.height = c.height + 'px'; fixDPI(c); });

setInterval(()=>{ document.getElementById('time').textContent = new Date().toLocaleString(); }, 1000);
</script>
</body>
</html>
'''

# 8. templates/forge.html (Source: filter assembler.html)
html_forge_content = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>FILTER ASSEMBLER</title>
<style>
  :root{ --bg:#ffffff; --panel:#fbfaf8; --gold:#c99a2e; --muted:#f0e9e0; --accent:#b88613; --glass: rgba(200,150,30,0.06); font-family:Inter, system-ui, -apple-system, 'Segoe UI', Roboto, Arial; }
  html,body{height:100%;margin:0;background:linear-gradient(180deg,#ffffff 0%, #f7f5f2 60%);color:#2a2a2a}
  .app{padding:14px;display:grid;grid-template-columns:360px 1fr 420px;grid-template-rows:68px 1fr;gap:12px;height:100vh;box-sizing:border-box}
  header{grid-column:1/-1;display:flex;align-items:center;gap:12px;padding:12px;border-radius:10px;background:linear-gradient(90deg, rgba(201,154,46,0.04), rgba(201,154,46,0.02));border:1px solid rgba(201,154,46,0.06)}
  .panel{background:var(--panel);border:1px solid rgba(0,0,0,0.04);padding:12px;border-radius:10px;box-shadow:0 6px 30px rgba(0,0,0,0.03)}
  .left{overflow:auto}
  .stat{display:flex;align-items:center;justify-content:space-between;padding:10px;border-radius:8px;background:linear-gradient(180deg, rgba(201,154,46,0.02), rgba(201,154,46,0.01));border:1px solid rgba(201,154,46,0.03)}
  .streams{font-family:monospace;background:linear-gradient(180deg,#fff,#fbfaf8);padding:8px;border-radius:8px;border:1px solid rgba(201,154,46,0.03);height:140px;overflow:auto}
  .log{font-family:monospace;padding:8px;border-radius:8px;height:200px;overflow:auto;background:linear-gradient(180deg,#fff,#fbfaf8);border:1px solid rgba(0,0,0,0.02)}
  .center{display:grid;grid-template-rows:1fr 240px;gap:12px}
  .big-grid{display:grid;grid-template-columns:1fr 420px;gap:12px}
  canvas{border-radius:8px;background:linear-gradient(180deg, rgba(245,242,238,0.6), rgba(250,248,246,0.8));}
  .right{display:flex;flex-direction:column;gap:12px;overflow:auto}
  .rules{display:flex;flex-direction:column;gap:8px}
  .rule{display:flex;justify-content:space-between;align-items:center;padding:8px;border-radius:8px;background:linear-gradient(180deg,#fff,#fbfaf8);border:1px solid rgba(201,154,46,0.03);font-family:monospace}
  .matrix{width:100%;height:160px;border-radius:6px;overflow:hidden}
  .footer{grid-column:1/-1;display:flex;justify-content:space-between;align-items:center;color:#7a6a3e;font-size:12px}
  @media (max-width:1100px){.app{grid-template-columns:1fr;grid-template-rows:68px auto auto;}}
</style>
</head>
<body>
<div class="app">
  <header>
    <div style="display:flex;align-items:center;gap:12px">
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="1" y="1" width="22" height="22" rx="4" stroke="#c99a2e" stroke-opacity="0.24" stroke-width="1.5"/><path d="M7 12h10M12 7v10" stroke="#c99a2e" stroke-width="1.6" stroke-linecap="round"/></svg>
    </div>
    <div class="brand"><h1>NETWORK FILTER ASSEMBLER</h1><p>Active Forge</p></div>
    <div style="margin-left:auto;display:flex;gap:12px;align-items:center">
      <div class="stat"><div style="font-size:11px;color:#7a6233">Collected</div><div style="font-weight:700;font-size:16px" id="collected">0</div></div>
      <div class="stat"><div style="font-size:11px;color:#7a6233">Rules</div><div style="font-weight:700;font-size:16px" id="ruleCount">0</div></div>
    </div>
  </header>

  <aside class="left panel">
    <div style="display:flex;flex-direction:column;gap:10px">
      <div class="panel"><strong>Incoming Detections</strong><div class="streams" id="incoming">(waiting...)</div></div>
      <div class="panel"><strong>Detection Log</strong><div class="log" id="dlog">--</div></div>
    </div>
  </aside>

  <main class="center">
    <div class="big-grid">
      <div class="panel" style="min-width:420px;">
        <div style="display:flex;justify-content:space-between;align-items:center"><strong>Kill & Collection Timeline</strong></div>
        <canvas id="lineChart" width="820" height="320"></canvas>
      </div>
      <div class="panel">
        <strong>Rule Forge</strong>
        <div class="rules" id="rulesArea" style="margin-top:8px;max-height:360px;overflow:auto"></div>
        <div style="display:flex;gap:8px;margin-top:8px"><button id="exportRules" style="padding:8px;border-radius:8px;cursor:pointer">EXPORT JSON</button></div>
      </div>
    </div>
    <div style="display:flex;gap:12px;align-items:stretch">
      <div class="panel" style="flex:1"><strong>Network Matrix (heat)</strong><canvas id="matrix" class="matrix" width="820" height="160"></canvas></div>
    </div>
  </main>

  <aside class="right panel">
    <strong>Filter Visualizer</strong>
    <div style="height:180px;margin-top:8px"><canvas id="filterCanvas" width="380" height="160"></canvas></div>
  </aside>
  <div class="footer"><div id="time">--</div></div>
</div>

<script>
const rand = (a=0,b=1)=>Math.random()*(b-a)+a; const rint=(a,b)=>Math.floor(rand(a,b+1));
const incoming = document.getElementById('incoming');
const dlog = document.getElementById('dlog');
const rulesArea = document.getElementById('rulesArea');
let rules = [];

function makeDetection(){
    // In a real app, this comes from a WebSocket or API polling
    const t = {id:Math.random().toString(36).slice(2,7), type: 'Exploit', time: new Date().toLocaleTimeString()};
    incoming.innerText = `${t.time} • DETECT ${t.type} ${t.id}\n` + incoming.innerText;
    
    if(Math.random() < 0.5) fetchRule();
}

function fetchRule(){
    fetch('/api/rule/compile', {method:'POST'}).then(r=>r.json()).then(r=>{
        rules.push(r);
        renderRules();
    });
}

function renderRules(){
    rulesArea.innerHTML = '';
    rules.slice().reverse().forEach(r=>{
        const el = document.createElement('div'); el.className='rule';
        el.innerHTML = `<div><strong>${r.rule_id}</strong><br><span style="font-size:11px">${r.match.signature}</span></div><div>${r.action}</div>`;
        rulesArea.appendChild(el);
    });
    document.getElementById('ruleCount').textContent = rules.length;
}

// Visuals (simplified for template)
const matrix = document.getElementById('matrix'); const mctx = matrix.getContext('2d');
function drawMatrix(){
    const w=matrix.width, h=matrix.height; const cols=40, rows=8; const cellW=w/cols, cellH=h/rows;
    for(let r=0;r<rows;r++){ for(let c=0;c<cols;c++){ const v=Math.random(); mctx.fillStyle=`rgba(201,154,46,${0.02+v*0.28})`; mctx.fillRect(c*cellW, r*cellH, cellW-1, cellH-1); }}
}
setInterval(()=>{ if(Math.random()<0.85) makeDetection(); drawMatrix(); }, 900);
</script>
</body>
</html>
'''

# -------------------------------------------------------------------------
# BUILDER LOGIC
# -------------------------------------------------------------------------

def create_repo():
    base_name = "Gold-Guard-Network-Defense"
    
    # Structure definition: path -> content
    structure = {
        f"{base_name}/README.md": readme_content,
        f"{base_name}/requirements.txt": requirements_content,
        f"{base_name}/app.py": app_py_content,
        f"{base_name}/src/__init__.py": init_py_content,
        f"{base_name}/src/threat_engine.py": threat_engine_content,
        f"{base_name}/src/rule_forge.py": rule_forge_content,
        f"{base_name}/templates/index.html": html_index_content,
        f"{base_name}/templates/forge.html": html_forge_content,
    }

    # Write files
    for path, content in structure.items():
        # Ensure dir exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        # Write file
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    # Zip it up
    zip_filename = f"{base_name}.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_name):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(base_name))
                zipf.write(file_path, arcname)
                
    print(f"✅ Repository built successfully!")
    print(f"📦 Created: {zip_filename}")
    print(f"📂 Folder:  {base_name}/")

if __name__ == "__main__":
    create_repo()