from typing import Optional

from google.api_core.client_options import ClientOptions
from google.cloud import documentai  # Google Document AI 라이브러리

# 실행 전에 아래 변수들을 설정하세요.
project_id = "black-function-419515"  # Google Cloud 프로젝트 ID
location = "us"  # 위치 설정 ('us' 또는 'eu')
processor_id = "f4b5c33f1f6cc1cd"  # 프로세서 ID, 프로세서 생성 필요
file_path = "seonwooNote.pdf"  # 처리할 파일 경로
mime_type = "application/pdf"  # 파일 타입, 지원하는 파일 타입 확인 필요
field_mask = "text,entities,pages.pageNumber"  # 반환받을 필드 선택 (옵션)
processor_version_id = "pretrained-ocr-v2.0-2023-06-02"  # 프로세서 버전 (옵션)


def process_document_sample(
        project_id: str,
        location: str,
        processor_id: str,
        file_path: str,
        mime_type: str,
        field_mask: Optional[str] = None,
        processor_version_id: Optional[str] = None,
) -> None:
    # API 엔드포인트 설정
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # 프로세서 경로 설정
    if processor_version_id:
        name = client.processor_version_path(project_id, location, processor_id, processor_version_id)
    else:
        name = client.processor_path(project_id, location, processor_id)

    # 파일을 읽어서 내용을 image_content 변수에 저장
    with open(file_path, "rb") as image:
        image_content = image.read()

    # RawDocument 객체 생성
    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    # 문서 처리 요청 구성
    request = documentai.ProcessRequest(
        name=name,
        raw_document=raw_document,
        field_mask=field_mask,
    )

    # 문서 처리 및 결과 출력
    result = client.process_document(request=request)
    document = result.document
    print("The document contains the following text:")
    print(document.text)


# 메인 함수
if __name__ == "__main__":
    process_document_sample(
        project_id,
        location,
        processor_id,
        file_path,
        mime_type,
        field_mask,
        processor_version_id,
    )
