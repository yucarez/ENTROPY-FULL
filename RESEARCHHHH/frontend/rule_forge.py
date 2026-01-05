import uuid

class RuleForge:
    def __init__(self):
        self.rules_db = []

    def compile_rule(self, threat_data):
        """
        Takes a neutralized threat and compiles a firewall rule 
        to prevent future occurrences.
        """
        # Generate a unique signature from the payload fragment
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

    def export_rules_json(self):
        """Returns the current policy fabric as JSON."""
        return self.rules_db