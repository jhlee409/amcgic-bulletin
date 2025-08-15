import streamlit as st

# Create pages
login_page = st.Page("pages/Login.py", title="로그인 페이지", icon=":material/chat:")
page_1 = st.Page("pages/0 Home.py", title="Home", icon=":material/analytics:")
page_2 = st.Page("pages/1 교육 프로그램 구성.py", title="교육 프로그램 구성", icon=":material/domain:")
page_3 = st.Page("pages/2 내과 전공의 3년차 프로퍼.py", title="내과 전공의 3년차 프로퍼", icon=":material/domain:")
page_4 = st.Page("pages/3 소화기 전임의 공통 프로그램.py", title="소화기 전임의 공통 프로그램", icon=":material/domain:")
page_5 = st.Page("pages/4 소화기 전임의 1년차용.py", title="소화기 전임의 1년차용", icon=":material/domain:")
page_6 = st.Page("pages/5 소화기 전임의 상부 2년차용.py", title="소화기 전임의 상부 2년차용", icon=":material/domain:")

# Set up navigation with sections
pg = st.navigation(
    {
        "로그인 페이지": [login_page],
        "구성": [page_1, page_2, page_3, page_4, page_5, page_6],
    },
)

# Set default page configuration
st.set_page_config(
    page_title="AMC GIC bulletin",
    page_icon="🤖",
)

# Run the selected page
pg.run() 