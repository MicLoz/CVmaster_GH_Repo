from docx import Document

# Function to parse .docx file and extract text
def extract_docx_text(file_path, Fsg):
    try:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    except Exception as e:
        Fsg.popup(f"Error reading file: {e}")
        return ""
