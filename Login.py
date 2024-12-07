import streamlit as st
import requests
import json
import streamlit_authenticator as stauth
import datetime
import firebase_admin
from firebase_admin import storage
from firebase_admin import credentials

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

        if is_login:
            # 로그인 성공 시 처리
            st.success("로그인에 성공하셨습니다. 이제 왼편의 각 프로그램을 사용하실 수 있습니다.")
            st.session_state.logged_in = True
            st.session_state.user_name = name  # 이름을 세션 상태에 저장
            st.divider()

            # 로그 파일 생성
            if st.session_state.user_name:
                # 현재 날짜 가져오기
                today = datetime.datetime.now().strftime("%Y%m%d")
                log_file_name = f"{st.session_state.user_name}_{today}.txt"
                
                # 로그 파일 내용 작성
                log_content = f"사용자: {st.session_state.user_name}\n로그인 날짜: {datetime.datetime.now()}\n"
                
                # 로그 파일 저장
                with open(log_file_name, "w") as log_file:
                    log_file.write(log_content)

                # Firebase Storage에 파일 업로드
                if not firebase_admin._apps:
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
                    # storageBucket을 하드코딩
                    firebase_admin.initialize_app(cred, {'storageBucket': 'your-project-id.appspot.com'})  # 여기에 실제 버킷 이름을 입력하세요.

                # 버킷 이름을 하드코딩
                bucket_name = 'your-project-id.appspot.com'  # 여기에 실제 버킷 이름을 입력하세요.
                bucket = storage.bucket(bucket_name)  # 버킷 이름을 명시적으로 설정
                blob = bucket.blob(log_file_name)
                blob.upload_from_filename(log_file_name)

                st.success(f"{log_file_name} 파일이 Firebase Storage에 업로드되었습니다.")
        else:
            st.error("로그인 정보가 정확하지 않습니다.")
else:
    # 로그인 성공 시 화면
    st.success("로그인에 성공하셨습니다. 이제 왼편의 각 프로그램을 사용하실 수 있습니다.")
    st.divider()
    
    # 로그아웃 버튼 생성
    if st.sidebar.button('로그아웃'):
        st.session_state.logged_in = False
        # st.experimental_rerun()  # 페이지를 새로고침하여 로그인 화면으로 돌아감

    st.write("마지막 수정 날짜 및 수정사항: 2024년 10월 17일; 로그인 방식 변경; 연간 계획표에서 ID와 PW 제공")
