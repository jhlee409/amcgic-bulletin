import streamlit as st
import firebase_admin
from firebase_admin import credentials, storage
import os
import tempfile
from datetime import datetime
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

# 사용자 입력
password = st.text_input("Password", type="password")
name = st.text_input("Your Name (예: 홍길동)")
position = st.selectbox("Select Position", ["", "Staff", "F1", "F2 ", "R3", "Student", "신촌", "계명"])

# 로그인 버튼
if st.button("Login"):
    # 입력 검증
    validation_passed = True
    
    if not name.strip():
        st.error("한글 이름을 입력해 주세요")
        validation_passed = False
    elif not any(0xAC00 <= ord(char) <= 0xD7A3 for char in name):
        st.error("한글 이름을 입력해 주세요")
        validation_passed = False

    if not position.strip():
        st.error("position을 선택해 주세요")
        validation_passed = False

    if not password.strip():
        st.error("비밀번호를 입력해 주세요")
        validation_passed = False

    # 모든 검증을 통과한 경우에만 로그인 처리
    if validation_passed:
        if password == "3180":
            st.success(f"로그인에 성공하셨습니다. 이제 왼쪽의 메뉴를 이용하실 수 있습니다.")
            st.session_state['logged_in'] = True
            st.session_state['user_position'] = position
            st.session_state['user_name'] = name
            
            # 로그인 시간 기록
            login_time = datetime.now(timezone('Asia/Seoul'))
            st.session_state['login_time'] = login_time
            login_time_str = login_time.strftime("%Y_%m_%d_%H_%M_%S")
            
            # 날짜와 사용자 이름 기반 텍스트 파일 생성
            current_date = datetime.now(timezone('Asia/Seoul')).strftime("%Y-%m-%d")
            filename = f"{position}*{name}*bulletin"
            file_content = f"{position}*{name}*bulletin\n"
            
            # 로그인 로그 파일 생성
            login_filename = f"{position}*{name}*login*{login_time_str}"
            login_file_content = f"{position}*{name}*login*{login_time_str}\n"

            # 임시 디렉토리에 파일 저장
            with tempfile.TemporaryDirectory() as temp_dir:
                # 기존 bulletin 로그 파일 저장
                temp_file_path = os.path.join(temp_dir, filename)
                with open(temp_file_path, "w", encoding="utf-8") as file:
                    file.write(file_content)

                # 로그인 로그 파일 저장
                login_file_path = os.path.join(temp_dir, login_filename)
                with open(login_file_path, "w", encoding="utf-8") as file:
                    file.write(login_file_content)

                # Firebase Storage에 업로드
                try:
                    # bulletin 로그 업로드
                    blob = bucket.blob(f"log_bulletin/{filename}")
                    blob.upload_from_filename(temp_file_path)
                    
                    # 로그인 로그 업로드 (임시 저장)
                    login_blob = bucket.blob(f"log_login/{login_filename}")
                    login_blob.upload_from_filename(login_file_path)
                    # 로그인 파일 경로 저장
                    st.session_state['login_blob_path'] = f"log_login/{login_filename}"
                except Exception as e:
                    st.error("로그 자료 업로드 중 오류가 발생했습니다: " + str(e))
        else:
            st.error("로그인에 실패했습니다. 비밀번호를 확인하세요.")

# 로그아웃 버튼
if "logged_in" in st.session_state and st.session_state['logged_in']:
    if st.sidebar.button("Logout"):
        # 로그아웃 시간 기록
        logout_time = datetime.now(timezone('Asia/Seoul'))
        logout_time_str = logout_time.strftime("%Y_%m_%d_%H_%M_%S")
        
        # 사용 시간 계산 (시간:분 형식)
        if 'login_time' in st.session_state:
            login_time = st.session_state['login_time']
            duration_seconds = (logout_time - login_time).total_seconds()
            hours = int(duration_seconds // 3600)
            minutes = int((duration_seconds % 3600) // 60)
            duration_str = f"{hours}:{minutes:02d}"
            
            # 로그아웃 및 사용 시간 로그 파일 생성
            position = st.session_state['user_position']
            name = st.session_state['user_name']
            
            logout_filename = f"{position}*{name}*logout*{logout_time_str}"
            logout_file_content = f"{position}*{name}*logout*{logout_time_str}\n"
            
            duration_filename = f"{position}*{name}*duration"
            duration_file_content = f"{position}*{name}*{duration_str}\n"
            
            # 임시 디렉토리에 파일 저장 및 업로드
            with tempfile.TemporaryDirectory() as temp_dir:
                # 로그아웃 로그 파일 저장
                logout_file_path = os.path.join(temp_dir, logout_filename)
                with open(logout_file_path, "w", encoding="utf-8") as file:
                    file.write(logout_file_content)
                
                # 사용 시간 로그 파일 저장
                duration_file_path = os.path.join(temp_dir, duration_filename)
                with open(duration_file_path, "w", encoding="utf-8") as file:
                    file.write(duration_file_content)
                
                # Firebase Storage에 업로드
                try:
                    # 로그아웃 로그 업로드 (임시 저장)
                    logout_blob = bucket.blob(f"log_logout/{logout_filename}")
                    logout_blob.upload_from_filename(logout_file_path)
                    logout_blob_path = f"log_logout/{logout_filename}"
                    
                    # 사용 시간 로그 업로드
                    duration_blob = bucket.blob(f"log_duration/{duration_filename}")
                    duration_blob.upload_from_filename(duration_file_path)
                    
                    # 사용 시간 저장 후 로그인/로그아웃 로그 삭제
                    if 'login_blob_path' in st.session_state:
                        login_blob = bucket.blob(st.session_state['login_blob_path'])
                        login_blob.delete()
                    
                    logout_blob = bucket.blob(logout_blob_path)
                    logout_blob.delete()
                except Exception as e:
                    st.error("로그 처리 중 오류가 발생했습니다: " + str(e))
        
        # 세션 상태 초기화
        st.session_state['logged_in'] = False
        if 'login_time' in st.session_state:
            del st.session_state['login_time']
        if 'login_blob_path' in st.session_state:
            del st.session_state['login_blob_path']
        st.success("로그아웃 되었습니다.")
