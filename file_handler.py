import os
from config import SOURCE_DOCS_DIR, IMAGE_OUTPUT_DIR

# --- 폴더 초기화 ---
# 마크다운 폴더는 더 이상 필요 없으므로 초기화 목록에서 제외
for dir_path in [SOURCE_DOCS_DIR, IMAGE_OUTPUT_DIR]:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def get_source_document_path(filename):
    """소스 문서의 전체 경로를 반환합니다."""
    return os.path.join(SOURCE_DOCS_DIR, filename)

def source_document_exists(filename):
    """주어진 이름의 소스 문서가 존재하는지 확인합니다."""
    return os.path.exists(get_source_document_path(filename))

def save_uploaded_file(uploaded_file):
    """업로드된 파일을 소스 문서 디렉토리에 저장합니다."""
    file_path = get_source_document_path(uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path