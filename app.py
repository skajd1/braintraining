import os
import streamlit as st
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# --- 다른 스크립트에서 기능 임포트 ---
from pdf_to_md import main as process_all_pdfs
from setup_chroma import setup_vector_store

# --- Langchain 관련 임포트 ---
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.schema.output_parser import StrOutputParser

# --- 1. 설정 (Configuration) ---
load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
CHROMA_DB_PATH = "chroma_db"
EMBEDDING_MODEL_PATH = "./ko-sroberta-multitask"  # 로컬 경로
REMOTE_EMBEDDING_MODEL = "jhgan/ko-sroberta-multitask" # Hugging Face 모델
LLM_MODEL_NAME = "gemini-2.5-pro"
SOURCE_DOCS_DIR = "source_documents"

# --- 2. 핵심 기능 함수 (Core Functions) ---

@st.cache_resource
def load_retriever():
    """
    Chroma DB에서 Retriever를 로드합니다.
    로컬 임베딩 모델이 없으면 자동으로 다운로드합니다.
    """
    # 1. 로컬 모델 존재 여부 확인 및 자동 다운로드
    if not os.path.exists(EMBEDDING_MODEL_PATH):
        with st.spinner(f"'{REMOTE_EMBEDDING_MODEL}' 모델을 다운로드 중입니다... (최초 1회)"): 
            try:
                model = SentenceTransformer(REMOTE_EMBEDDING_MODEL)
                model.save(EMBEDDING_MODEL_PATH)
            except Exception as e:
                st.error(f"모델 다운로드 중 오류 발생: {e}")
                st.stop()

    # 2. DB 및 Retriever 로드
    if not os.path.exists(CHROMA_DB_PATH):
        st.warning("지식 베이스(Chroma DB)가 없습니다. PDF를 업로드하고 지식 베이스를 먼저 생성해주세요.")
        return None
    try:
        embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_PATH)
        vector_store = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
        return vector_store.as_retriever(search_kwargs={'k': 5})
    except Exception as e:
        st.error(f"Retriever 로딩 중 오류 발생: {e}")
        return None

@st.cache_resource
def load_llm():
    """Google Generative AI 모델을 로드합니다."""
    if not GEMINI_API_KEY:
        st.error("GEMINI_API_KEY가 설정되지 않았습니다. .env 파일을 확인해주세요.")
        st.stop()
    try:
        return GoogleGenerativeAI(model=LLM_MODEL_NAME, temperature=0.7, google_api_key=GEMINI_API_KEY)
    except Exception as e:
        st.error(f"LLM 로딩 중 오류 발생: {e}")
        st.stop()

def create_rag_chain(_retriever, _llm):
    """RAG 체인을 생성합니다."""
    prompt_template = """
    당신은 제공된 컨텍스트 정보를 바탕으로 질문에 답변하는 AI 어시스턴트입니다.
    답변은 반드시 한국어로 작성해주세요.
    
    # 컨텍스트:
    {context}
    
    # 질문: {question}
    
    # 답변:
    """
    prompt = PromptTemplate.from_template(prompt_template)

    def format_docs(docs):
        return "\n\n".join(f"[출처: {doc.metadata.get('source', '알 수 없음')}]\n{doc.page_content}" for doc in docs)

    return (
        {"context": _retriever | RunnableLambda(format_docs), "question": RunnablePassthrough()}
        | prompt
        | _llm
        | StrOutputParser()
    )

# --- 3. Streamlit UI 및 메인 로직 (UI & Main Logic) ---

st.set_page_config(page_title="나만의 RAG 지식 센터", page_icon="🧠")
st.title("🧠 나만의 RAG 지식 센터")
st.write("PDF를 업로드하여 나만의 지식 베이스를 만들고, 자유롭게 질문해보세요!")

# --- 사이드바: 파일 업로드 및 DB 관리 ---
with st.sidebar:
    st.header("지식 베이스 관리")
    
    uploaded_files = st.file_uploader(
        "여기에 PDF 파일을 드래그 앤 드롭하세요",
        type="pdf",
        accept_multiple_files=True
    )

    if st.button("지식 베이스 업데이트"):
        if uploaded_files:
            if not os.path.exists(SOURCE_DOCS_DIR):
                os.makedirs(SOURCE_DOCS_DIR)

            for file in uploaded_files:
                file_path = os.path.join(SOURCE_DOCS_DIR, file.name)
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())
            st.success(f"{len(uploaded_files)}개의 PDF 파일을 저장했습니다.")

            with st.spinner("PDF를 처리하여 지식 베이스를 업데이트하는 중입니다..."):
                process_all_pdfs()
                setup_vector_store()
                st.cache_resource.clear()
            st.success("지식 베이스 업데이트 완료!")
            st.rerun()
        else:
            st.warning("업데이트할 PDF 파일을 먼저 선택해주세요.")

# --- 메인 화면: QA 챗봇 ---

retriever = load_retriever()
llm = load_llm()

if retriever and llm:
    rag_chain = create_rag_chain(retriever, llm)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_prompt := st.chat_input("지식 베이스에 대해 질문해보세요."):
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("답변을 생성하는 중입니다..."):
                response = rag_chain.invoke(user_prompt)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.info("왼쪽 사이드바에서 PDF 파일을 업로드하고 '지식 베이스 업데이트' 버튼을 눌러주세요.")
    