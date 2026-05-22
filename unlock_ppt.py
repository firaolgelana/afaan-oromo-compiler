import zipfile
import os
import shutil

pptx_path = r"C:\Users\sebon\OneDrive\Desktop\Afaan_Oromoo_Compiler_Presentation.pptx"
temp_dir = "temp_pptx"

# Unzip the pptx
with zipfile.ZipFile(pptx_path, 'r') as zip_ref:
    zip_ref.extractall(temp_dir)

# Read presentation.xml
pres_xml_path = os.path.join(temp_dir, "ppt", "presentation.xml")
with open(pres_xml_path, 'r', encoding='utf-8') as f:
    xml_content = f.read()

# Look for modifyVerifier and remove it
import re
# The tag looks like <p:modifyVerifier ... />
new_xml_content = re.sub(r'<p:modifyVerifier[^>]*/>', '', xml_content)

if new_xml_content != xml_content:
    print("Found and removed modifyVerifier (password protection).")
    with open(pres_xml_path, 'w', encoding='utf-8') as f:
        f.write(new_xml_content)
else:
    print("No modifyVerifier found.")

# Re-zip the pptx
new_pptx_path = r"C:\Users\sebon\OneDrive\Desktop\Afaan_Oromoo_Compiler_Presentation_Unlocked.pptx"

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, path)
            ziph.write(file_path, arcname)

with zipfile.ZipFile(new_pptx_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipdir(temp_dir, zipf)

print(f"Saved unlocked presentation to {new_pptx_path}")

# Cleanup
shutil.rmtree(temp_dir)
