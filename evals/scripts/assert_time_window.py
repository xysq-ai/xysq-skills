import json, sys
from datetime import datetime, timedelta

def in_window(occurred_at, now, days):
    dt = datetime.fromisoformat(occurred_at.replace("Z", "+00:00"))
    return dt >= now - timedelta(days=days)

def check(output_text, fixture_path, window_days):
    data = json.load(open(fixture_path))
    now = datetime.fromisoformat(data["now"].replace("Z", "+00:00"))
    leaks = []
    for m in data["memories"]:
        out_of_window = not in_window(m["occurred_at"], now, window_days)
        phrase = " ".join(m["content"].split()[:6])
        if out_of_window and phrase.lower() in output_text.lower():
            leaks.append(m["content"])
    return leaks

if __name__ == "__main__":
    output = open(sys.argv[1]).read()
    leaks = check(output, sys.argv[2], int(sys.argv[3]))
    if leaks:
        print("FAIL: out-of-window leaks:", leaks); sys.exit(1)
    print("PASS: no out-of-window leaks")
