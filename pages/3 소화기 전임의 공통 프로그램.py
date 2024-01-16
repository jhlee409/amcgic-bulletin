import streamlit as st
import os

st.set_page_config(page_title="Fellow")

if st.session_state.get('logged_in', False):  # 로그인 상태 확인

    st.header("AMC 소화기 내과 전임의 공통 교육 과정 설명")
    st.markdown("이 페이지는 AMC **GI 전임의 1년차 및 상부 전임의 2년차**를 대상으로하는 EGD 교육 과정의 설명입니다.")
    st.markdown("이 페이지는 2023년 말에 작성된 문서로 **2024년** 근무 소화기내과 전임의를 위한 설명서입니다.")
    st.divider()

    tab1, tab2, tab3 = st.tabs(["공통 당부사항", "공통 프로그램 설명", "temp"])

    with tab1:
        st.subheader("소화기 전임의에게 드리는 당부")
        st.markdown(
            '''
            1. 내시경 검사 건수가 많습니다. 검사가 정시에 마칠 수 있도록 여러분의 도움이 절실합니다.
            1. 1년 수련기간 동안 논문 1편과 한 번의 학회 초록 발표는 최소한의 달성목표입니다.
            1. 내시경실 전 직원은 여러분의 명령을 받는 부하가 아니라 같이 일하는 동료입니다.
            1. 교육위원회에 허락을 받지 않은 사람을 병원내에서 무단으로 교육하는 것은 금지입니다.
            1. 전공의 3년차에게 훈련을 위해 내시경 과정 일부를 넘겨 줄 경우, 반드시 진정이 잘된 환자일 경우에만 넘겨 주세요. 비진정 환자에서 그런 일이 벌어지면 책임을 묻겠습니다.
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
            1. 공식적으로는 50% 이상 출석이 권장되지만 너무 중요한 훈련 프로그램이므로 꼭 참석하세요.
            '''
        )
        st.subheader("AI 소화기 환자 병력 청취 훈련 프로그램")
        with st.expander("AI 소화기 환자 병력 청취 훈련 프로그램 내용을 보려면 여기를 눌러주세요"):
            st.markdown(
                '''
                1. chatgpt를 이용한 전형적인 소화기 환자의 chief complaint에 대한 병력 청취 훈련 프로그램입니다.
                1. [AI patient Hx taking program](https://amcgi-22questions.streamlit.app/)에 접속하고, ID는 amcgi, PW는 3180을 입력하면 사용할 수 있습니다.
                1. 왼편 sidebar에서 증례를 선정하고 한글 타이핑으로 질문하면 AI 환자가 적절한 대답을 하는 형식으로 진행됩니다.
                1. 질문을 다 했으면 "궁금하신 점이 있으신가요"라고 AI 환자에게 질문하고 2 개의 질문을 받아 대답합니다.
                1. AI의 두 가지 질문에 답하면 약 50초 기다렸다가 선생님이 질문하지 않았던 항목을 찾아 줍니다. 단 완전치는 않습니다.
                1. 왼편 sidebar에는 증례의 해설 파일을 다운로드 받는 기능이 있으니 훈련에 참고하세요.
                '''
            )
        st.subheader("")
        st.subheader("")

    with tab3:
        st.markdown("추가사항이 있으면 채워주세요")

else:
    st.warning('Please log in to read more.')