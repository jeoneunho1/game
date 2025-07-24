import streamlit as st

# 앱 설정
st.set_page_config(page_title="클릭 챌린지 1000")

# 상태 초기화
if "click_count" not in st.session_state:
    st.session_state.click_count = 0
if "goal" not in st.session_state:
    st.session_state.goal = 1000

# 제목
st.title("🖱️ 클릭 챌린지: 1000번을 눌러라!")
st.markdown(f"현재 클릭 수: **{st.session_state.click_count} / {st.session_state.goal}**")

# 버튼
if st.button("클릭!"):
    st.session_state.click_count += 1

    # 999에서 리셋 + 놀리기
    if st.session_state.click_count == 999:
        st.warning("🤪 오 마이 갓! 999번에서 초기화되었습니다. 처음부터 다시 시작하세요!")
        st.session_state.click_count = 0

# 축하 메시지
if st.session_state.click_count >= st.session_state.goal:
    st.balloons()
    st.success("🎉 대단해요! 진짜 1000번 클릭에 성공했어요!")
    st.markdown("이제 손 좀 쉬어도 돼요 😅")

# 초기화 버튼
if st.button("다시 시작"):
    st.session_state.click_count = 0
    st.experimental_rerun()
