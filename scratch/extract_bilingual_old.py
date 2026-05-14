import zipfile
import xml.etree.ElementTree as ET
import re

def extract_bilingual_text(path):
    document = zipfile.ZipFile(path)
    xml_content = document.read('word/document.xml')
    document.close()
    tree = ET.fromstring(xml_content)
    
    kazakh_text = []
    russian_text = []
    
    for p in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
        p_text = ""
        for t in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'):
            if t.text:
                p_text += t.text
        
        if not p_text.strip():
            continue
            
        if re.search(r'[әіңғүұқөһӘІҢҒҮҰҚӨҺ]', p_text):
            kazakh_text.append(p_text)
        else:
            if re.search(r'[а-яА-ЯёЁ]', p_text):
                russian_text.append(p_text)
                
    return kazakh_text, russian_text

try:
    kz, ru = extract_bilingual_text('учебник.docx')
    with open('extracted_kz_old.txt', 'w', encoding='utf-8') as f:
        f.write("\n".join(kz))
    with open('extracted_ru_old.txt', 'w', encoding='utf-8') as f:
        f.write("\n".join(ru))
    print(f"Success: {len(kz)} Kazakh paragraphs, {len(ru)} Russian paragraphs found.")
except Exception as e:
    print(f"Error: {e}")
