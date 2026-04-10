
import os
import subprocess
import sys
import time
import requests
from requests.auth import HTTPBasicAuth


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
GENERATOR_SCRIPT = os.path.join(ROOT, "scripts", "player_rdf.py")
TTL_FILE = os.path.join(ROOT, "rdf", "football.ttl")

# Fuseki config từ docker-compose
# Dataset name: football
# Base URL: http://localhost:3030/football
FUSEKI_BASE = os.environ.get("FUSEKI_BASE", "http://localhost:3030")
DATASET_NAME = os.environ.get("FUSEKI_DATASET", "rdf_upload")
FUSEKI_URL = f"{FUSEKI_BASE}/{DATASET_NAME}"
UPLOAD_URL = f"{FUSEKI_URL}/upload"
QUERY_URL = f"{FUSEKI_URL}/query"

# Authentication (nếu cần)
FUSEKI_AUTH = "admin:vEQYqmFLsoa2uu8"
AUTH = None
if FUSEKI_AUTH:
    username, password = FUSEKI_AUTH.split(":", 1)
    AUTH = HTTPBasicAuth(username, password)


def run_generator():
    if not os.path.exists(GENERATOR_SCRIPT):
        raise FileNotFoundError(f"Generator script not found: {GENERATOR_SCRIPT}")

    print("🔧 Running RDF generator...")
    result = subprocess.run(
        [sys.executable, GENERATOR_SCRIPT],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise RuntimeError("RDF generator failed")

    print(result.stdout)
    print("✅ RDF generator finished")


def wait_for_fuseki(timeout_seconds=90):
    print(f"⏳ Waiting for Fuseki at {QUERY_URL} ...")
    deadline = time.time() + timeout_seconds
    while True:
        try:
            response = requests.get(QUERY_URL, timeout=5, auth=AUTH)
            if response.status_code == 200:
                print("✅ Fuseki is available")
                return
        except Exception:
            pass

        if time.time() > deadline:
            raise TimeoutError("Fuseki did not become available in time")

        print("⏱️  Waiting for Fuseki...")
        time.sleep(3)


def upload_rdf():
    if not os.path.exists(TTL_FILE):
        raise FileNotFoundError(f"RDF file not found: {TTL_FILE}")

    print(f"📤 Uploading RDF to Fuseki: {UPLOAD_URL}")
    
    with open(TTL_FILE, "rb") as f:
        files = {"files": (os.path.basename(TTL_FILE), f, "text/turtle")}
        response = requests.post(UPLOAD_URL, files=files, timeout=30, auth=AUTH)
        
        if response.status_code in [200, 204, 201]:
            print("✅ RDF upload successful!")
            print(response.text)
        else:
            print(f"❌ Upload failed: HTTP {response.status_code}")
            print(response.text)
            raise RuntimeError(f"Upload failed with status {response.status_code}")


def main():
    run_generator()
    wait_for_fuseki(timeout_seconds=90)
    upload_rdf()
    print("\n🎉 Done! RDF is uploaded to Jena Fuseki.")
    print(f"Query endpoint: {QUERY_URL}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Error: {exc}")
        sys.exit(1)
