import sys

def check(skill, text):
    t = text.lower()
    if skill == "decisions":
        return any(line.strip().startswith(("-", "*", "1.", "1)")) for line in text.splitlines())
    if skill == "recap":
        return ("what happened" in t or "happened" in t) and ("next" in t)
    if skill == "blockers":
        return "waiting" in t or "blocked" in t
    if skill == "actionables":
        return any(line.strip().startswith(("-", "*")) for line in text.splitlines())
    if skill == "prep":
        return len(text.strip()) > 0
    return False

if __name__ == "__main__":
    ok = check(sys.argv[1], open(sys.argv[2]).read())
    print("PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
