import json
import re
from collections import defaultdict


with open("income_tax_bill_chunks.json", "r", encoding="utf-8") as f:
    clauses = json.load(f)


grouped = defaultdict(lambda: defaultdict(list))


subsection_regex = re.compile(r"([A-Z])\.—\s*([\w\s,]*)", re.UNICODE)

for clause in clauses:
    chapter = clause["chapter_title"]
    
    match = subsection_regex.search(clause["text"])
    if match:
        subsection = f"{match.group(1)}.— {match.group(2).strip()}"
    else:
        subsection = "General"

    grouped[chapter][subsection].append(clause)

grouped = {k: dict(v) for k, v in grouped.items()}

with open("grouped_clauses.json", "w", encoding="utf-8") as f:
    json.dump(grouped, f, indent=2, ensure_ascii=False)

print("✅ Grouped clauses saved to 'grouped_clauses.json'")
