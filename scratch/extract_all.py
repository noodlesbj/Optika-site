import zipfile
import xml.etree.ElementTree as ET

def extract_all_text(path):
    document = zipfile.ZipFile(path)
    xml_content = document.read('word/document.xml')
    document.close()
    tree = ET.fromstring(xml_content)
    
    paragraphs = []
    for p in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
        texts = [t.text for t in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if t.text]
        if texts:
            paragraphs.append("".join(texts))
    return paragraphs

try:
    paragraphs = extract_all_text('учебник новый.docx')
    with open('all_paragraphs.txt', 'w', encoding='utf-8') as f:
        for p in paragraphs:
            f.write(p + "\n")
    print(f"Success: {len(paragraphs)} paragraphs extracted.")
except Exception as e:
    print(f"Error: {e}")
