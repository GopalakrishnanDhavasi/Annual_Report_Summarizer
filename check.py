"""
check_wkhtmltopdf.py
--------------------
A simple standalone script to verify that wkhtmltopdf works properly with pdfkit.

✅ It checks:
   - If wkhtmltopdf.exe exists at the given path
   - If pdfkit can generate a PDF using it

🧠 How to use:
   1️⃣ Update the path below if your wkhtmltopdf.exe is installed elsewhere.
   2️⃣ Run this script:
       python check_wkhtmltopdf.py
   3️⃣ If everything works, it will create 'test_output.pdf' in your folder.
"""

import os
import pdfkit

# 🔧 STEP 1: Provide your wkhtmltopdf.exe path here
WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"

# 🔍 STEP 2: Check if the file exists
if not os.path.exists(WKHTMLTOPDF_PATH):
    print("❌ wkhtmltopdf.exe not found!")
    print("👉 Please check if it's installed at:")
    print(WKHTMLTOPDF_PATH)
    print("\nIf not, install it from https://wkhtmltopdf.org/downloads.html")
    exit(1)

# ✅ STEP 3: Configure pdfkit
config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)
print(f"✅ wkhtmltopdf found at: {config.wkhtmltopdf}")

# 🧾 STEP 4: Create simple HTML content to convert
html_content = """
<html>
  <head>
    <meta charset="UTF-8">
    <style>
      body { font-family: 'DejaVu Sans', sans-serif; padding: 30px; }
      h1 { color: #2C3E50; text-align: center; }
      p { color: #34495E; font-size: 14px; }
    </style>
  </head>
  <body>
    <h1>✅ wkhtmltopdf Test Successful!</h1>
    <p>If you can see this text inside a generated PDF, your setup is working perfectly.</p>
    <p>Test supports Unicode: नमस्ते · مرحبا · 你好 · Hello</p>
  </body>
</html>
"""

# 📄 STEP 5: Try generating a test PDF
try:
    output_file = "test_output.pdf"
    pdfkit.from_string(html_content, output_file, configuration=config)
    print(f"🎉 PDF successfully created at: {os.path.abspath(output_file)}")
except Exception as e:
    print("❌ Failed to create PDF:")
    print(e)
