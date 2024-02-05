import streamlit as st
import pandas as pd
from datetime import datetime
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
import json

st.set_page_config(page_title="AMC GI C 게시판", layout="wide")
    
if st.session_state.get('logged_in', False):  # 로그인 상태 확인
    
    with st.container():
        st.header("상부 알림판")
        st.markdown(
            '''
                ---------------------------------------------------------------------------------------------------------------------------------------------------------
                1. 소화기 내시경 교육 동영상은 서울아산병원 시뮬레이션 센터 [Sim Class](https://edu.amc.seoul.kr/)에서 시청할 수 있습니다.
                    * ID 와 PW를 받아서 로그인 합니다.
                    * 필요한 동영상을 청취하면 자동으로 출석 처리 됩니다.
                1. AI 소화기 환자 병력 청취 훈련 프로그램과 EGD 병변 진단 훈련 프로그램은 [GI training program](https://gi-training.streamlit.app/) 웹페이지에 접속하여 ID는 amcgi이고, PW는 3180을 입력하시면 사용하실 수 있습니다.
                ---------------------------------------------------------------------------------------------------------------------------------------------------------
                1. 2월 후반부부터 3월 전반부에는 신임 전임의 1년차 선생님들 중에서 외부출신과 AMC 출신 중 EGD 교육 받지 않았던 선생님들의 EGD 교육이 있습니다.
                    * MT, SHT, EMT 과정을 한 달 안에 이수해야 합니다.
                    * 변소영 선생님께서는 해당 선생님들과 일정을 상의해서 교육이 진행되도록 해주세요.
                1. 외부출신 전임의 2년차 선생님께서는 EMT 시뮬레이터를 이진혁 선생님 앞에서 수행하면서 우리병원 검사 방식을 익히도록 합니다.
                    * 병원에 출근하고 2주정도 이내에 시행예정입니다. 시간은 20분 정도 걸릴 겁니다. 장소와 정확한 날짜 시간은 따로 알려주겠습니다.
                1. 2024년 3월부터 근무하는 신임 소화기 전임의 1년차 선생님들의 등록이 전원 완료되었습니다. 전체 EGD 교육과정과 일정에 대한 공지 사항이 이 게시판을 통해 전달되므로 잘 이용하세요.
                1. EGD 사진 Dx 훈련 프로그램에는 현재 7개의 증례가 올려져 있습니다. 사용해 보시고 문제가 있으면 게시글을 남기거나, 원내 메일을 보내 주세요. 아직 시작 단계라서, 많은 벌레가 있을 것으로 예상합니다. 본격적인 가동은 4월부터이고 매년 4월부터 다음해 2월까지 매월 18-20 증례가 올려질 예정입니다. 난이도에 따라 전임의 1년차와 2년차용 증례로 나뉘어 올려지는데, 물론 모두 해 보는 걸 권장합니다.
            '''
        )

# 로그 아웃 버튼
if "logged_in" in st.session_state and st.session_state['logged_in']:
    st.sidebar.divider()
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.success("로그아웃 되었습니다.")
        # 필요시 추가적인 세션 상태 초기화 코드
        # 예: del st.session_state['logged_in']
    
    # Check if Firebase app has already been initialized
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
        firebase_admin.initialize_app(cred)

    db = firestore.client()

    # Function to get the next document number
    def get_next_document_number():
        # Query all documents in the 'amcgic_comments' collection
        docs = db.collection('amcgic_comments').stream()
        
        # Extract document numbers, assume format 'documentXXXX'
        doc_numbers = [int(doc.id.replace('document', '')) for doc in docs]
        
        # Find the highest number and add one
        next_number = max(doc_numbers, default=0) + 1
        return f'document{next_number:04d}'

    # 댓글을 추가하는 함수
    def add_comment(author, title, text):
        comment = {
            'author': author,
            'title': title,  # Added title field
            'text': text,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        doc_name = get_next_document_number()
        db.collection('amcgic_comments').document(doc_name).set(comment)

    # Function to get the latest 10 comments
    def get_latest_comments():
        comments_query = db.collection('amcgic_comments').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(10)
        return comments_query.stream()

    # Streamlit app
    def main():
        # Using an expander for the comment form
        with st.expander("*댓글을 입력하려면 누르세요.*"):
            with st.form(key='comment_form'):
                name = st.text_input('이름')
                title = st.text_input('제목')  # Input field for title
                comment = st.text_area('내용', height=150)  # Adjust the height as needed
                submit_button = st.form_submit_button(label='Submit')

                if submit_button:
                    add_comment(name, title, comment)  # Updated function call
                    
    if __name__ == '__main__':
        main()

    # Display the latest 10 comments with serial numbers in separate columns
    st.markdown('### 최근 댓글')
    comment_counter = 1  # Initialize counter
    for comment in get_latest_comments():
        comment_data = comment.to_dict()

        # Check if the 'title' key exists in the comment data
        title = comment_data.get('title', '제목 없음')  # Default to '제목 없음' if 'title' is not found

        # Create a single row for each comment
        col1, col2 = st.columns([1,2])  # Adjust column widths as needed

        with col1:
            # Concatenate the comment details
            comment_details = f"{comment_counter}. 이름: {comment_data['author']} | 제목: {title} | 날짜: {comment_data['timestamp']}"
            st.text(comment_details)

        with col2:
            # Place the expander in the second column
            with st.expander("내용 보기"):
                st.write(comment_data['text'])

        # Increment the counter
        comment_counter += 1

    # Single line space after each comment
    st.write("\n")  # Adds a single line space
                
else:
    st.warning('Please log in to read more.')