import streamlit as st
import requests
import json
import streamlit_authenticator as stauth
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials, storage

st.set_page_config(page_title="AMC GI C", layout="wide")

# Streamlit 페이지 설정
st.title("서울 아산병원 GI 상부 게시판")					
st.header("Login page")
st.markdown(
    '''
    1. 이 게시판은 서울 아산병원 GI 상부 전용 게시판입니다.
    1. GI 상부의 교육 관련 공지사항 전달과 문서 자료 제공을 위한 공간입니다. 일반 공지는 취급하지 않습니다.
    '''
)
st.divider()

# 로그아웃 버튼 상태 관리
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# 로그인 상태에 따른 UI 표시
if not st.session_state.logged_in:
    # 사용자 ID 및 비밀번호 입력창 설정
    st.subheader("로그인 페이지")
    id = st.text_input("사용자 ID")
    password = st.text_input("비밀번호", type="password")

    # 로그인 버튼 추가
    login_button = st.button('로그인')

    # 로그인 버튼이 클릭되었을 때만 처리
    if login_button:
        # ID 및 비밀번호 확인
        is_login = id == "amcgi" and password == "3180"

        if is_login:
            # 로그인 성공 시 처리
            # 사용자 이메일과 접속 날짜 기록
            user_email = st.session_state.get('user_email', 'unknown')  # 세션에서 이메일 가져오기
            access_date = datetime.now().strftime("%Y-%m-%d")  # 현재 날짜 가져오기 (시간 제외)

            # 로그 내용을 문자열로 생성
            log_entry = f"Email: {user_email}, Access Date: {access_date}, Menu: EGD Hemostasis training\n"

            # Firebase Storage에 로그 파일 업로드
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
            firebase_admin.initialize_app(cred)
            bucket = storage.bucket('amcgi-bulletin.appspot.com')  # Firebase Storage 버킷 참조
            log_blob = bucket.blob(f'logs/{user_email}_{access_date}_EGD Hemostasis training.txt')  # 로그 파일 경로 설정
            log_blob.upload_from_string(log_entry, content_type='text/plain')  # 문자열로 업로드

            st.success("로그인에 성공하셨습니다. 이제 왼편의 각 프로그램을 사용하실 수 있습니다.")
            st.session_state.logged_in = True
            st.divider()
        else:
            st.error("로그인 정보가 정확하지 않습니다.")
else:
    # 로그인 성공 시 화면
    st.success("로그인에 성공하셨습니다. 이제 왼편의 각 프로그램을 사용하실 수 있습니다.")
    st.divider()
    
    # 로그아웃 버튼 생성
    if st.sidebar.button('로그아웃'):
        st.session_state.logged_in = False
        st.experimental_rerun()  # 페이지를 새로고침하여 로그인 화면으로 돌아감

    st.write("마지막 수정 날짜 및 수정사항: 2024년 10월 17일; 로그인 방식 변경; 연간 계획표에서 ID와 PW 제공")
