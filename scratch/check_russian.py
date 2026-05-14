import zipfile
import re

def check_xml_for_russian(path):
    document = zipfile.ZipFile(path)
    xml_content = document.read('word/document.xml').decode('utf-8')
    document.close()
    
    # Look for Cyrillic characters that are NOT Kazakh specific (like ә, і, ң, ғ, ү, ұ, қ, ө, һ)
    # Actually, let's just look for common Russian words or headers.
    russian_sample = re.findall(r'[а-яА-ЯёЁ]{4,}', xml_content)
    # Filter out common Kazakh words if possible, but just seeing many Russian words is enough.
    return russian_sample[:50]

try:
    samples = check_xml_for_russian('учебник новый.docx')
    print("Found samples:", samples)
except Exception as e:
    print(f"Error: {e}")
