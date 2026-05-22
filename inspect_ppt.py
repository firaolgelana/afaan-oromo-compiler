import zipfile
import os

pptx_path = r"C:\Users\sebon\OneDrive\Desktop\Afaan_Oromoo_Compiler_Presentation.pptx"
temp_dir = "temp_pptx_inspect"

# Unzip the pptx
with zipfile.ZipFile(pptx_path, 'r') as zip_ref:
    zip_ref.extractall(temp_dir)

# Read presentation.xml
pres_xml_path = os.path.join(temp_dir, "ppt", "presentation.xml")
with open(pres_xml_path, 'r', encoding='utf-8') as f:
    xml_content = f.read()

print("PRESENTATION.XML:")
print(xml_content)
