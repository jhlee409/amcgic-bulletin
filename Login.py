import streamlit as st
import firebase_admin
from firebase_admin import credentials, storage
import os
import tempfile
from datetime import datetime, timezone
from pytz import timezone

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
    1. GI 상부의 교육 관련 공지사항 전달과 문서 자료 제공을 위한 공간입니다. 일반 진료 및 행정 공지는 취급하지 않습니다.
    1. 한글 이름은 게시판에 접속하셨는지 확인하는 자료이므로 반드시 기입해 주세요.
    '''
)
st.divider()

# 초기화
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "password" not in st.session_state:
    st.session_state["password"] = ""

# 입력 필드
name = st.text_input("이름", value="")
position = st.text_input("직급", value="")
password = st.text_input("비밀번호", value=st.session_state["password"], type="password")
st.session_state["password"] = password

# 검증
show_login_button = True

if not name.strip():
    st.error("한글 이름을 입력해 주세요")
    show_login_button = False
if name.strip() and not any(0xAC00 <= ord(char) <= 0xD7A3 for char in name):
    st.error("한글 이름을 입력해 주세요")
    show_login_button = False

if not position.strip():
    st.error("position을 선택해 주세요")
    show_login_button = False

if not password.strip():
    st.error("비밀번호를 입력해 주세요")
    show_login_button = False

# 상태 확인
st.write("Session State:", st.session_state)
st.write("Final show_login_button state:", show_login_button)

# 로그인 버튼
if show_login_button:
    if st.button("Login"):
        if password == "3180":
            st.success(f"로그인에 성공하셨습니다. 이제 왼쪽의 메뉴를 이용하실 수 있습니다.")
            st.session_state['logged_in'] = True
            st.session_state['user_name'] = name
            st.session_state['user_position'] = position

            # 로그 파일 생성 및 업로드
            current_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            filename = f"{position}*{name}*{current_date}.txt"
            file_content = f"사용자: {name}\n직급: {position}\n날짜: {current_date}\n"

            with tempfile.TemporaryDirectory() as temp_dir:
                temp_file_path = os.path.join(temp_dir, filename)
                with open(temp_file_path, "w", encoding="utf-8") as file:
                    file.write(file_content)

                # Firebase Storage 업로드 (예외 처리)
                try:
                    blob = bucket.blob(f"log_bulletin/{filename}")
                    blob.upload_from_filename(temp_file_path)
                except Exception as e:
                    st.error("로그 자료 업로드 중 오류가 발생했습니다: " + str(e))
        else:
            st.error("로그인에 실패했습니다. 비밀번호를 확인하세요.")

# 로그아웃 버튼
if "logged_in" in st.session_state and st.session_state['logged_in']:
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.success("로그아웃 되었습니다.")
