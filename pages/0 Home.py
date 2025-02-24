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
                1. 소화기 내시경 교육 동영상은 [AMC GI 상부 Simulator training](https://amcgic-simulator.streamlit.app/)와 [AMC GI 상부 Education Program](https://amcgic-training.streamlit.app/)에서 시청할 수 있습니다.
                    * AMC GI 상부 Simulator training에 로그인 하기 위해서는 이메일 주소를 ID로 알파벳 글자와 숫자 섞어서 8자 이상의 PW를 이진혁 교수에게 메일로 보내 허락을 받고 등록한 후 들어갈 수 있습니다.
                      -각종 시뮬에이터를 사용하는 EGD basic and advancedcourse와 관련된 교육 자료를 시청하거나, 훈련 후 수행 동영상이나 결과 report를 업로드하는 웹페이지 입니다.
                    * AMC GI 상부 Education Program에 로그인 하기 위해서는 이메일 주소를 ID로 알파벳 글자와 숫자 섞어서 8자 이상의 PW를 이진혁 교수에게 메일로 보내 허락을 받고 등록한 후 들어갈 수 있습니다.
                      -AMC GI 상부 Education Program 웹페이지에는 소화기 내과 상부의 교육에 관련된 프로그램 모듈들이 있으므로 일정에 따라 학습하시면 됩니다.
                    * AMC GI 상부 교육 웹페이지들은 출석 체크가 되므로, 끝낼 때는 반드시 왼쪽 아래 로그아웃 버튼을 눌러 종결하세요. 그냥 나가면 출석처리가 안됩니다.
                1. 소화기 전임의 공통 프로그램 페이지에 NBI 리뷰 논문 링크를 적어 놓았습니다. 반드시 공부하기 바랍니다.
                '''
                # 1. 전임의 외래 참관 (2024): 새로 추가, 소화기 전임의 1년차에게만 해당하는 교육 프로그램입니다.
                #     * 최소 1달에 1회 / 1년에 12회 참관합니다.
                #     * 각 외래는 최장 1시간 정도만 참관합니다.
                #     * 외래 참관 후 링크된 문서에 날짜를 적습니다 (YYYY-MM-DD).
                #         + 1. [GIA 외래](https://docs.google.com/spreadsheets/d/1sJ4hPndCBE8j_NkteWZPB7R5sb8cmy1zRHLARH-mLJ8/edit?usp=sharing) - 상반기에는 최종기, 최원묵 교수님 외래를 하반기에는 최원묵, 정성원 교수님 외래를 참관합니다.
                #         + 2. [GIB 췌담도암 통합진료](https://docs.google.com/spreadsheets/d/1RNUF94DAvPpAU6dxJlnGi5T3w_8rWgATSG6Q1w4DSsU/edit?usp=sharing) - 매주 수요일 12:30-1:30 000통합진료 외래를 참관합니다.
                #         + 3. [GIC 식도암 통합진료](https://docs.google.com/spreadsheets/d/12W-hZsQnPqYPgUe_DxGe1NfYaTk5g5mrfRN_NkFTUOE/edit?usp=sharing) - 매주 금요일 09:00-10:00 통합진료 외래를 참관합니다.
                #         + 4. [GIC 위암 통합진료](https://docs.google.com/spreadsheets/d/1ni_0S6GDMt6uKjpNDPcmBLW1Za0zW-KrbaqKWjwEQRk/edit?usp=sharing) - 매주 화요일 16:00-17:00 통합진료 외래를 참관합니다.
                #         + 5. [GID 대장종양](https://docs.google.com/spreadsheets/d/1BRwxnp9wLSfE_Y99fquhw-AiW5pdw7qjZVnmAmDQ5AY/edit?usp=sharing) - 변정식, 양동훈 교수님 외래를 참관합니다.
                #         + 6. [GID IBD](https://docs.google.com/spreadsheets/d/1F9bHCCDq4UNux3Bi0_Za3pAGAxVFA7ENq4Fhcx2dWcw/edit?usp=sharing) - 황성욱 교수님 외래를 참관합니다.
                #         + 7. [GICD 기능질환](https://docs.google.com/spreadsheets/d/1-knhzdyZhTmJWOHpXILp7Umnwr9ztoQLiRJCnm2GMAw/edit?usp=sharing) - 정기욱, 김도훈 교수님 외래를 참관합니다.

                # 1. 2월 후반부부터 3월 전반부에는 신임 전임의 1년차 선생님들 중에서 외부출신과 AMC 출신 중 EGD 교육 받지 않았던 선생님들의 EGD 교육이 있습니다.
                #     * MT, SHT, EMT 과정을 한 달 안에 이수해야 합니다.
                #     * 변소영 선생님께서는 해당 선생님들과 일정을 상의해서 교육이 진행되도록 해주세요.
                # 1. 외부출신 전임의 2년차 선생님께서는 EMT 시뮬레이터를 이진혁 선생님 앞에서 수행하면서 우리병원 검사 방식을 익히도록 합니다.
                #     * 병원에 출근하고 2주정도 이내에 시행예정입니다. 시간은 20분 정도 걸릴 겁니다. 장소와 정확한 날짜 시간은 따로 알려주겠습니다.
                # 1. 2024년 3월부터 근무하는 신임 소화기 전임의 1년차 선생님들의 등록이 전원 완료되었습니다. 전체 EGD 교육과정과 일정에 대한 공지 사항이 이 게시판을 통해 전달되므로 잘 이용하세요.
        )

# 로그 아웃 버튼
if "logged_in" in st.session_state and st.session_state['logged_in']:
    
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