import streamlit as st

# 경기장 크기 설정
FIELD_WIDTH = 7
FIELD_HEIGHT = 5
GOAL_X = FIELD_WIDTH - 1
GOAL_Y = FIELD_HEIGHT // 2

# 초기화
if "ball_pos" not in st.session_state:
    st.session_state.ball_pos = [0, FIELD_HEIGHT // 2]

if "score" not in st.session_state:
    st.session_state.score = 0

st.title("⚽ Streamlit 축구 조작 게임")
st.caption("방향 버튼을 눌러 공을 이동시켜 골을 넣어보세요!")

# 경기장 그리기 함수
def draw_field():
    field = ""
    for y in range(FIELD_HEIGHT):
        row = ""
        for x in range(FIELD_WIDTH):
            if [x, y] == st.session_state.ball_pos:
                row += "🟡"  # 공
            elif x == GOAL_X and y == GOAL_Y:
                row += "🥅"  # 골대
            else:
                row += "🟩"
        field += row + "\n"
    return field

st.markdown("#### 경기장")
st.text(draw_field())

# 방향 버튼 UI
col1, col2, col3 = st.columns(3)
with col2:
    if st.button("⬆️ 위"):
        if st.session_state.ball_pos[1] > 0:
            st.session_state.ball_pos[1] -= 1

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⬅️ 왼쪽"):
        if st.session_state.ball_pos[0] > 0:
            st.session_state.ball_pos[0] -= 1
with col3:
    if st.button("➡️ 오른쪽"):
        if st.session_state.ball_pos[0] < FIELD_WIDTH - 1:
            st.session_state.ball_pos[0] += 1

col1, col2, col3 = st.columns(3)
with col2:
    if st.button("⬇️ 아래"):
        if st.session_state.ball_pos[1] < FIELD_HEIGHT - 1:
            st.session_state.ball_pos[1] += 1

# 골 판정
if st.session_state.ball_pos == [GOAL_X, GOAL_Y]:
    st.success("🎉 골인! 점수 +1")
    st.session_state.score += 1
    st.session_state.ball_pos = [0, FIELD_HEIGHT // 2]

st.markdown(f"**현재 점수: {st.session_state.score}골**")

# 리셋 버튼
if st.button("🔄 리셋"):
    st.session_state.ball_pos = [0, FIELD_HEIGHT // 2]
    st.session_state.score = 0
