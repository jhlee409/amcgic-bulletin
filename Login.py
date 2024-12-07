import streamlit as st
import requests
import json
import streamlit_authenticator as stauth
import firebase_admin
from firebase_admin import credentials, storage
from datetime import datetime
import tempfile
import os

# Initialize Firebase if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("c:/Users/jhlee/OneDrive - UOU/Endoscopy education system/EGD_training_progmramming/project_amcgic_bulletin/secret/amcgi-bulletin-4f317f4638ed.json")
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'amcgi-bulletin.appspot.com'
    })

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
    name = st.text_input("이름")  

    # 로그인 버튼 추가
    login_button = st.button('로그인')

    # 로그인 버튼이 클릭되었을 때만 처리
    if login_button:
        # ID 및 비밀번호 확인
        is_login = id == "amcgi" and password == "3180"

        if is_login and name:  
            # Create log file
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_filename = f"{name}_{current_time}.txt"
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
                temp_file.write(f"Login Time: {current_time}\n")
                temp_file.write(f"User Name: {name}\n")
                temp_file_path = temp_file.name

            try:
                # Upload to Firebase Storage
                bucket = storage.bucket()
                blob = bucket.blob(f"login_logs/{log_filename}")
                blob.upload_from_filename(temp_file_path)
                
                # Clean up temporary file
                os.unlink(temp_file_path)
                
                # 로그인 성공 시 처리
                st.success("로그인에 성공하셨습니다. 이제 왼편의 각 프로그램을 사용하실 수 있습니다.")
                st.session_state.logged_in = True
                st.divider()
            except Exception as e:
                st.error(f"로그 파일 업로드 중 오류가 발생했습니다: {str(e)}")
        else:
            if not is_login:
                st.error("로그인 정보가 정확하지 않습니다.")
            if not name:
                st.warning("이름을 입력해주세요.")
else:
    # 로그인 성공 시 화면
    st.success("로그인에 성공하셨습니다. 이제 왼편의 각 프로그램을 사용하실 수 있습니다.")
    st.divider()
    
    # 로그아웃 버튼 생성
    if st.sidebar.button('로그아웃'):
        st.session_state.logged_in = False
        st.rerun()  

    st.write("마지막 수정 날짜 및 수정사항: 2024년 10월 17일; 로그인 방식 변경; 연간 계획표에서 ID와 PW 제공")
