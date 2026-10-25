"""Rewrite the grade sentence in entry_requirements so it no longer
presupposes that international applicants can apply (which answered
part 1 by implication). Checked and approved by Vahid, 25 Oct 2026.

Run once:  python3 fix_entry_overlap.py
"""

import json
from pathlib import Path

PATH = Path(__file__).parent / "dataset.json"

OLD = (
    "Minimum grade requirements for international applicants vary by university, "
    "by the country where the degree was taken, and often by the ranking of the "
    "applicant's home institution. There is no single conversion to the UK grading scale."
)
NEW = (
    "Where a master's programme sets a minimum undergraduate grade, the figure varies "
    "by university, by the country where the degree was taken, and often by the ranking "
    "of the home institution. There is no single conversion to the UK grading scale."
)

data = json.loads(PATH.read_text())
changed = []
for case in data:
    if case["scenario"] != "entry_requirements":
        continue
    if OLD in case["knowledge"]:
        case["knowledge"] = case["knowledge"].replace(OLD, NEW)
        changed.append(case["id"])

if not changed:
    raise SystemExit("Old sentence not found - nothing changed. Send me the output.")

PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
print(f"changed {len(changed)} cases: {', '.join(changed)}")
