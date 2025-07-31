import fitz  # PyMuPDF
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP
import file_handler

def extract_text_from_pdf(pdf_path):
    """PDF 파일에서 텍스트를 추출하여 마크다운 파일로 저장합니다."""
    try:
        doc = fitz.open(pdf_path)
        content = ""
        for page in doc:
            content += page.get_text()
        
        md_path = file_handler.get_md_path(pdf_path)
        file_handler.write_markdown_file(md_path, content)
        return md_path
    except Exception as e:
        print(f"PDF 텍스트 추출 오류 ({pdf_path}): {e}")
        return None

def load_and_split_document(md_path):
    """마크다운 파일을 로드하고 청크로 분할하여 Document 객체 리스트를 반환합니다."""
    try:
        loader = UnstructuredMarkdownLoader(md_path)
        docs = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE, 
            chunk_overlap=CHUNK_OVERLAP
        )
        return text_splitter.split_documents(docs)
    except Exception as e:
        print(f"문서 로드 및 분할 오류 ({md_path}): {e}")
        return []
