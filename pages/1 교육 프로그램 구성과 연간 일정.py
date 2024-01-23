import streamlit as st
import os

st.set_page_config(page_title="EGD 교육 구성과 일정", layout="wide")

if st.session_state.get('logged_in', False):  # 로그인 상태 확인

    st.header("AMC GI EGD 교육 프로그램 구성과 연간 일정")
    st.markdown("서울 아산병원 **GI C**에서 시행되는 내시경 교육 프로그램의 구성과 연간 일정을 보여주는 표입니다.")
    st.markdown("현 페이지의 정보는 2024년 1월에 작성된 것으로 **2024년**에 근무하는 선생님들을 위한 정보입니다.")
    st.markdown("구성표와 일정표를 다운로드 하려면 맨 아래 '파일 다운로드' 버튼을 눌러주세요")
    st.divider()
    st.image('./images/contents.png', caption='2023년 소화기 상부 내시경 교육 프로그램 구성표')
    st.divider()
    st.image('./images/schedule.png', caption='2023년 소화기 상부 내시경 교육 프로그램 연간 일정표')
    st.divider()

    file_path = './pages/data/EGD_training_programs.xlsx'

    if os.path.isfile(file_path):
        btn = st.download_button(
            label="파일 다운로드",
            data=open(file_path, "rb").read(),
            key="contents_download_button",
            file_name=os.path.basename(file_path),
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("파일을 찾을 수 없습니다. 'contents.xlsx' 파일이 현재 폴더에 존재해야 합니다.")

else:
    st.warning('Please log in to read more.')