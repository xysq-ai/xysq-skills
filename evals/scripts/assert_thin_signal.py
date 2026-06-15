import sys
SIGNALS = ["i don't have", "i don't have much", "nothing logged", "no record",
           "couldn't find", "not much on", "don't have anything logged"]
text = open(sys.argv[1]).read().lower()
ok = any(s in text for s in SIGNALS)
print("PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
