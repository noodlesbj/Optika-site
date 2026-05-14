import zipfile
import xml.etree.ElementTree as ET
import re

def extract_bilingual_text(path):
    document = zipfile.ZipFile(path)
    xml_content = document.read('word/document.xml')
    document.close()
    tree = ET.fromstring(xml_content)
    
    # Namespaces
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    
    kazakh_text = []
    russian_text = []
    
    for p in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
        p_text = ""
        for t in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'):
            if t.text:
                p_text += t.text
        
        if not p_text.strip():
            continue
            
        # Heuristic: check for Kazakh-specific characters
        if re.search(r'[әіңғүұқөһӘІҢҒҮҰҚӨҺ]', p_text):
            kazakh_text.append(p_text)
        else:
            # If it's Cyrillic but doesn't have Kazakh chars, it might be Russian or just a shared word.
            if re.search(r'[а-яА-ЯёЁ]', p_text):
                russian_text.append(p_text)
                
    return kazakh_text, russian_text

try:
    kz, ru = extract_bilingual_text('учебник новый.docx')
    with open('extracted_kz.txt', 'w', encoding='utf-8') as f:
        f.write("\n".join(kz))
    with open('extracted_ru.txt', 'w', encoding='utf-8') as f:
        f.write("\n".join(ru))
    print(f"Success: {len(kz)} Kazakh paragraphs, {len(ru)} Russian paragraphs found.")
except Exception as e:
    print(f"Error: {e}")
