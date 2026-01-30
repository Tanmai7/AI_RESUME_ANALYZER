import os
from docx import Document
import pdfplumber
from PIL import Image
import pytesseract

# -------------------------------
# Supported file formats
# -------------------------------
ALLOWED_EXTENSIONS = [".pdf", ".docx", ".jpg", ".jpeg", ".png"]

# Resume-related keywords (basic intelligence  check)
RESUME_KEYWORDS = [
    "education", "skills", "experience",
    "projects", "certifications", "internship",
    "summary", "objective"
]

# -------------------------------
# Function to check valid file
# -------------------------------
def is_valid_file(filename):
    return any(filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS)

# -------------------------------
# Extract text from DOCX
# -------------------------------
def extract_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join(para.text for para in doc.paragraphs)

# -------------------------------
# Extract text from PDF
# -------------------------------
def extract_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

# -------------------------------
# Extract text from Image (OCR)
# -------------------------------
def extract_from_image(file_path):
    image = Image.open(file_path)
    return pytesseract.image_to_string(image)

# -------------------------------
# Check if text looks like a resume
# -------------------------------
def is_resume(text):
    text = text.lower()
    matches = sum(1 for word in RESUME_KEYWORDS if word in text)
    return matches >= 2   # simple but effective rule

# -------------------------------
# Main function
# -------------------------------
def process_resume(file_path):

    if not os.path.exists(file_path):
        print("❌ File not found.")
        return

    if not is_valid_file(file_path):
        print("❌ Invalid file format. Upload PDF, DOCX, or Image only.")
        return

    print("📄 File accepted. Extracting text...")

    if file_path.endswith(".docx"):
        text = extract_from_docx(file_path)

    elif file_path.endswith(".pdf"):
        text = extract_from_pdf(file_path)

    else:
        text = extract_from_image(file_path)

    if not text.strip():
        print("❌ No readable text found. Invalid input.")
        return

    if not is_resume(text):
        print("❌ This does NOT look like a resume. Invalid input.")
        return

    # Save extracted resume text
    with open("resume_text.txt", "w", encoding="utf-8") as f:
        f.write(text)

    print("✅ Resume accepted and text extracted successfully!")
    print("📁 Output saved as resume_text.txt")

# -------------------------------
# Run the program
# -------------------------------
if __name__ == "__main__":
    file_path = input("📤 Enter resume file path: ")
    process_resume(file_path)
