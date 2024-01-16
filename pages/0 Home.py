import streamlit as st
import pandas as pd
from datetime import datetime
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
import json

st.set_page_config(page_title="AMC GI C 게시판")
    
if st.session_state.get('logged_in', False):  # 로그인 상태 확인
    
    with st.container():
        st.header("상부 알림판")
        st.markdown(
            '''
                1. 소화기 내시경 교육 동영상은 서울아산병원 시뮬레이션 센터 [Sim Class](https://edu.amc.seoul.kr/)에서 시청할 수 있습니다.
                    1. ID 와 PW를 받아서 로그인 합니다.
                    1. 필요한 동영상을 청취하면 자동으로 출석 처리 됩니다.
                1. AI 소화기 환자 병력 청취 훈련 프로그램은 훈련 프로그램 웹페이지 [AI patient Hx taking program](https://amcgi-22questions.streamlit.app/)에 접속하여 ID는 amcgi PW는 3180을 입력하시면 사용하실 수 있습니다.
            '''
        )
    st.divider()
    
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
    def add_comment(author, text):
        comment = {
            'author': author,
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
                comment = st.text_area('내용', height=150)  # Adjust the height as needed
                submit_button = st.form_submit_button(label='Submit')

                if submit_button:
                    add_comment(name, comment)
                    
    if __name__ == '__main__':
        main()

    # Display the latest 10 comments with serial numbers in separate columns
    st.markdown('### 최근 댓글')
    comment_counter = 1  # Initialize counter
    for comment in get_latest_comments():
        comment_data = comment.to_dict()

        # Create columns: Serial number, Name and Date, Content
        col1, col2, col3 = st.columns([1, 20, 30])
        with col1:
            st.markdown(f'**{comment_counter}**')
        with col2:
            st.text(f"이름: {comment_data['author']}")
            st.text(f"날짜: {comment_data['timestamp']}")
        with col3:
            with st.expander("내용 보기"):
                st.write(comment_data['text'])

        # Increment the counter
        comment_counter += 1

        # Single line space after each comment
        st.write("\n")  # Adds a single line space
            
else:
    st.warning('Please log in to read more.')