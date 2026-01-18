import json
import datetime
from dataclasses import dataclass
from typing import List

@dataclass
class LogEntry:
    id: str
    timestamp: datetime.datetime
    actor: str
    action: str
    resource: str
    status: str

class AuditAnalyzer:
    def __init__(self):
        self.logs: List[LogEntry] = []

    def load_logs(self, log_data: List[dict]):
        for entry in log_data:
            dt = datetime.datetime.fromisoformat(entry['timestamp'])
            self.logs.append(LogEntry(
                id=entry['id'],
                timestamp=dt,
                actor=entry['actor'],
                action=entry['action'],
                resource=entry['resource'],
                status=entry['status']
            ))
        
        # Sort by time
        self.logs.sort(key=lambda x: x.timestamp)
        print(f"📂 Loaded {len(self.logs)} log entries.")

    def run_forensics(self):
        print("\n🕵️ Running Forensic Analysis...")
        self._detect_brute_force()
        self._detect_bulk_delete()
        print("✅ Scan Complete.")

    def _detect_brute_force(self):
        # Rule: > 3 failed logins in 1 minute by same actor
        failures = {} # actor -> list of timestamps
        
        for log in self.logs:
            if log.action == "LOGIN" and log.status == "FAILURE":
                if log.actor not in failures: failures[log.actor] = []
                failures[log.actor].append(log.timestamp)
        
        for actor, timestamps in failures.items():
            if len(timestamps) < 3: continue
            
            # Check windows
            for i in range(len(timestamps) - 2):
                start = timestamps[i]
                end = timestamps[i+2] # 3rd failure
                delta = (end - start).total_seconds()
                
                if delta < 60:
                    print(f"🚨 ALERT: Potential Brute Force by '{actor}' ({len(timestamps)} failures)")
                    return

    def _detect_bulk_delete(self):
        # Rule: > 2 deletes in 1 minute
        deletes = {} # actor -> list of timestamps
        
        for log in self.logs:
            if log.action == "DELETE" and log.status == "SUCCESS":
                if log.actor not in deletes: deletes[log.actor] = []
                deletes[log.actor].append(log.timestamp)
                
        for actor, timestamps in deletes.items():
            if len(timestamps) < 2: continue
            
            for i in range(len(timestamps) - 1):
                 start = timestamps[i]
                 end = timestamps[i+1]
                 delta = (end - start).total_seconds()
                 if delta < 60:
                     print(f"⚠️  WARNING: Rapid Deletion by '{actor}'")
                     return

if __name__ == "__main__":
    # 1. Simulate Logs (JSON structure)
    raw_logs = [
        {"id": "1", "timestamp": "2026-01-18T10:00:00", "actor": "alice", "action": "LOGIN", "resource": "portal", "status": "SUCCESS"},
        # Hacker trying to login
        {"id": "2", "timestamp": "2026-01-18T10:05:01", "actor": "hacker", "action": "LOGIN", "resource": "portal", "status": "FAILURE"},
        {"id": "3", "timestamp": "2026-01-18T10:05:05", "actor": "hacker", "action": "LOGIN", "resource": "portal", "status": "FAILURE"},
        {"id": "4", "timestamp": "2026-01-18T10:05:10", "actor": "hacker", "action": "LOGIN", "resource": "portal", "status": "FAILURE"},
        # Rogue employee deleting files
        {"id": "5", "timestamp": "2026-01-18T11:00:00", "actor": "bob", "action": "DELETE", "resource": "DB_PROD", "status": "SUCCESS"},
        {"id": "6", "timestamp": "2026-01-18T11:00:05", "actor": "bob", "action": "DELETE", "resource": "BACKUPS", "status": "SUCCESS"},
    ]
    
    analyzer = AuditAnalyzer()
    analyzer.load_logs(raw_logs)
    analyzer.run_forensics()
