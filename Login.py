import streamlit as st
import requests
import json
import streamlit_authenticator as stauth
import firebase_admin
from firebase_admin import credentials, storage
from datetime import datetime
import os

st.set_page_config(page_title="AMC GI C", layout="wide")

# Firebase 초기화
if not firebase_admin._apps:
    cred = credentials.Certificate('secret/amcgi-bulletin-4f317f4638ed.json')
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'amcgi-bulletin.appspot.com'
    })

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

def create_and_upload_log(name):
    # 현재 날짜 가져오기
    current_date = datetime.now().strftime("%Y%m%d")
    
    # 로그 파일 이름 생성
    filename = f"{name}_{current_date}.txt"
    
    # 로그 파일 생성
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Login Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"User Name: {name}\n")
    
    try:
        # Firebase Storage에 업로드
        bucket = storage.bucket()
        blob = bucket.blob(f'login_logs/{filename}')
        blob.upload_from_filename(filename)
        
        # 로컬 파일 삭제
        os.remove(filename)
        return True
    except Exception as e:
        st.error(f"로그 업로드 중 오류 발생: {str(e)}")
        if os.path.exists(filename):  # 에러 발생 시 로컬 파일 정리
            os.remove(filename)
        return False

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

        if is_login:
            # 로그인 성공 시 처리
            st.success("로그인에 성공하셨습니다. 이제 왼편의 각 프로그램을 사용하실 수 있습니다.")
            st.session_state.logged_in = True
            st.session_state.user_name = name  # 이름을 세션 상태에 저장
            
            # 이름이 비어있지 않은 경우 로그 파일 생성 및 업로드
            if name.strip():
                if create_and_upload_log(name):
                    st.info(f"{name}님의 로그인이 기록되었습니다.")
            
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
        st.rerun()  # 페이지를 새로고침하여 로그인 화면으로 돌아감

    st.write("마지막 수정 날짜 및 수정사항: 2024년 10월 17일; 로그인 방식 변경; 연간 계획표에서 ID와 PW 제공")
