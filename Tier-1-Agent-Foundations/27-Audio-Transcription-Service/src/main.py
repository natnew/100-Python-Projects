import time
import random
from typing import Dict, Optional, Callable
from collections import deque
from threading import Thread
from dataclasses import dataclass

@dataclass
class AudioJob:
    id: str
    filename: str
    status: str = "pending"
    result: Optional[str] = None

class TranscriptionService:
    def __init__(self):
        self.queue = deque()
        self.running = False
        self.jobs: Dict[str, AudioJob] = {}

    def submit_audio(self, job_id: str, filename: str):
        job = AudioJob(job_id, filename)
        self.jobs[job_id] = job
        self.queue.append(job)
        print(f"🎤 Received audio: {filename} (Job {job_id})")

    def start_worker(self):
        self.running = True
        t = Thread(target=self._worker_loop)
        t.daemon = True
        t.start()
        print("⚙️ Transcription Worker Started.")

    def _worker_loop(self):
        while self.running:
            if self.queue:
                job = self.queue.popleft()
                self._process_job(job)
            time.sleep(0.1)

    def _process_job(self, job: AudioJob):
        print(f"Processing Job {job.id}...")
        job.status = "processing"
        
        # Simulate Whisper API Latency (1-2s)
        time.sleep(random.uniform(0.5, 1.5))
        
        # Simulated Output
        transcript = f"[Simulated Text from {job.filename}]"
        
        job.result = transcript
        job.status = "completed"
        print(f"✅ Job {job.id} Complete: '{transcript}'")

    def get_result(self, job_id: str) -> Optional[str]:
        job = self.jobs.get(job_id)
        if job and job.status == "completed":
            return job.result
        return None

# --- Example Usage ---

if __name__ == "__main__":
    service = TranscriptionService()
    service.start_worker()
    
    # 1. User speaks
    service.submit_audio("jb_1", "user_query_1.wav")
    service.submit_audio("jb_2", "user_query_2.wav")
    
    # 2. Poll for results (Simulating Agent Loop)
    print("\n--- Agent waiting for text ---")
    completed_count = 0
    while completed_count < 2:
        for jid in ["jb_1", "jb_2"]:
            res = service.get_result(jid)
            if res:
                print(f"Agent received: {res}")
                # Mark as handled in real logic
                # For demo, we just rely on job status
                
        # Count completion locally to exit loop
        completed_count = sum(1 for j in service.jobs.values() if j.status == "completed")
        time.sleep(0.5)
        
    print("Done.")
