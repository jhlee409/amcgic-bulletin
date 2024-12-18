import streamlit as st
import json
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, storage
import os
import tempfile
import re

st.set_page_config(page_title="AMC GI C")

# Firebase 초기화
if not firebase_admin._apps:
    # Streamlit Secrets에서 Firebase 설정 정보 로드
    cred = credentials.Certificate({
        "type": "service_account",
        "project_id": st.secrets["project_id"],
        "private_key_id": st.secrets["private_key_id"],
        "private_key": st.secrets["private_key"].replace('\\n', '\n'),
        "client_email": st.secrets["client_email"],
        "client_id": st.secrets["client_id"],
        "auth_uri": st.secrets["auth_uri"],
        "token_uri": st.secrets["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["client_x509_cert_url"],
        "universe_domain": st.secrets["universe_domain"]
    })
    firebase_admin.initialize_app(cred, {"storageBucket": "amcgi-bulletin.appspot.com"})

# Firebase Storage 버킷 참조
bucket_name = 'amcgi-bulletin.appspot.com'
bucket = storage.bucket(bucket_name)  # 항상 사용할 수 있도록 초기화

# Streamlit 페이지 설정
st.title("서울 아산병원 GI 상부 게시판")
st.header("Login page")
st.markdown(
    '''
    1. 이 게시판은 서울 아산병원 GI 상부 전용 게시판입니다.
    1. GI 상부의 교육 관련 공지사항 전달과 문서 자료 제공을 위한 공간입니다. 일반 공지는 취급하지 않습니다.
    1. 이름은 게시판에 접속하셨는지 확인하는 자료이므로 반드시 기입해 주세요.
    '''
)
st.divider()

# 세션 상태 초기화
if 'name' not in st.session_state:
    st.session_state.name = ""
if 'position' not in st.session_state:
    st.session_state.position = "Select Position"
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# 사용자 입력
name = st.text_input("Your Name (예: 홍길동)", key="name_input", value=st.session_state.name)
position = st.selectbox("Position", 
    ["Select Position", "Staff", "F1", "F2 ", "R3", "Student"],
    key="position_input",
    index=["Select Position", "Staff", "F1", "F2 ", "R3", "Student"].index(st.session_state.position))
password = st.text_input("Password", type="password", key="password_input")

# 한글 이름 확인 함수
def is_korean_name(name):
    return bool(re.match('^[가-힣]+$', name.strip()))

# 입력 유효성 검사
is_valid = True

if not name or not is_korean_name(name):
    st.error("한글 이름을 입력해 주세요")
    is_valid = False
if position == "Select Position":
    st.error("position을 선택해 주세요")
    is_valid = False
if not password:
    st.error("비밀번호를 입력해 주세요")
    is_valid = False

# 로그인 버튼
if st.button("Login", key="login_button"):
    if not is_valid:
        st.error("모든 정보를 올바르게 입력해주세요")
    elif password != "3180":
        st.error("비밀번호가 올바르지 않습니다")
    else:
        st.session_state.name = name
        st.session_state.position = position
        st.session_state.logged_in = True
        st.success(f"로그인에 성공하셨습니다. 이제 왼쪽의 메뉴를 이용하실 수 있습니다.")
        
        # 날짜와 사용자 이름 기반 텍스트 파일 생성
        current_date = datetime.now().strftime("%Y-%m-%d")
        filename = f"{position}*{name}*{current_date}"
        file_content = f"사용자: {name}\n직급: {position}\n날짜: {current_date}\n"

        # 임시 디렉토리에 파일 저장
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, filename)
            with open(temp_file_path, "w", encoding="utf-8") as file:
                file.write(file_content)

            # Firebase Storage에 업로드
            try:
                blob = bucket.blob(f"log_bulletin/{filename}")
                blob.upload_from_filename(temp_file_path)
            except Exception as e:
                st.error("Firebase 업로드 중 오류가 발생했습니다: " + str(e))

# 로그아웃 버튼
if "logged_in" in st.session_state and st.session_state['logged_in']:
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.success("로그아웃 되었습니다.")
