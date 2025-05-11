
import fitz  # PyMuPDF
import re
import json

PDF_PATH = "income-tax-bill-2025.pdf"
OUTPUT_JSON = "income_tax_bill_chunks.json"

# LOAD PDF AND EXTRACT PAGE TEXTS 
doc = fitz.open(PDF_PATH)
pages = [{"page": i + 1, "text": page.get_text()} for i, page in enumerate(doc)]

# CONCATENATE TEXT AND PREP FOR CLAUSE EXTRACTION 
full_text = ""
page_offsets = []
for page in pages:
    page_offsets.append(len(full_text))
    full_text += f"\n[PAGE:{page['page']}]\n" + page["text"]

# REGEX FOR CLAUSES AND CHAPTER HEADINGS 
clause_regex = re.compile(r"\n(\d+)\.\s+(.*?)(?=\n\d+\.|\Z)", re.DOTALL)
chapter_regex = re.compile(r"CHAPTER\s+([A-Z]+)\s*\n(.*?)\n", re.IGNORECASE)

# EXTRACT CHAPTERS FOR REFERENCE 
chapter_matches = list(chapter_regex.finditer(full_text))
chapter_map = {}
for i, match in enumerate(chapter_matches):
    start = match.start()
    end = chapter_matches[i + 1].start() if i + 1 < len(chapter_matches) else len(full_text)
    chapter_map[start] = {
        "chapter_code": match.group(1).strip(),
        "chapter_title": match.group(2).strip(),
        "start": start,
        "end": end
    }

def find_chapter(pos):
    for chap_start in sorted(chapter_map.keys(), reverse=True):
        if pos >= chap_start:
            return chapter_map[chap_start]
    return {"chapter_code": "Unknown", "chapter_title": "Unknown"}

def find_page(pos):
    for i, offset in enumerate(page_offsets):
        if pos < offset:
            return i
    return len(page_offsets)

# EXTRACT CLAUSES AND ASSIGN METADATA 
clauses = []
for match in clause_regex.finditer(full_text):
    start_pos = match.start()
    clause_number = match.group(1).strip()
    clause_title = match.group(2).split('\n')[0].strip()
    clause_text = match.group(0).strip()

    chapter_info = find_chapter(start_pos)
    page_number = find_page(start_pos)

    clauses.append({
        "clause": clause_number,
        "title": clause_title,
        "text": clause_text,
        "chapter": f"Chapter {chapter_info['chapter_code']}",
        "chapter_title": chapter_info['chapter_title'],
        "page": page_number
    })

#  STEP 6: SAVE TO JSON FILE 
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(clauses, f, indent=2, ensure_ascii=False)

print(f"✅ Saved {len(clauses)} clauses to {OUTPUT_JSON}")


