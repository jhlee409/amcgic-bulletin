import streamlit as st
import requests
import json

st.set_page_config(page_title="AMC GI C", layout="wide")

# Streamlit 페이지 설정
st.title("서울 아산병원 GI 상부 게시판")					
st.header("Login page")
st.markdown(
    '''
    1. 이 게시판은 서울 아산병원 GI 상부 전용 게시판입니다.
    1. GI 상부의 교육 관련 공지사항 전달과 문서 자료 제공을 위한 공간입니다. 일반 공지는 취급하지 않습니다.
    1. 처음 접속하는 선새님은 반드시 게시판에 실명으로 접속확인을 위한 댓글을 남겨주세요.
    '''
)
st.divider()

# 사용자 인풋
email = st.text_input("Email")
password = st.text_input("Password", type="password")

# 로그인 버튼
if st.button("Login"):
    try:
        # Streamlit secret에서 Firebase API 키 가져오기
        api_key = st.secrets["FIREBASE_API_KEY"]
        request_ref = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
        headers = {"Content-Type": "application/json"}
        data = json.dumps({"email": email, "password": password, "returnSecureToken": True})

        response = requests.post(request_ref, headers=headers, data=data)
        response_data = response.json()

        if response.status_code == 200:
            st.success(f"{email}님, 로그인에 성공하셨습니다. 이제 왼쪽의 메뉴를 이용하실 수 있습니다.")
            st.session_state['logged_in'] = True
            st.session_state['user_email'] = email  # 이메일 주소를 세션 상태에 저장
        else:
            st.error(response_data["error"]["message"])
    except Exception as e:
        st.error("An error occurred: " + str(e))

# 로그 아웃 버튼
if "logged_in" in st.session_state and st.session_state['logged_in']:
    
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.success("로그아웃 되었습니다.")
        # 필요시 추가적인 세션 상태 초기화 코드
        # 예: del st.session_state['logged_in']

user_email = st.session_state.get('user_email', 'unknown')  # 세션에서 이메일 가져오기