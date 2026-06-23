import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def parse(path):
    t = open(path).read()
    fm = re.match(r"^---\n(.*?)\n---\n", t, re.S).group(1)
    name = re.search(r"^name:\s*(.+)$", fm, re.M).group(1).strip()
    # Handle both inline description and YAML block scalar (description: >)
    desc_m = re.search(r"^description:\s*(.+)$", fm, re.M)
    raw_desc = desc_m.group(1).strip()
    if raw_desc == ">":
        # Multi-line block scalar: collect indented continuation lines
        lines = fm.split("\n")
        desc_idx = next(i for i, l in enumerate(lines) if re.match(r"^description:\s*>", l))
        block_lines = []
        for l in lines[desc_idx + 1:]:
            if l.startswith("  ") or l == "":
                block_lines.append(l.strip())
            else:
                break
        raw_desc = " ".join(l for l in block_lines if l)
    desc = raw_desc.strip('"').strip("'")
    ver = re.search(r"<!--\s*version:\s*(\d+)\s*-->", t)
    return name, desc, int(ver.group(1)) if ver else 1

catalog = {}
for skill_dir in sorted(os.listdir(ROOT)):
    full = os.path.join(ROOT, skill_dir)
    if not os.path.isdir(full) or skill_dir.startswith(("_", ".")) or skill_dir in ("scripts", "evals"):
        continue
    platforms = sorted(
        p for p in os.listdir(full)
        if os.path.isfile(os.path.join(full, p, "SKILL.md"))
    )
    if not platforms:
        continue
    # Try each platform in order until one parses - report any that fail
    parsed = None
    for platform in platforms:
        skill_path = os.path.join(full, platform, "SKILL.md")
        try:
            parsed = parse(skill_path)
            break
        except (AttributeError, TypeError) as e:
            print(f"WARNING: {skill_dir}/{platform}/SKILL.md has no parseable frontmatter - skipping for catalog name/desc")
    if parsed is None:
        print(f"ERROR: {skill_dir} - no platform has parseable frontmatter; skipping skill")
        continue
    name, desc, ver = parsed
    catalog[skill_dir] = {"name": name, "description": desc,
                          "platforms": platforms, "version": ver}

with open(os.path.join(ROOT, "catalog.json"), "w") as f:
    json.dump(catalog, f, indent=2, sort_keys=True)
    f.write("\n")  # trailing newline so regenerating is a clean no-op (no dirty diff)
print(f"wrote catalog.json with {len(catalog)} skills")
