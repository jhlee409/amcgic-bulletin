import streamlit as st
import json
from datetime import datetime
from firebase_admin import credentials, storage, initialize_app
import os

st.set_page_config(page_title="AMC GI C", layout="wide")

# Firebase 초기화
firebase_credentials_path = st.secrets["FIREBASE_CREDENTIALS_PATH"]
initialize_app(firebase_credentials_path , {"storageBucket": "amcgi-bulletin.appspot.com"})
bucket = storage.bucket()

# Streamlit 페이지 설정
st.title("서울 아산병원 GI 상부 게시판")
st.header("Login page")
st.markdown(
    '''
    1. 이 게시판은 서울 아산병원 GI 상부 전용 게시판입니다.
    1. GI 상부의 교육 관련 공지사항 전달과 문서 자료 제공을 위한 공간입니다. 일반 공지는 취급하지 않습니다.
    1. 처음 접속하는 선생님은 반드시 게시판에 실명으로 접속확인을 위한 댓글을 남겨주세요.
    '''
)
st.divider()

# 사용자 입력
email = st.text_input("Email (예: amcgi)")
password = st.text_input("Password (예: 3180)", type="password")
name = st.text_input("Your Name (예: 홍길동)")

# 로그인 버튼
if st.button("Login"):
    if email == "amcgi" and password == "3180":
        if name.strip() == "":
            st.error("사용자 이름을 입력하세요.")
        else:
            st.success(f"{email}님, 로그인에 성공하셨습니다. 이제 왼쪽의 메뉴를 이용하실 수 있습니다.")
            st.session_state['logged_in'] = True
            st.session_state['user_email'] = email
            st.session_state['user_name'] = name
            
            # 날짜와 사용자 이름 기반 텍스트 파일 생성
            current_date = datetime.now().strftime("%Y-%m-%d")
            filename = f"{name}_{current_date}.txt"
            file_content = f"사용자: {name}\n날짜: {current_date}\n이메일: {email}"

            # 파일 저장
            with open(filename, "w", encoding="utf-8") as file:
                file.write(file_content)

            # Firebase Storage에 업로드
            try:
                blob = bucket.blob(f"users/{filename}")
                blob.upload_from_filename(filename)
                st.success(f"{filename} 파일이 성공적으로 Firebase Storage에 업로드되었습니다.")
            except Exception as e:
                st.error("Firebase 업로드 중 오류가 발생했습니다: " + str(e))
            finally:
                # 로컬 파일 삭제
                if os.path.exists(filename):
                    os.remove(filename)
    else:
        st.error("로그인에 실패했습니다. ID 또는 비밀번호를 확인하세요.")

# 로그아웃 버튼
if "logged_in" in st.session_state and st.session_state['logged_in']:
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.success("로그아웃 되었습니다.")
