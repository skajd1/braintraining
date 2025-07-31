import os
import hashlib
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from config import CHROMA_DB_PATH, EMBEDDING_MODEL_PATH, SEARCH_K_VALUE

class VectorStoreManager:
    def __init__(self):
        self.db_path = CHROMA_DB_PATH
        self.embedding_function = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_PATH)
        self.vectordb = Chroma(
            persist_directory=self.db_path, 
            embedding_function=self.embedding_function
        )

    def _generate_doc_ids(self, docs):
        """문서 내용 기반으로 고유 ID를 생성합니다."""
        return [hashlib.md5(doc.page_content.encode('utf-8')).hexdigest() for doc in docs]

    def add_documents(self, docs):
        """분할된 Document 객체들을 벡터 저장소에 추가합니다."""
        if not docs:
            return
        ids = self._generate_doc_ids(docs)
        self.vectordb.add_documents(documents=docs, ids=ids)
        self.vectordb.persist()

    def delete_documents(self, filename):
        """특정 파일명(source)을 가진 모든 문서를 벡터 저장소에서 삭제합니다."""
        results = self.vectordb.get(where={"source": filename})
        if results.get("ids"):
            self.vectordb.delete(ids=results["ids"])
            self.vectordb.persist()

    def get_retriever(self):
        """벡터 저장소로부터 Retriever를 생성하여 반환합니다."""
        if not os.path.exists(self.db_path) or not self.vectordb.get()["ids"]:
            return None
        return self.vectordb.as_retriever(search_kwargs={'k': SEARCH_K_VALUE})
