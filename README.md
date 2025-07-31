# PDF 기반 질의응답 챗봇

이 프로젝트는 PDF 문서를 기반으로 사용자의 질문에 답변하는 RAG (Retrieval-Augmented Generation) 챗봇 애플리케이션입니다. Streamlit을 사용하여 웹 인터페이스를 제공하며, LangChain 프레임워크와 ChromaDB 벡터 스토어를 활용하여 구현되었습니다.

## 주요 기능

- **동적 PDF 처리:** 사용자가 웹 UI에서 직접 PDF 파일을 업로드하면, 실시간으로 텍스트를 추출하고 처리합니다.
- **자동 지식 베이스 구축:** 업로드된 PDF 내용은 자동으로 텍스트로 변환되고, 의미 기반의 벡터로 임베딩되어 ChromaDB에 저장됩니다.
- **대화형 챗봇 인터페이스:** 사용자가 자연어로 질문을 입력하고 문서 기반의 답변을 받을 수 있는 직관적인 채팅 UI를 제공합니다.
- **RAG 기반 답변 생성:** 사용자의 질문과 가장 관련성이 높은 문서 조각을 벡터 저장소에서 검색하고, 이를 근거로 Gemini LLM이 정확하고 신뢰도 높은 답변을 생성합니다.
- **지식 베이스 관리:** 이미 추가된 PDF를 다시 업로드할 경우, 기존 내용을 삭제하고 새로 업데이트하는 덮어쓰기 기능을 지원합니다.

## 시스템 워크플로우

```
1. 사용자가 Streamlit 웹 앱 실행
   (streamlit run app.py)
       |
       V
2. 웹 UI에서 PDF 파일 업로드
       |
       V
3. PDF 텍스트 추출 및 분할 (document_processor.py)
       |
       V
4. 텍스트 벡터화 및 ChromaDB 저장 (vector_store_manager.py)
       |
       V
5. 사용자 질문 입력
       |
       V
6. 관련 문서 검색 (Retriever)
       |
       V
7. LLM(Gemini)을 통해 답변 생성 (rag_handler.py)
       |
       V
8. 웹 UI에 답변 출력
```

## 설치 방법

1.  **저장소 복제:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **필요한 라이브러리 설치:**
    `requirements.txt` 파일에 명시된 라이브러리를 설치합니다.
    ```bash
    pip install -r requirements.txt
    ```
3.  **환경 변수 설정:**
    `.env` 파일을 생성하고, 아래와 같이 Gemini API 키를 입력합니다.
    ```
    GEMINI_API_KEY="YOUR_API_KEY"
    ```

## 사용 방법

1.  **챗봇 애플리케이션 실행:**
    다음 명령어를 터미널에 입력하여 Streamlit 앱을 실행합니다.
    ```bash
    streamlit run app.py
    ```

2.  **지식 베이스 구축:**
    - 웹 브라우저에 앱이 열리면, 왼쪽 사이드바의 파일 업로더를 사용하여 하나 이상의 PDF 파일을 업로드합니다.
    - 파일 선택 후 '지식 베이스 업데이트' 버튼을 클릭합니다.
    - 앱이 자동으로 파일을 처리하고 벡터 데이터베이스에 저장합니다.

3.  **질의응답:**
    - 지식 베이스 구축이 완료되면 메인 화면에 채팅 입력창이 나타납니다.
    - 업로드한 PDF 문서의 내용에 대해 자유롭게 질문하고 답변을 받을 수 있습니다.

## 프로젝트 구조

```
.
├── app.py                  # Streamlit 메인 애플리케이션
├── config.py               # API 키, 경로, 모델 설정
├── document_processor.py   # PDF 텍스트 추출 및 문서 분할
├── file_handler.py         # 파일 저장 및 경로 관리
├── rag_handler.py          # RAG 체인 및 LLM 핸들러
├── vector_store_manager.py # ChromaDB 벡터 저장소 관리
├── requirements.txt        # Python 라이브러리 의존성
├── source_documents/       # 업로드된 원본 PDF 저장
├── processed_markdown/     # 추출된 텍스트(마크다운) 저장
└── chroma_db/              # ChromaDB 벡터 데이터 저장
```

## 주요 의존성

-   `streamlit`
-   `langchain`
-   `langchain-google-genai`
-   `chromadb`
-   `sentence-transformers` (`ko-sroberta-multitask`)
-   `unstructured[md]`
-   `python-dotenv`

자세한 내용은 `requirements.txt` 파일을 참고하세요.