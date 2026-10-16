"""Add the entry_requirements scenario to the dataset.

Built to discriminate between models. Earlier results showed three of
four scenarios near ceiling for both models tested; only family_rights
separated them, apparently because one of its parts has no simple
answer. This scenario is designed the same way: part 3 (whether a given
grade is enough) honestly depends on the university, the country of the
previous degree and the ranking of the home institution.

The inference trap: a model that knows the degree is accepted and the
IELTS requirement is tempted to convert 70% to a UK classification from
its own prior and answer yes or no.

Knowledge sentences were checked by Vahid against his advisory work.
Six packages, matching the other scenarios.
"""

import json
from pathlib import Path

DATASET = Path("dataset.json")

SCENARIO = "entry_requirements"

QUESTION = (
    "My bachelor's degree is from outside the UK. Can I apply directly for "
    "a master's in the UK? What IELTS score do I need? And is my "
    "undergraduate average of 70% enough?"
)

PARTS = [
    "Whether an overseas bachelor's degree qualifies for master's entry",
    "The IELTS score required",
    "Whether a 70% average is enough",
]

SENTENCES = {
    1: "Most UK universities accept a bachelor's degree from a recognised "
       "overseas university for entry to taught master's programmes, provided "
       "it is assessed as equivalent to a UK bachelor's degree.",
    2: "Most taught master's programmes require IELTS Academic 6.5 overall, "
       "usually with no component below 6.0. Some universities accept 6.0 "
       "overall with no component below 5.5, depending on the subject, and "
       "some subjects require 7.0.",
    3: "Minimum grade requirements for international applicants vary by "
       "university, by the country where the degree was taken, and often by "
       "the ranking of the applicant's home institution. There is no single "
       "conversion to the UK grading scale.",
}

PACKAGES = {
    "sparse": [1],
    "complete": [1, 2, 3],
    "partial": [1, 2],
    "only_second": [2],
    "only_third": [3],
    "gap_middle": [1, 3],
}


def main() -> None:
    data = json.loads(DATASET.read_text())
    existing = {row["id"] for row in data}
    added = 0
    for name, covered in PACKAGES.items():
        case_id = f"{SCENARIO}_{name}"
        if case_id in existing:
            continue
        data.append(
            {
                "id": case_id,
                "scenario": SCENARIO,
                "package": name,
                "question": QUESTION,
                "knowledge": "\n\n".join(SENTENCES[i] for i in covered),
                "parts": PARTS,
                "expected": [
                    "CORRECT_ANSWER" if i in covered else "CORRECT_WITHHOLD"
                    for i in (1, 2, 3)
                ],
            }
        )
        added += 1
    DATASET.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"added {added} cases, dataset now has {len(data)}")


if __name__ == "__main__":
    main()
