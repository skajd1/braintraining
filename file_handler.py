import os
from config import SOURCE_DOCS_DIR, MARKDOWN_OUTPUT_DIR, IMAGE_OUTPUT_DIR

# --- 폴더 초기화 ---
for dir_path in [SOURCE_DOCS_DIR, MARKDOWN_OUTPUT_DIR, IMAGE_OUTPUT_DIR]:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def get_pdf_path(filename):
    """PDF 파일의 전체 경로를 반환합니다."""
    return os.path.join(SOURCE_DOCS_DIR, filename)

def get_md_path(pdf_filename):
    """PDF 파일명에 해당하는 마크다운 파일의 전체 경로를 반환합니다."""
    base_filename = os.path.splitext(pdf_filename)[0]
    return os.path.join(MARKDOWN_OUTPUT_DIR, f"{base_filename}.md")

def pdf_exists(filename):
    """주어진 이름의 PDF 파일이 존재하는지 확인합니다."""
    return os.path.exists(get_pdf_path(filename))

def save_uploaded_pdf(uploaded_file):
    """업로드된 파일을 PDF 소스 디렉토리에 저장합니다."""
    file_path = get_pdf_path(uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def write_markdown_file(md_path, content):
    """주어진 경로에 마크다운 컨텐츠를 작성합니다."""
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(content)
