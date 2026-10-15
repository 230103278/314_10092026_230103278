"""Hardware-bound HMAC-SHA256 submission token.

Usage: python generate_submission_token.py <STUDENT_ID> '<STUDENT_NAME>'
Writes submission_token.json, signing the student, the GPU and a SHA-256 of every lab_kernels/*.py.
Set LAB_HMAC_KEY to the instructor's secret if one was issued; otherwise the GPU UUID is the key.
"""
import glob
import hashlib
import hmac
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

if len(sys.argv) != 3:
    sys.exit(__doc__)
student_id, student_name = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))

gpu_name, gpu_uuid = subprocess.check_output(
    ["nvidia-smi", "--query-gpu=name,uuid", "--format=csv,noheader", "-i", "0"], text=True
).strip().split(", ")

files = {}
for path in sorted(glob.glob(os.path.join(here, "lab_kernels", "*.py"))):
    with open(path, "rb") as f:
        files[os.path.relpath(path, here)] = hashlib.sha256(f.read()).hexdigest()

payload = {
    "student_id": student_id,
    "student_name": student_name,
    "gpu_name": gpu_name,
    "gpu_uuid": gpu_uuid,
    "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "files": files,
}
key = os.environ.get("LAB_HMAC_KEY", gpu_uuid).encode()
message = json.dumps(payload, sort_keys=True).encode()
payload["signature"] = hmac.new(key, message, hashlib.sha256).hexdigest()

out = os.path.join(here, "submission_token.json")
with open(out, "w") as f:
    json.dump(payload, f, indent=2)
print(f"[+] Token written to {out}\n    signature: {payload['signature']}")
