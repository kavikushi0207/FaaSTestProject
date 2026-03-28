import requests
import time
import threading

url = "http://localhost:7071/api/match"
data = {
    "resume": "Experienced Python developer with expertise in Docker, Kubernetes, and Azure Functions. Skilled in NLP.",
    "jd": "Looking for a Cloud Engineer with Python, Docker, and FaaS experience."
}

def send_request():
    start = time.time()
    response = requests.post(url, json=data)
    end = time.time()
    print(f"Status: {response.status_code} | Score: {response.json().get('match_score')}% | Time: {round(end-start, 4)}s")

# Test 1: Single Request
print("--- Single Request Test ---")
send_request()

# Test 2: Concurrency (Simulating 5 people at once)
print("\n--- Concurrency Test (5 simultaneous) ---")
threads = []
for i in range(5):
    t = threading.Thread(target=send_request)
    threads.append(t)
    t.start()