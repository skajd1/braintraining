import os
from sentence_transformers import SentenceTransformer
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.schema.output_parser import StrOutputParser
from config import (
    GEMINI_API_KEY, 
    EMBEDDING_MODEL_PATH, 
    REMOTE_EMBEDDING_MODEL, 
    LLM_MODEL_NAME
)

def download_embedding_model_if_needed():
    """로컬 임베딩 모델이 없으면 Hugging Face에서 다운로드합니다."""
    if not os.path.exists(EMBEDDING_MODEL_PATH):
        print(f"임베딩 모델 '{REMOTE_EMBEDDING_MODEL}'을 다운로드합니다...")
        SentenceTransformer(REMOTE_EMBEDDING_MODEL).save(EMBEDDING_MODEL_PATH)
        print("다운로드 완료.")

def get_llm():
    """Google Generative AI 모델을 로드하여 반환합니다."""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY가 설정되지 않았습니다.")
    return GoogleGenerativeAI(model=LLM_MODEL_NAME, temperature=0.7, google_api_key=GEMINI_API_KEY)

def create_rag_chain(retriever, llm):
    """RAG 체인을 생성합니다."""
    prompt_template = """
    당신은 제공된 컨텍스트 정보를 바탕으로 질문에 답변하는 AI 어시스턴트입니다.
    답변은 반드시 한국어로 작성해주세요.
    답변 후 출처를 명시해야 합니다.
    
    # 컨텍스트:
    {context}
    
    # 질문: {question}
    
    # 답변:
    """
    prompt = PromptTemplate.from_template(prompt_template)

    def format_docs(docs):
        return "\n\n".join(f"[출처: {doc.metadata.get('source', '알 수 없음')}]\n{doc.page_content}" for doc in docs)

    return (
        {"context": retriever | RunnableLambda(format_docs), "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

