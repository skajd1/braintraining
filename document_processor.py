from langchain_community.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP

def load_and_split_document(file_path):
    """주어진 경로의 파일을 로드하고 청크로 분할하여 Document 객체 리스트를 반환합니다."""
    try:
        # 파일 확장자에 따라 적절한 로더를 사용하는 UnstructuredFileLoader 사용
        loader = UnstructuredFileLoader(file_path)
        docs = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE, 
            chunk_overlap=CHUNK_OVERLAP
        )
        return text_splitter.split_documents(docs)
    except Exception as e:
        print(f"문서 로드 및 분할 오류 ({file_path}): {e}")
        return []