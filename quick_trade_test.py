#!/usr/bin/env python3
import subprocess

result = subprocess.run([
    ".venv\\Scripts\\python.exe",
    "run_draft_helper.py"
],
input="3\n7\n",  # Trade analysis, then quit
text=True,
capture_output=True,
timeout=30
)

print("=== OUTPUT SAMPLE ===")
# Look for the kept players section which should show matchup indicators
lines = result.stdout.split('\n')
found_kept = False
for i, line in enumerate(lines):
    if "[KEPT] PLAYERS REMAINING ON ROSTER:" in line:
        found_kept = True
        print("Found kept players section:")
        # Print next 10 lines to see the indicators
        for j in range(i, min(i+15, len(lines))):
            print(f"  {lines[j]}")
        break

if not found_kept:
    print("Kept players section not found, showing last 30 lines:")
    for line in lines[-30:]:
        print(line)

# Count indicators
caret_count = result.stdout.count("^")
o_count = result.stdout.count(" o ")  # Space around to avoid false matches
v_count = result.stdout.count(" v ")

print(f"\nIndicator counts:")
print(f"^ (great): {caret_count}")
print(f"o (good): {o_count}")
print(f"v (poor): {v_count}")

if caret_count + o_count + v_count > 0:
    print("SUCCESS: Matchup indicators now working!")
else:
    print("Still no indicators found")