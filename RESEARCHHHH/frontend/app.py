from flask import Flask, render_template, jsonify
from src.threat_engine import ThreatEngine
from src.rule_forge import RuleForge

app = Flask(__name__)
engine = ThreatEngine()
forge = RuleForge()

@app.route('/')
def index():
    """Serves the Entropic Randomizer Dashboard"""
    return render_template('index.html')

@app.route('/forge')
def filter_assembler():
    """Serves the Filter Assembler Dashboard"""
    return render_template('forge.html')

# API Endpoint: Fetches a live threat from Python backend
@app.route('/api/threat/spawn')
def api_spawn():
    threat = engine.spawn_threat()
    return jsonify(threat)

# API Endpoint: Compiles a rule from a threat
@app.route('/api/rule/compile', methods=['POST'])
def api_compile():
    # In a real scenario, this would accept POST data
    # For demo, we simulate a threat being passed in
    dummy_threat = engine.spawn_threat()
    rule = forge.compile_rule(dummy_threat)
    return jsonify(rule)

if __name__ == '__main__':
    app.run(debug=True, port=5000)