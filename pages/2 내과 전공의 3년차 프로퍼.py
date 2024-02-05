import streamlit as st
import os

st.set_page_config(page_title="R3", layout="wide")

if st.session_state.get('logged_in', False):  # 로그인 상태 확인

    st.header("AMC 내과 R3 소화기 proper용 교육 과정 설명")
    st.divider()
    st.markdown("이 페이지는 AMC **내과 전공의 3년차 소화기 proper**를 대상으로하는 진단 EGD 교육 과정의 설명입니다.")

    # 로그 아웃 버튼
    if "logged_in" in st.session_state and st.session_state['logged_in']:
        st.sidebar.divider()
        if st.sidebar.button("Logout"):
            st.session_state['logged_in'] = False
            st.success("로그아웃 되었습니다.")
            # 필요시 추가적인 세션 상태 초기화 코드
            # 예: del st.session_state['logged_in'

    tab1, tab2, tab3 = st.tabs(["당부사항", "각 프로그램 설명", "temp"])

    with tab1:
        st.subheader("내과 3년차 소화기 프로퍼에게 드리는 당부")
        st.markdown(
            '''
            1. 여러분은 앞으로 1년동안 체계적으로 구축된 진단 EGD 교육 프로그램을 이수하게 됩니다.
            1. 4월 orientation과 memory test 를 시작으로 앞에 첨부된 연간 일정표에 따라 훈련이 진행됩니다. OT 때 교육 수첩을 받아 교육과정 내내 사용하게 됩니다.
            1. 교육 과정은 MT(memory test), SHT(scope handling test), EMT(EGD method training), participation, performance test로 이 순서에 따라 진행됩니다.
            1. 훈련 프로그램 OT는 1번을 기본으로 하고, 필요에 따라 2번 반복하는 것이 원칙이니, 미리 알려주는 일정에 참여할 수 있도록 스케쥴을 조정하기 바랍니다.
            1. 목표 달성 여부는 시험을 통해 확인하는데, 시험에는 교수님이 참관하시므로 열심히 훈련하기 바랍니다.
            1. 의무사항은 아니지만, AI 환자 병력 청취 훈련 프로그램은 매우 효과적인 문진 훈련 프로그램입니다. 10개의 증례가 마련되어 있으므로 완전히 자기 것이 될 때 까지 반복 훈련하세요.
            1. 시뮬레이션 센터의 여러 선생님들이 소화기의 요청에 의해 프로그램을 운영하시고 계십니다. 예의와 존중을 잊지 말기 바랍니다.               
        '''
        )
    with tab2:
        st.subheader("내과 3년차 proper 진단 EGD 교육 프로그램 설명")
        st.markdown("상세한 내용은 [Sim Class](https://edu.amc.seoul.kr/)에 있는 소개 동영상을 시청하기 바랍니다.")
        st.divider()
        st.subheader("Memory Test")
        with st.expander("Memory Test 내용을 보려면 여기를 눌러주세요"):
            st.markdown(
                '''
                1. 이 과정은 내시경 수행 순서를 말로 외움으로써 실제 스코프를 잡고 훈련할 때 주의력이 분산되지 않도록 하는 목적으로 만들어진 프로그램입니다.
                1. 첨부된 mt.doc 파일을 다운받아 모두 암기한 후 정해진 날에 교수님 앞에서 암기한 것을 구술하는 방식으로 시험을 보게 됩니다.
                '''
            )
        file_path = './pages/data/mt.doc'
        if os.path.isfile(file_path):
            btn = st.download_button(
                label="다운로드 1",
                data=open(file_path, "rb").read(),
                key="contents_download_button_1",
                file_name=os.path.basename(file_path),
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        else:
            st.warning("파일을 찾을 수 없습니다. 'contents.xlsx' 파일이 현재 폴더에 존재해야 합니다.")
            
        st.subheader("Scope Handling Test")
        with st.expander("Scope Handling Test 내용을 보려면 여기를 눌러주세요"):
            st.markdown(
                '''
                1. 이 프로그램은 간략화된 시뮬레이터를 대상으로 훈련하여 내시경 조작 technique을 집중적으로 익히도록 고안된 프로그램입니다.
                1. 벽에 자석으로 붙어있는 7 개의 단추를 2분 30초 안에, 도중에 떨어 뜨리지 않고, 정해진 용기에 운반해 넣으면 합격입니다.
                1. 이 때부터 스코프를 직접 다루게 되는데 무리한 동작으로 스코프가 고장나지 않게 조심하는 습관을 가지기 바랍니다.
                1. 적어도 이 과정은 이수해야 실제 내시경 검사에서 스코프를 잡을 수 있습니다. 환자 안전을 위해 그 전에는 참관만 하세요.
                '''
            )
        st.subheader("EGD Method Trainig")
        with st.expander("EGD Method Trainig 내용을 보려면 여기를 눌러주세요"):
            st.markdown(
                '''
                1. 이 과정은 인체와 똑같은 3차원 구조와 경도를 가진 실리콘 모형을 대상으로 EGD를 체계적으로 수행하는 훈련을 하는 과정입니다.
                1. 여러분이 암기한 검사 순서를 이 시뮬레이터를 대상으로 해 보면서 숙련되도록 하는데, 중요한 점은 천천히 같은 속도록 사진도 찍어가며 정해진 순서를 지키는 것입니다.
                1. 전체 검사 시간은 5분에서 5분30초 사이로, 사진은 62장에서 66장 사이의 사진을 찍어야 합니다.
                1. 나중에 교수님이 보는 앞에서 시험을 보게되니 열심히 하기 바랍니다.
                '''
            )
        st.subheader("Participation")
        with st.expander("Participation 내용을 보려면 여기를 눌러주세요"):
            st.markdown(
                '''
                1. 이 과정은 시뮬레이터를 대상을 익힌 techique를 실제 환자에서 수행하면서 EGD 실전 수행 능력을 익히는 과정입니다.
                1. 교육 수첩 안에 있는 EGD 출석표에 supervisor의 출석 사인을 받아야 하는데 총 20회 출석이 필수 참관 수입니다.
                1. 처음에는 난이도가 낮고 환자에 대한 위해도가 낮은 과정부터 차츰 난이도를 높여 가면 나중에서 혼자서 insertion을 수행하게 됩니다.
                1. 반드시 진정 내시경이 잘 된 환자를 대상으로 훈련해야 합니다. 비진정 환자를 대상으로 하면 시킨 사람과 한 사람 모두 책임을 묻겠습니다.
                1. 한 방에 여러 피교육자가 들어온 경우는 반드시 한 사람만 내시경을 잡을 수 있습니다.
                '''
            )      
        st.subheader("Performance Test")
        with st.expander("Performance Test 내용을 보려면 여기를 눌러주세요"):
            st.markdown(
                '''
                1. 모든 과정을 이수하고 나면 이제는 실제 환자에게 진단 EGD를 수행하는 과정이 남았습니다.
                1. 2월 중에 담당 교수님을 배정 받아 그 교수님 내시경 할 때 들어가서 정상 진정 내시경 환자 중에서 교수님이 지정한 환자에 대해 처음부터 끝까지 검사를 수행합니다.
                1. 2명의 환자에 대해 검사를 수행하는데 문제가 없었고 목넘김은 한 환자에서 성공하면 전체적으로 통과입니다.
                '''
            )
        st.subheader("인증서 수여")
        with st.expander("인증서 수여 내용을 보려면 여기를 눌러주세요"):
            st.markdown(
                '''
                1. 모들 과정을 다 이수하고 나면 2월에 정훈용 교수님께서 직접 인증서에 사인을 해 주십니다.
                1. 인증서의 의미는 정상 EGD를 단독으로 수행할 수 있는 수준의 70%에 달했다는 것을 AMC 소화기가 인증하는 것입니다.
                '''
            )
        st.subheader("")
        st.subheader("")

    with tab3:
        st.subheader("필요한 사항을 기록해 주세요")
    
else:
    st.warning('Please log in to read more.')