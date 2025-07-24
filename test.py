import streamlit as st

# 앱 설정
st.set_page_config(page_title="1만 번 클릭 챌린지")

# 세션 상태 초기화
if "click_count" not in st.session_state:
    st.session_state.click_count = 0
if "goal" not in st.session_state:
    st.session_state.goal = 10000

# 제목 및 카운트 표시
st.title("🖱️ 10,000번 클릭 챌린지")
st.markdown(f"현재 클릭 수: **{st.session_state.click_count} / {st.session_state.goal}**")

# 버튼 클릭
if st.button("클릭!"):
    st.session_state.click_count += 1

# 결과 출력
if st.session_state.click_count >= st.session_state.goal:
    st.balloons()
    st.success("🎉 축하합니다! 10,000번 클릭에 성공했어요!")

# 초기화 버튼
if st.button("다시 시작"):
    st.session_state.click_count = 0
    st.experimental_rerun()
