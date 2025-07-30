import fitz  # PyMuPDF
import os
import glob

# --- 설정 ---
PDF_SOURCE_DIR = 'source_documents'
MARKDOWN_OUTPUT_DIR = 'processed_markdown'
IMAGE_OUTPUT_DIR = 'images'

# --- 출력 폴더 생성 ---
for dir_path in [MARKDOWN_OUTPUT_DIR, IMAGE_OUTPUT_DIR]:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def convert_pdf_to_md(pdf_path, md_dir, img_dir):
    """단일 PDF 파일을 마크다운으로 변환하고 이미지와 텍스트를 추출합니다."""
    try:
        doc = fitz.open(pdf_path)
        markdown_content = []
        base_filename = os.path.splitext(os.path.basename(pdf_path))[0]
        output_md_path = os.path.join(md_dir, f"{base_filename}.md")

        print(f"\n--- Processing: {pdf_path} ---")

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            
            # 1. 텍스트 추출
            text = page.get_text("text")
            if text.strip():
                markdown_content.append(text)
            
            # 2. 이미지 추출
            image_list = page.get_images(full=True)
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                image_filename = f"{base_filename}_page_{page_num + 1}_{img_index + 1}.{image_ext}"
                image_path = os.path.join(img_dir, image_filename)
                
                with open(image_path, "wb") as f:
                    f.write(image_bytes)
                
                markdown_image_tag = f"![{image_filename}]({image_path})\n"
                markdown_content.append(markdown_image_tag)

        with open(output_md_path, "w", encoding="utf-8") as md_file:
            md_file.write("\n".join(markdown_content))

        print(f"Successfully converted to {output_md_path}")
        return True

    except Exception as e:
        print(f"Error converting {pdf_path}: {e}")
        return False

def main():
    """source_documents 폴더의 모든 PDF를 마크다운으로 변환합니다."""
    pdf_files = glob.glob(os.path.join(PDF_SOURCE_DIR, '*.pdf'))
    
    if not pdf_files:
        print(f"No PDF files found in '{PDF_SOURCE_DIR}'.")
        return

    print(f"Found {len(pdf_files)} PDF file(s) to convert.")
    success_count = 0
    for pdf_file in pdf_files:
        if convert_pdf_to_md(pdf_file, MARKDOWN_OUTPUT_DIR, IMAGE_OUTPUT_DIR):
            success_count += 1
            
    print(f"\n--- Conversion Complete ---")
    print(f"{success_count} out of {len(pdf_files)} files converted successfully.")

if __name__ == "__main__":
    main()