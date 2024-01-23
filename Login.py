import streamlit as st
import requests
import json
import streamlit_authenticator as stauth

st.set_page_config(page_title="AMC GI C")

# Streamlit 페이지 설정
st.title("서울 아산병원 GI 상부 게시판")					
st.header("Login page")
st.markdown(
    '''
    1. 이 게시판은 서울 아산병원 GI 상부 전용 게시판입니다.
    1. GI 상부의 교육 관련 공지사항 전달과 문서 자료 제공을 위한 공간입니다.
    1. 아래에 미리 등록하신 이메일 주소와 비밀 번호를 입력하시면, 옆의 sidebar에 있는 웹페이지를 이용할 수 있게됩니다.
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
        else:
            st.error(response_data["error"]["message"])
    except Exception as e:
        st.error("An error occurred: " + str(e))

st.divider()
st.write("2024년 1월 17일 코드 수정")
st.write("2024년 1월 24일 게시물 내용 수정")