import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# --- API 및 모델 설정 ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
# 로컬에 저장될 임베딩 모델의 경로
EMBEDDING_MODEL_PATH = "./ko-sroberta-multitask"
# Hugging Face에서 다운로드할 원본 모델 이름
REMOTE_EMBEDDING_MODEL = "jhgan/ko-sroberta-multitask"
# 사용할 LLM 모델 이름
LLM_MODEL_NAME = "gemini-2.5-pro"

# --- 파일 시스템 경로 설정 ---
# 원본 파일이 저장될 디렉토리 (PDF, DOCX, XLSX 등)
SOURCE_DOCS_DIR = "source_documents"
# 추출된 이미지가 저장될 디렉토리 (현재 사용 안 함, 확장성 위해 유지)
IMAGE_OUTPUT_DIR = "images"
# ChromaDB 벡터 데이터베이스가 저장될 디렉토리
CHROMA_DB_PATH = "chroma_db"

# --- 텍스트 분할 설정 ---
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

# --- 검색 설정 ---
# Retriever가 검색할 문서의 수
SEARCH_K_VALUE = 5