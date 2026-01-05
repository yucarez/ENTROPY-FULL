import random
import uuid
import time

class ThreatEngine:
    THREAT_TYPES = ['Virus', 'Phishing Link', 'Trojan', 'Ransomware', 'Malware', 'Spyware', 'Exploit']
    CODENAMES = ['PAYLOAD', 'INJECT', 'CLICK_FRAUD', 'DROPBEAR', 'NIGHTCRAWL', 'SILENT_NOMAD', 'GOLDEN_EGG']

    @staticmethod
    def generate_ip():
        """Generates a random internal or external IP address."""
        return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

    @staticmethod
    def generate_payload(length=32):
        """Generates a random hex payload simulating a signature."""
        return ' '.join([f"{random.randint(0, 255):02x}" for _ in range(length)])

    def spawn_threat(self):
        """Creates a threat object with scored heuristics."""
        threat_id = str(uuid.uuid4())[:8].upper()
        t_type = random.choice(self.THREAT_TYPES)
        name = random.choice(self.CODENAMES)
        
        # Calculate heuristic score (simulated)
        base_score = random.randint(10, 98)
        
        return {
            "id": threat_id,
            "name": name,
            "type": t_type,
            "score": base_score,
            "src": self.generate_ip(),
            "dst": "192.168.1.100",  # Protected Internal Node
            "payload": self.generate_payload(),
            "timestamp": time.time(),
            "status": "active"
        }

    def analyze_entropy(self, payload):
        """Mock analysis of payload entropy."""
        unique_chars = len(set(payload))
        return (unique_chars / len(payload)) * 100