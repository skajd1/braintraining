import os
import glob
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredMarkdownLoader

# --- 설정 ---
MARKDOWN_SOURCE_DIR = "processed_markdown"
CHROMA_DB_PATH = "chroma_db"
EMBEDDING_MODEL_PATH = "./ko-sroberta-multitask" # 로컬 모델 경로

def setup_vector_store():
    """processed_markdown 폴더의 모든 마크다운 파일을 로드, 분할하여 Chroma DB를 생성합니다."""
    markdown_files = glob.glob(os.path.join(MARKDOWN_SOURCE_DIR, '*.md'))
    if not markdown_files:
        print(f"오류: '{MARKDOWN_SOURCE_DIR}'에서 마크다운 파일을 찾을 수 없습니다.")
        return

    all_docs = []
    print(f"총 {len(markdown_files)}개의 마크다운 파일을 로드합니다...")
    for md_file in markdown_files:
        try:
            loader = UnstructuredMarkdownLoader(md_file)
            documents = loader.load()
            # 메타데이터에 파일 출처(source) 추가
            for doc in documents:
                doc.metadata["source"] = os.path.basename(md_file)
            all_docs.extend(documents)
            print(f" - 로드 완료: {md_file}")
        except Exception as e:
            print(f" - 로드 실패: {md_file} ({e})")

    if not all_docs:
        print("오류: 처리할 문서가 없습니다.")
        return

    print("\n문서를 텍스트 덩어리로 분할합니다...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(all_docs)

    if not docs:
        print("오류: 문서를 분할하지 못했습니다.")
        return

    print(f"텍스트 덩어리를 임베딩하고 Chroma DB에 저장합니다. (모델: {EMBEDDING_MODEL_PATH})")
    print("이 작업은 시간이 다소 걸릴 수 있습니다...")

    try:
        embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_PATH)
        
        # 기존 DB가 있다면 삭제 후 새로 생성 (혹은 업데이트 로직 추가도 가능)
        if os.path.exists(CHROMA_DB_PATH):
            print(f"기존 Chroma DB('{CHROMA_DB_PATH}')를 삭제합니다.")
            import shutil
            shutil.rmtree(CHROMA_DB_PATH)

        vectordb = Chroma.from_documents(
            documents=docs, 
            embedding=embeddings, 
            persist_directory=CHROMA_DB_PATH
        )
        vectordb.persist()
        print(f"\n성공적으로 Chroma DB를 '{CHROMA_DB_PATH}' 폴더에 저장했습니다.")
        print(f"총 {len(docs)}개의 텍스트 조각이 저장되었습니다.")

    except Exception as e:
        print(f"\nChroma DB 생성 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    setup_vector_store()