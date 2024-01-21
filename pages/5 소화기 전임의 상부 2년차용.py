import streamlit as st
import os

st.set_page_config(page_title="F2", layout="wide")

if st.session_state.get('logged_in', False):  # 로그인 상태 확인

    st.header("AMC 소화기 내과 상부 F2 전용 교육 과정 설명")
    st.markdown("이 페이지는 서울 아산병원 **GI 상부 전임의 2년차**를 대상으로하는 EGD 교육 과정의 설명입니다.")
    st.markdown("이 페이지는 2023년 말에 작성된 문서로 **2024년** 근무 소화기내과 상부 F2를 위한 설명서입니다.")
    st.divider()

    tab1, tab2, tab3 = st.tabs(["당부사항", "각 프로그램 설명", "각종표"])

    with tab1:
        st.subheader("상부 전임의 2년차에게 드리는 당부")
        st.markdown(
            '''
            1. 내시경 검사 건수가 많습니다. 검사가 정시에 마칠 수 있도록 여러분의 주도적인 참여가 절실합니다.
            1. 2년차 하는 동안 원저 1편과 한 번의 외국학회 초록 발표는 최소한의 달성목표입니다.
            1. 전공의 3년차와 전임의 1년차의 내시경 교육에 여러분의 참여가 꼭 필요합니다.
            1. 가만히 있으면 아무도 안챙겨 줍니다. 시간을 짜내서라도 치료 내시경 세션에 참여하세요.
            1. [Sim Class](https://edu.amc.seoul.kr/)에 올려져 있는 교육 자료들은 1년차 뿐 아니라 여러분에게도 매우 도움이 되는 내용들이니 꼭 보기 바랍니다.
            1. AI 환자 병력 청취 훈련 프로그램은 매우 효과적인 문진 훈련 프로그램입니다. 10개의 증례가 마련되어 있으므로 완전히 자기 것이 될 때 까지 반복 훈련하세요.
            1. AI를 이용한 EGD 사진 Dx. 훈련 프로그램이 곧 제공될 예정입니다. 난이도를 높여가며 매달 10개씩의 증례를 제공할 예정이니 반드시 공부하기 바랍니다.
            1. 내시경실 전 직원은 여러분의 명령을 받는 부하가 아니라 같이 일하는 동료입니다.
            1. 교육위원회에 허락을 받지 않은 사람을 병원내에서 무단으로 교육하는 것은 금지입니다.
        '''
        )
    with tab2:
        st.subheader("GI C 전임의 2년차 교육 프로그램 설명")
        st.divider()
        st.subheader("Stomach conference")
        with st.expander("Stomach conference 내용을 보려면 여기를 눌러주세요"):
            st.markdown(
                '''
                1. 매주 화요일 저녁 6시 동관 10층 외과 희의실에서는 소화기 내과, 위장관 외과, 종양내과, 병리과 선생님들이 모여 stomach conference를 합니다.
                1. 학회나 진료 중에 배울 수 없는 타 과의 유용한 전문 지식을 얻을 수 있는 source 이니 꼭 참가하도록 하세요. 저녁거리도 챙겨 줍니다.
                1. 본인이 하는 study가 있을 경우, 여기서 발표하면 자신의 연구를 한 번 다듬는 기회가 되므로 적극 활용하세요.
                '''
            )
        st.subheader("Side Scope Insertion Training (SSIT)")
        with st.expander("SSIT 내용을 보려면 여기를 눌러주세요"):
            st.markdown(
                '''
                1. 이 시뮬레이터 훈련은 초음파 내시경을 할 때 두껴운 side view scope로 insertion을 하다가 식도 천공이 발생한 전례를 계기로 개발된 프로그램입니다.
                1. 이 프로그램을 통과하기 전에는 전임의가 직접 EUS scope를 UES로 삽입하는 것은 금지되어 있습니다. 물론 다른 관찰과정은 이 과정 통과 전에 해도 됩니다
                1. ERCP scope를 blind 방식으로, simulator UES에 삽입하는데, 경고음이 안나도록 통과하는 것이 목표입니다. 두 번 시도해서 한 번 성공하면 통과입니다.
                1. 일정표 대로 6월 후반부에 시행하게 됩니다. 하는 방법 시범보고 각자 연습해서 시험 날 스텝의 참관하에 시험을 보게되므로 열심히 훈련하기 바랍니다.
                '''
            )
        st.subheader("ESD Simulator Training")
        with st.expander("ESD Simulator Training 내용을 보려면 여기를 눌러주세요"):
            st.markdown(
                '''
                1. 일년에 두 번 정도 일본 제품인 EndoGel을 사용한 ESD 훈련 프로그램입니다.
                1. 일정에 대해서 이후 공지가 있으니 참고하세요.
                '''
            )
        st.subheader("바람직한 EUS, ESD training 요령")
        with st.expander("바람직한 EUS, ESD training 요령의 내용을 보려면 여기를 눌러주세요"):
            st.markdown(
                '''
                1. 근무 전반부는 내시경 로딩이 많아 ESD, EUS 세션 참여가 어려울 겁니다. 조금 여유가 나면 EUS, ESD 세션에 들어가서 교수님의 지시에 따르고 출석 사인 받으세요.
                1. 시간이 지나서 여러분이 procedure 진행 과정에 익숙해졌다고 판단되면, 교수님이 간단하고 위험하지 않은 과정부터 해보도록 scope를 넘겨주게 됩니다. 난이도가 낮은 과정에 익숙해지면 조금씩 난이도가 높아지게 됩니다.
                1. 최종 목표는 최소한 한 증례는 전 과정을 혼자 해보는 것입니다.
                1. EUS 의 경우 필수 case 리스트에 있는 진단이 내려진 환자를 내시경실의 도움을 받아 찾아내서 사진과 report를 교과서와 대조해 가면서 공부해야 합니다. 동료들과 같이 작업하세요.
                1. 다시 한 번 강조하지만 SSIT 통과 전에는 EUS scope를 환자에게 직접 삽입하는 것은 금지입니다. 교수님이 하라고 해도 SSIT 통과 전이면 사정을 말씀드리고 하지 마세요.
                1. EndoGel 을 사용한 ESD simulator 훈련은 매우 효과적인 사전교육입니다. 반드시 참석하도록 노력하세요.
                1. 교수들의 생각으로는 EUS와 ESD 모두 20증례 정도를 참가해야, 어느 정도 수준에 도달한다고 봅니다.힘들겠지만 20회 이상은 참여하기 바라고, EUS 증례를 사진을 통해 공부하는 것도 매우 중요하니 혼자 어려우면 다른 상부 2년차와 공동으로 공부를 진행하세요.
                '''
            )
        st.subheader("")
        st.subheader("")

    with tab3:
        st.header("각종 출석표 및 수련항목 점검표")
        with st.expander("사용방법을 보려면 여기를 눌러주세요"):
            st.markdown(
                '''
                1. 근무 시작 후 다음의 표들을 다운 받아 인쇄하여 수첩에 붙입니다.
                1. ESD 경우, 시간이 될 때 ESD 참관 들어가서 출석표에 스텝의 사인을 받습니다. 20 세션이 권장 참관 세션 수 입니다.
                1. EUS 경우, ESD와 마찬가지로 최소 20 세션을 들어가서 출석표에 스텝사인을 받고, 필수 case에 해당하는 증례의 사진을 내시경실의 자료를 검색해서 확보하여 공부 합니다. 자신이 직접 본 증례와 찾은 증례의 병록번호를 표에 기록합니다. 필수 증례는 반드시 채우도록 합니다.
                1. 수련항목 점검 사항은 연간일정에 정해진 시기에 이진혁 교수님에게 점검을 받게 됩니다.
            '''
            )
        st.write("")

        col1, col2, col3 = st.columns([1,1,1])

        with col1:
            st.image("./images/ESD_attendance.png")

        with col2:
            st.image("./images/EUS_attendance.png")
            st.image("./images/eus_case_list2.png")
            st.image("./images/eus_case_list1.png")

        with col3:
            st.image("./images/check_list.png")

        file_path = './pages/data/gic_f2_tables.xlsx'

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