import xml.etree.ElementTree as ET

def extract_text(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Namespaces
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    
    text = []
    for p in root.findall('.//w:p', ns):
        p_text = ""
        for t in p.findall('.//w:t', ns):
            if t.text:
                p_text += t.text
        if p_text:
            text.append(p_text)
    
    return "\n\n".join(text)

xml_path = 'temp_test/word/document.xml'
extracted_text = extract_text(xml_path)

with open('extracted_test.txt', 'w', encoding='utf-8') as f:
    f.write(extracted_text)
