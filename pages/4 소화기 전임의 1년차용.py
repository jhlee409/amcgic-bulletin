import streamlit as st
import os

st.set_page_config(page_title="F1", layout="wide")

if st.session_state.get('logged_in', False):  # 로그인 상태 확인

    st.header("AMC 소화기 내과 F1 전용 교육 과정 설명")
    st.divider()
    st.markdown("이 페이지는 서울 아산병원 **소화기내과 전임의 1년차**를 대상으로하는 EGD 교육 과정의 설명입니다.")

    # 로그 아웃 버튼
    if "logged_in" in st.session_state and st.session_state['logged_in']:

        if st.sidebar.button("Logout"):
            st.session_state['logged_in'] = False
            st.success("로그아웃 되었습니다.")
            # 필요시 추가적인 세션 상태 초기화 코드
            # 예: del st.session_state['logged_in'

    st.divider()

    tab1, tab2, tab3 = st.tabs(["당부사항", "각 프로그램 설명", "temp"])

    with tab1:
        st.subheader("소화기 전임의 1년차에게 드리는 당부")
        st.markdown(
            '''
            1. 근무 초기에는 다른 병원에서 수련받다가 온 선생님들이 여기 시스템에 적응하는데 힘들어하는 시기 입니다. 잘 도와주기 바랍니다.
            1. 출신을 불문하고 EGD 기초 교육을 이수하지 못한 선생님들은 3월 중에 반드시 교육과정을 이수하기 바랍니다. 소화기 과내 방침입니다.
            1. 진단 EGD를 빨리 배우고 싶은 마음은 이해됩니다. 그러나 ER, 강릉, GI B 등의 일정도 있기 때문에 일정 정하는데 갈등이 있을 수 있겠습니다. 과내 지침은 초반에는 주로 원내 출신이 앞의 일정을 맡고 그 다음 달에는 앞의 일정은 빠진다는 것입니다. 모쪼록 원내 출신 선생님들의 자발적인 협조를 부탁합니다.
            1. [AMC GI 상부 Education Program](https://amcgic-training.streamlit.app/)에 올려져 있는 교육 자료들은 매우 충실하게 잘 만든 교육자료 입니다. 시기별로 자기에게 맞는 내용을 꼭 반복해서 학습하세요.
            1. AMC GI 상부 Education Program은 출석 체크가 되므로, 끝낼 때는 반드시 왼쪽 아래 로그아웃 버튼을 눌러 종결하세요. 그냥 나가면 출석처리가 안됩니다.
            1. AI patient Hx. taking 훈련 프로그램은 매우 강력한 프로그램입니다. 완전히 자기 것이 될 정도로 훈련하면 외래 진료를 능숙하게 할 수 있게 될겁니다.
            1. EGD Lesion Dx. 훈련 프로그램은 매우 강력한 프로그램입니다. 여러분이 알아야 할 거의 모든 증례를 다룹니다. 완전히 자기 것이 될 정도로 훈련하면 실력향상에 큰 도움이 되니 열심히 하세요.
        '''
        )
    with tab2:
        st.subheader("GI 1년차 전용 교육 프로그램 설명")
        st.divider()
        
        st.subheader("쪽지 시험")
        with st.expander("쪽지 시험 내용을 보려면 여기를 눌러주세요"):
            st.markdown(
                '''
                1. 소화기 전임의 1년차 초반에 기본적으로 알고 있어야 할 내시경 관련 기본지식에 대한 쪽지 시험을 3월 전반부에 칩니다.
                1. 시험 범위는 다음 내용이므로 다운 받아서 이에 관련해서 열심히 공부하고 암기하기 바랍니다.
                1. 개별 성적은 개인에게만 알려 주고 전체 회람은 익명처리됩니다.
                '''
            )
        file_path = './pages/data/pop_quiz.xlsx'
        if os.path.isfile(file_path):
            btn = st.download_button(
                label="다운로드 1",
                data=open(file_path, "rb").read(),
                key="contents_download_button_1",
                file_name=os.path.basename(file_path),
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("파일을 찾을 수 없습니다. 'pop_quiz.xlsx' 파일이 현재 폴더에 존재해야 합니다.")
        
        st.subheader("땡시험")
        with st.expander("땡시험 내용을 보려면 여기를 눌러주세요"):
            st.markdown(
                '''
                1. 3월 후반부와 5월 후반부 EGD 병변 사진을 보고 description과 impression 을 적어내는 땡시험을 칩니다.
                1. 날짜와 장소는 추후 공지합니다.
                1. 진행 방식은 준비된 병변 사진을 PPT로 보여주면 description과 impression 을 적어내는 방식으로 나중에 결과는 개인에게 통보됩니다.
                '''
            )
        st.subheader("Lt. Hand Trainer")
        with st.expander("Lt. Hand Trainer 내용을 보려면 여기를 눌러주세요"):
            st.markdown(
                '''
                1. 치료 내시경을 하려면 전진을 제외한 모든 scope의 조작을 왼손으로만 할 수 있어야, 치료 도구를 오른손으로 쓸 수 있습니다.
                1. 이 프로그램은 벽에 붙어 있는 단추를 왼손 조작만으로 정해진 시간에 떨어 뜨려야 합격하도록 고안된 시뮬레이터를 사용합니다.
                1. https://amcgic-simulator.streamlit.app/ 의 LHT 페이지에서 LHT orientation 동영상을 시청하고, 훈련하면서 전문가 시범 동영상을 보면서 미러링을 하세요.
                1. 기준에 통과한 동영상을 녹화해서 수행 동영상 업로드에 올리면 훈련이 종결됩니다.
                '''
            )
        st.subheader("EGD variation 강의")
        with st.expander("EGD variation 강의 내용을 보려면 여기를 눌러주세요"):
            st.markdown(
                '''
                1. 기본 시뮬레이터 내시경 교육을 받고 나서 1-2 달이 지나면 조금은 내시경 조작에 익숙해지지만, 환자의 다양한 상황에 대해 대처를 못해 애를 먹게됩니다.
                1. 이 강의 동영상은 예를 들면 'pyloric ring을 통과하는데 잘 안된다'와 같은 다양하고 흔한 상황에서 전문가가 어떻게 하는지를 나래이션으로 설명하는 동영상클립들을 모아 놓는 프로그램입니다.
                1. 강의 동영상은 [AMC GI 상부 Education Program](https://amcgic-training.streamlit.app/)에 올려져 있고, 보통은 5월이나 6월 정도면 절실하게 필요한 내용이 들어 있습니다.
                1. 1년차 첫 달에는 더 기본적인 조작이 힘들어 이 동영상을 봐도 먼나라 얘기이고, 1년차 후반부에는 볼 필요가 없을 정도로 이미 숙련되어 있을 것이므로 꼭 필요한 때 찾아서 보기 바랍니다.
                1. 특히 각 상황에 1번 동영상은 자세한 설명이 있는 동영상입니다. 이 1번 동영상은 모두 시청해야 합니다.
                '''
            )
        st.subheader("Hemostasis simulator training")
        with st.expander("Hemostasis simulator training 내용을 보려면 여기를 눌러주세요"):
            st.markdown(
                '''
                1. AMC GI 에서 시행되는 지혈술 시뮬레이터 훈련 종목은, hemoclip, injection, APC, Nexpower spray, EVL  이렇게 5가지 입니다.
                1. 7월 전반부에 주로 토요일 오후에 교육이 있습니다. 5개 방에서 모든 지혈술을 그 날 훈련하게 됩니다. 확정 날짜는 추후 통보됩니다.
                1. 훈련 전 [AMC GI 상부 Education Program](https://amcgic-training.streamlit.app/)에 올려져 있는 5가지 지혈술에 대해 설명한 orientation 동영상을 모두 시청한 후 실습에 임해주세요. 실습날은 따로 자세한 설명을 하지 않습니다.
                1. 5개 그룹으로 나누어서 한 방에 한 그룹이 들어가 훈련하고 로테이션 하는 체제로 진행합니다.
                '''
            )
        st.subheader("PEG simulator training")
        with st.expander("PEG simulator training 내용을 보려면 여기를 눌러주세요"):
            st.markdown(
                '''
                1. 9월 초에 PEG simulator를 가지고 직접 해보는 훈련이 있습니다. 대게는 토요일 오후에 시행하게 됩니다. 확정 날짜는 추후 통보됩니다.
                1. 훈련 전 [AMC GI 상부 Education Program](https://amcgic-training.streamlit.app/)에 올려져 있는 PEG simulator강의 동영상을 충분히 보고 훈련에 임하기 바랍니다.
                1. 세 조로 나뉘어 각 방에서 시범을 보고 직접 해 보는 방식으로 진행됩니다.
                '''
            )
        st.subheader("")
        st.subheader("")

    with tab3:
        st.subheader("temp")

else:
    st.warning('Please log in to read more.')