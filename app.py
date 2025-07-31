import streamlit as st
import os

# --- 모듈 임포트 ---
import file_handler
import document_processor
from vector_store_manager import VectorStoreManager
import rag_handler

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="brain training", page_icon="🧠")
st.title("🧠 brain training")

# --- 2. 시스템 초기화 (세션 상태 기반) ---
if 'initialized' not in st.session_state:
    with st.spinner("시스템을 초기화하고 모델을 로드 중입니다..."):
        rag_handler.download_embedding_model_if_needed()
        st.session_state.llm = rag_handler.get_llm()
        st.session_state.vector_manager = VectorStoreManager()
        st.session_state.initialized = True
        st.rerun() # 초기화 후 한번 더 실행하여 스피너를 지움

# 초기화된 객체 가져오기
llm = st.session_state.llm
vector_manager = st.session_state.vector_manager

# --- 3. 사이드바 UI ---
with st.sidebar:
    st.header("지식 베이스 관리")
    
    uploaded_files = st.file_uploader(
        "PDF 파일을 선택하세요",
        type="pdf",
        accept_multiple_files=True
    )

    if uploaded_files:
        if 'overwrite_choices' not in st.session_state:
            st.session_state.overwrite_choices = {}

        st.markdown("--- ")
        for file in uploaded_files:
            if file_handler.pdf_exists(file.name):
                st.session_state.overwrite_choices[file.name] = st.checkbox(f"'{file.name}' 덮어쓰기", key=f"cb_{file.name}")
            else:
                st.write(f"- '{file.name}' (새 파일)")
        st.markdown("--- ")

        if st.button("지식 베이스 업데이트"):
            with st.spinner("선택된 파일로 지식 베이스를 업데이트합니다..."):
                for file in uploaded_files:
                    is_new_file = not file_handler.pdf_exists(file.name)
                    should_overwrite = st.session_state.overwrite_choices.get(file.name, False)

                    if is_new_file or should_overwrite:
                        pdf_path = file_handler.save_uploaded_pdf(file)
                        md_filename = os.path.basename(file_handler.get_md_path(file.name))
                        
                        if should_overwrite:
                            vector_manager.delete_documents(md_filename)
                        
                        md_path = document_processor.extract_text_from_pdf(pdf_path)
                        if md_path:
                            docs = document_processor.load_and_split_document(md_path)
                            vector_manager.add_documents(docs)
                            st.write(f"✅ '{file.name}' 처리 완료")
            
            st.success("지식 베이스 업데이트 완료!")
            # 벡터 매니저를 새로고침하여 변경사항을 반영
            st.session_state.vector_manager = VectorStoreManager()
            st.rerun()

# --- 4. 메인 화면 QA 인터페이스 ---
retriever = vector_manager.get_retriever()

if retriever:
    rag_chain = rag_handler.create_rag_chain(retriever, llm)

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
    st.info("왼쪽 사이드바에서 PDF를 업로드하고 '지식 베이스 업데이트' 버튼을 눌러주세요.")
