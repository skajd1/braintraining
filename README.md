# PDF 기반 질의응답 챗봇

이 프로젝트는 PDF 문서를 기반으로 사용자의 질문에 답변하는 RAG (Retrieval-Augmented Generation) 챗봇 애플리케이션입니다. Streamlit을 사용하여 웹 인터페이스를 제공하며, LangChain 프레임워크와 ChromaDB 벡터 스토어를 활용하여 구현되었습니다.

## 주요 기능

- **PDF 문서 처리:** `source_documents` 폴더에 있는 PDF 파일을 Markdown 형식으로 변환합니다.
- **벡터 데이터베이스 생성:** 변환된 텍스트를 의미 기반의 벡터로 임베딩하고 ChromaDB에 저장하여 빠른 검색을 가능하게 합니다.
- **챗봇 인터페이스:** 사용자가 자연어로 질문을 입력하고 문서 기반의 답변을 받을 수 있는 대화형 웹 UI를 제공합니다.
- **답변 생성:** 사용자의 질문과 가장 관련성이 높은 문서 조각을 검색하고, 이를 바탕으로 LLM(Large Language Model)이 답변을 생성합니다.

## 시스템 구성도

```
1. PDF 파일 입력
   (source_documents)
       |
       V
2. PDF -> Markdown 변환
   (pdf_to_md.py)
       |
       V
3. 텍스트 분할 및 벡터화
   (setup_chroma.py)
       |
       V
4. ChromaDB 벡터 저장소
   (chroma_db)
       |
       V
5. Streamlit 챗봇 앱
   (app.py)
   - 사용자 질문 입력
   - DB에서 관련 문서 검색
   - LLM으로 답변 생성
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

## 사용 방법

1.  **PDF 파일 준비:**
    질의응답의 기반으로 삼고 싶은 PDF 파일들을 `source_documents` 폴더에 넣어주세요.

2.  **PDF를 Markdown으로 변환:**
    다음 스크립트를 실행하여 PDF 파일을 텍스트로 변환합니다. 변환된 파일은 `processed_markdown` 폴더에 저장됩니다.
    ```bash
    python pdf_to_md.py
    ```

3.  **벡터 데이터베이스 설정:**
    변환된 텍스트를 벡터화하여 ChromaDB에 저장합니다.
    ```bash
    python setup_chroma.py
    ```

4.  **챗봇 애플리케이션 실행:**
    Streamlit 앱을 실행하여 챗봇을 시작합니다.
    ```bash
    streamlit run app.py
    ```
    웹 브라우저에서 앱이 열리면 질문을 입력하여 답변을 받을 수 있습니다.

## 주요 의존성

-   `streamlit`
-   `langchain`
-   `chromadb`
-   `sentence-transformers` (`ko-sroberta-multitask`)
-   `PyMuPDF`

자세한 내용은 `requirements.txt` 파일을 참고하세요.
