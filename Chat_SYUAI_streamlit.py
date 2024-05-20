import streamlit as st
from google.cloud import documentai
from google.api_core.client_options import ClientOptions
import google.generativeai as genai
import os
import toml
import json

config = st.secrets


# Google Cloud 자격 증명 환경 변수 설정
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/tmp/credentials.json'
with open(os.environ['GOOGLE_APPLICATION_CREDENTIALS'], 'w') as f:
    json.dump(json.loads(config['google_cloud']['credentials']), f)

# Google Cloud 설정 읽기
project_id = config.google_cloud.project_id
location = config.google_cloud.location
processor_id = config.google_cloud.processor_id
processor_version_id = config.google_cloud.processor_version_id
mime_type = "application/pdf"  # 파일 타입, 지원하는 파일 타입 확인 필요
field_mask = "text,entities,pages.pageNumber"  # 반환받을 필드 선택 (옵션)


# Google API 키 읽기
api_key = config.google_api.api_key

# Streamlit 페이지 설정
st.title("PDF 요약, 풀이 시스템. 15페이지 이하의 Pdf만 가능합니다.")

# 파일 업로더 초기화
uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'], key='file_uploader')

# 모델 로드 및 채팅 세션 시작
@st.experimental_singleton
def load_model():
    return genai.GenerativeModel('gemini-pro')

model = load_model()

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 사용자 입력 받기
user_input = st.text_input("추가로 입력할 메세지를 작성해주세요:")

# 채팅 메시지 처리
if st.button("Send"):
    if "pdf_text" in st.session_state:
        # PDF 내용과 사용자 입력 결합
        query = st.session_state.pdf_text + " " + user_input + " 에 대해서 정리하고 요약해줘."
    else:
        query = user_input + " 에 대해서 정리하고 요약해줘."

    response = model.generate_content(query)
    with st.container():
        with st.expander("See response"):
            st.write(response.text)

# PDF 파일 처리
if uploaded_file is not None:
    with st.spinner("Processing document..."):
        # 문서 처리 함수
        def process_document(uploaded_file):
            opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
            client = documentai.DocumentProcessorServiceClient(client_options=opts)
            name = client.processor_version_path(project_id, location, processor_id, processor_version_id)

            # 메모리에서 바로 파일 읽기
            image_content = uploaded_file.getvalue()
            raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)
            request = documentai.ProcessRequest(name=name, raw_document=raw_document, field_mask=field_mask)
            result = client.process_document(request=request)
            return result.document.text

        # PDF 텍스트 추출
        pdf_text = process_document(uploaded_file)
        st.session_state.pdf_text = pdf_text  # 상태 저장
        st.success("Document processed successfully.")
