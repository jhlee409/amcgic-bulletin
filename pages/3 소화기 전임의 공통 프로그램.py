import streamlit as st
import os

st.set_page_config(page_title="Fellow", layout="wide")

if st.session_state.get('logged_in', False):  # 로그인 상태 확인

    st.header("AMC 소화기 내과 전임의 공통 교육 과정 설명")
    st.markdown("이 페이지는 AMC **GI 전임의 1년차 및 상부 전임의 2년차**를 모두 대상으로하는 EGD 교육 과정의 공통 설명입니다.")

    # 로그 아웃 버튼
    if "logged_in" in st.session_state and st.session_state['logged_in']:

        if st.sidebar.button("Logout"):
            st.session_state['logged_in'] = False
            st.success("로그아웃 되었습니다.")
            # 필요시 추가적인 세션 상태 초기화 코드
            # 예: del st.session_state['logged_in'

    st.divider()

    tab1, tab2, tab3 = st.tabs(["공통 당부사항", "공통 프로그램 설명", "temp"])

    with tab1:
        st.subheader("소화기 전임의에게 드리는 당부")
        st.markdown(
            '''
            1. 내시경 검사 건수가 많습니다. 검사가 정시에 마칠 수 있도록 여러분의 도움이 절실합니다.
            1. 1년 수련기간 동안 논문 1편과 한 번의 학회 초록 발표는 최소한의 달성목표입니다.
            1. 내시경실 전 직원은 여러분의 명령을 받는 부하가 아니라 같이 일하는 동료입니다.
            1. 전공의 3년차에게 훈련을 위해 내시경 과정 일부를 넘겨 줄 경우, 반드시 진정이 잘된 환자일 경우에만 넘겨 주세요. 비진정 환자에서 그런 일이 벌어지면 책임을 묻겠습니다.
            1. 교육위원에서 인정하지 않은 외부 의사를 대상으로 전임의가 허락없이 내시경 교육을 하는 것은 금지입니다. 필요 시 반드시 교육 위원회의 허락을 받아야 합니다.
            1. 원칙적으로 고위험 치료내시경(EMR, ESD 등)은 반드시 상급자의 감독하에 시행되어야 합니다. 담당 교수님의 허락없이 고위험 시술을 전임의가 혼자 수행하는 것은 금지입니다.
            1. 수많은 교육 자료가 [AMC GI 상부 Simulator training](https://amcgic-simulator.streamlit.app/)와 [AMC GI 상부 Education Program](https://amcgic-training.streamlit.app/)에 있습니다. 잘 이용하세요.
            1. AMC GI 상부 Education Program은 출석 체크가 되므로, 끝낼 때는 반드시 왼쪽 아래 로그아웃 버튼을 눌러 종결하세요. 그냥 나가면 출석처리가 안됩니다.
        '''
        )

    with tab2:
        st.subheader("GI C 공통 교육 프로그램 설명")
        st.divider()
        st.subheader("Morning conference")
        with st.expander("Morning conference 내용을 보려면 여기를 눌러주세요"):
            st.markdown(
                '''
                1. 매주 화요일과 목요일 오전 8시부터 30분간 서관 3층 소강당에서 전임의가 준비한 주제 발표를 듣고 discussion 하는 morning conference가 있습니다.
                1. 전임의 한 명이 1년 중 한 번 혹은 두 번 발표하게 되는데 일정은 미리 정해져서 공지됩니다.
                1. 반드시 담당 교수를 정해서 발표주제를 상의해서 확정하고 발표 **2주 전**까지는 초벌 PPT를 보여드리고 발표 지도를 받습니다.
                1. 발표 슬라이드에는 자신의 이름과 지도교수의 이름을 반드시 기재 합니다.
                1. 전임의의 발표 시간은 15분 정도로하여 충분한 discussion이 이루어지도록 합니다.
                '''
            )
        st.subheader("Endoscopy conference")
        with st.expander("Endoscopy conference 내용을 보려면 여기를 눌러주세요"):
            st.markdown(
            '''
            1. 매주 월요일 12:15-13:00에 2세미나실에서 Endoscopy conference가 있습니다.
            1. 흥미로운 내시경 증례를 가지고 discussion 하는 conference 입니다. 병리과와 함께 보는 증례, 병리과 없이 소화기 자체로 진행하는 증례, 지혈술 증례들이 있으며, 연간 일정은 다음 [링크](https://docs.google.com/spreadsheets/d/1zKjcjnvndWJqOmqGhnxxJOBldxzk_Gbu4bhQitlXDUU/edit#gid=1535622479)에서 확인할 수 있습니다.
            1. 발표 담당 1년차는 3 증례 정도 준비하고, 병리과와 함께 보는 경우는 발표 전 주 목요일 11시까지 병리과에 증례를 알려 줍니다.
            1. 간단한 case 발표 형식으로 발표한 후 각 증례마다 discussion을 합니다.
            1. 발표 전임의가 출석한 전임의 중에서 호명하여 내시경 소견 description을 하도록 요청합니다.
            1. Conference 종료 후 발표 파일은 병리과 파일과 합쳐서 하나로 만듭니다. 이후 이 파일을 [NAS](http://192.168.112.131:5678/)에 저장합니다.
            1. NAS에 파일을 저장 후 "Endoscopy conference 내용요약" 파일에 내용을 정리합니다. 정리 후 담당 2년차 선생님(일정표에 있음)에게 확인을 받습니다.
            1. 공식적으로는 50% 이상 출석이 권장되지만 너무 중요한 훈련 프로그램이므로 가능한 한 참석하세요.
            '''
        )
        st.subheader("AI patient Hx. taking 훈련 프로그램")
        with st.expander("AI patient Hx. taking 훈련 프로그램 내용을 보려면 여기를 눌러주세요"):
            st.markdown(
                '''
                1. chatgpt를 이용한 전형적인 소화기 환자의 chief complaint에 대한 병력 청취 훈련 프로그램입니다.
                1. [AMC GI 상부 Education Program](https://amcgic-training.streamlit.app/)에 접속하는데, ID는 이메일 주소, PW, 이름, 지위를 입력하고 로그인 합니다.
                1. PW는 숫자와 알파벳 글자섞어서 8자이상의 PW를 이진혁 교수님에게 이메일로 보내어 허락받고 등록한 후 접속가능합니다.
                1. 왼편 sidebar에서 AI patient Hx. taking 훈련 페이지를 선택한 후 그 아래에서 증례를 선정하고 한글 타이핑으로 질문하면 AI 환자가 적절한 대답을 하는 형식으로 진행됩니다.
                1. 질문을 다 했으면 "궁금하신 점이 있으신가요"라고 AI 환자에게 질문하고 2 개의 질문을 받아 대답합니다.
                1. AI의 두 가지 질문에 답하면 약 20-30초 기다렸다가 선생님이 질문하지 않았던 항목을 찾아 줍니다. 단 완전치는 않으니 참고만 하세요.
                1. 왼편 sidebar에는 증례의 해설 파일을 다운로드 받는 기능이 있으니 훈련에 참고하세요.
                '''
            )
            
        st.subheader("EGD Lesion Dx. 훈련 프로그램")
        with st.expander("EGD Lesion Dx. 훈련 프로그램의 내용을 보려면 여기를 눌러주세요"):
            st.markdown(
                '''
                1. 소화기 전임의 1년차와 상부 2년차가 알아야 할 병변의 사진을 보고 진단을 훈련하는 프로그램입니다.(총 200여개의 증례 사진)
                1. [AMC GI 상부 Education Program](https://amcgic-training.streamlit.app/)에 접속하고, 등록했던 이메일 주소와 PW, 이름, 지위를 입력하면 됩니다.
                1. 로그인 하려면, 사전에 이진혁 교수님에게 이메일 주소와 숫자 알파벳 글자를 혼용한 8자리의 PW를 등록해야 합니다.
                1. 가장 먼저 왼쪽 sidebar에서 EGD Lesion Dx. 훈련 프로그램 페이지를 선택하고 아래에서 F1이나 F2를 선택합니다. 가능하면 F1, F2를 모두 공부하길 권합니다.
                1. 다음 EGD 사진을 선택하면 증례 사진과 질문이 보입니다.
                1. 질문에 대한 답을 충분히 생각해 보고, '진행' 버튼을 누르면 답과 이 증례를 통해 알아야 할 지식이 보입니다. 자신의 답과 비교해 보세요.
                1. 내 EGD 진단 능력의 60% 정도가 여기에 포함되어 있다고 평가합니다.
                1. 이 과정을 귀찮은 과제로 여기고, 그냥 한 번 읽어보고 넘어가는 사람은 아무것도 얻지 못합니다. 한 증례마다 관련된 자료와 연관된 증례를 찾아 공부하여 철저히 자기 것으로 만드는 노력이 있어야만 실력이 늘 수 있습니다.
                1. 매년 4월부터 다음 해 2월까지 매월 마지막 근무 일에 새로운 증례를 올립니다. 1년차용과 상부 2년차 용으로 나눠져 있으며, 매월 총 19-20 증례 정도가 새로 upload됩니다.
                '''
            ) 
            
        st.subheader("EGD 병변 진단에 있어 M-NBI의 중요성")
        with st.expander("EGD 병변 진단에 있어 M-NBI의 중요성의 내용을 보려면 여기를 눌러주세요"):
            st.markdown(
                '''
                1. EGD 병변의 진단에 있어 이제는 magnifying visual chromoscopy (우리 병원에서는 near focus NBI)의 역할은 필수 불가결해졌습니다.
                1. 아직 병변의 분류체계는 정리되지 않았지만 머지 않은 시기에 M-NBI 진단체계는 정리되어 모든 내시경 의사들이 의무적으로 기술해야 하는 필수 요건이 될 것입니다.
                1. M-NBI는 확대 비율이 높아 soft black hood를 써야지만 관찰할 수 있어, 배율은 떨어지나, 우리 병원 처럼 near focus NBI정도로 배율을 확대하여 보는 것이 일반적입니다.
                1. 내시경 전문가가 되고자 하는 여러분은 반드시 M-NBI를 공부하여 진료에 적용해 보는 습관을 들여야 합니다.
                1. 여기에 3개의 review 논문의 링크를 적습니다. 2023년말 현재까지 나와 있는 자료 중 가장 잘 되어 있는 리뷰논문이니 반드시 여러번 공부하여 자기 것으로 만드세요.
                1. [Normal gastrointestinal mucosa with narrow band image](https://www.elsevier.es/en-revista-gastroenterologia-hepatologia-14-articulo-endoscopic-microanatomy-normal-gastrointestinal-mucosa-S0210570518302772)
                1. [Narrow-Band Imaging in the Esophageal tumor](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8283285/)
                1. [NBI of normal and Corresponding Histopathology in the Stomach](https://www.gutnliver.org/journal/view.html?doi=10.5009/gnl19392)
                '''
            ) 


        st.subheader("")

    with tab3:
        st.markdown("추가사항이 있으면 채워주세요")

else:
    st.warning('Please log in to read more.')