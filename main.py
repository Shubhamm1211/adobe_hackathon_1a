import fitz  # PyMuPDF
import json
import os
import re

# INPUT_DIR = "input"
# OUTPUT_DIR = "output"

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"
def identify_headings(pdf_path):
    doc = fitz.open(pdf_path)
    outline = []
    
    title = ""
    if doc.page_count > 0:
        page1 = doc[0]
        blocks = page1.get_text("dict", sort=True)["blocks"]
        max_font_size = 0
        if blocks:
            for b in blocks:
                if b['bbox'][1] < page1.rect.height * 0.3 and "lines" in b:
                    for l in b["lines"]:
                        for s in l["spans"]:
                            if s['size'] > max_font_size and len(s['text'].strip().split()) < 10:
                                max_font_size = s['size']
                                title = s['text'].strip()
    
    font_counts = {}
    for page in doc:
        for b in page.get_text("dict")["blocks"]:
            if "lines" in b:
                for l in b["lines"]:
                    for s in l["spans"]:
                        font_counts[round(s['size'])] = font_counts.get(round(s['size']), 0) + 1
    
    base_font_size = 0
    if font_counts:
        base_font_size = max(font_counts, key=font_counts.get)

    heading_fonts = {round(s['size']) for page in doc for b in page.get_text("dict")["blocks"] if "lines" in b for l in b["lines"] for s in l["spans"] if "bold" in s['font'].lower() and round(s['size']) > base_font_size}
    sorted_heading_fonts = sorted(list(heading_fonts), reverse=True)
    font_to_level = {size: f"H{i+1}" for i, size in enumerate(sorted_heading_fonts[:3])}

    for page_num, page in enumerate(doc):
        for b in page.get_text("dict", sort=True)["blocks"]:
            if "lines" in b:
                for l in b["lines"]:
                    if len(l["spans"]) > 0:
                        span = l["spans"][0]
                        text = " ".join([s['text'] for s in l["spans"]]).strip()
                        font_size, is_bold = round(span['size']), "bold" in span['font'].lower()
                        
                        level = None
                        match = re.match(r"^(Appendix\s+[A-Z]|\d+(\.\d+)*)\s+", text)
                        if match:
                            num_dots = text.split()[0].count('.')
                            if "Appendix" in text: level = "H1"
                            elif num_dots == 0: level = "H1"
                            elif num_dots == 1: level = "H2"
                            else: level = "H3"
                        elif is_bold and font_size in font_to_level:
                            level = font_to_level[font_size]

                        if level and text and len(text.split()) < 20 and not text.endswith('.'):
                            clean_text = re.sub(r"^(Appendix\s+[A-Z]|\d+(\.\d+)*)\s*", "", text).strip()
                            if clean_text.lower() != title.lower() and len(clean_text) > 2:
                                outline.append({"level": level, "text": clean_text, "page": page_num + 1})

    unique_outline = [dict(t) for t in {tuple(d.items()) for d in outline}]
    unique_outline.sort(key=lambda x: x['page'])
    
    return {"title": title, "outline": unique_outline}

def main():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    
    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith('.pdf')]
    for pdf_file in pdf_files:
        pdf_path = os.path.join(INPUT_DIR, pdf_file)
        print(f"Processing {pdf_file}...")
        try:
            result = identify_headings(pdf_path)
            output_filename = os.path.splitext(pdf_file)[0] + ".json"
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=4, ensure_ascii=False)
            print(f"Successfully created {output_filename}")
        except Exception as e:
            print(f"Error processing {pdf_file}: {e}")

if __name__ == "__main__":
    main()