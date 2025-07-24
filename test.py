import streamlit as st
import random
import time

# 설정
GRID_SIZE = 3
TIME_LIMIT = 10  # 게임 시간 (초)

# 초기화
if "score" not in st.session_state:
    st.session_state.score = 0

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "target_index" not in st.session_state:
    st.session_state.target_index = random.randint(0, GRID_SIZE**2 - 1)

# 타이머 시작
def start_game():
    st.session_state.score = 0
    st.session_state.start_time = time.time()
    st.session_state.target_index = random.randint(0, GRID_SIZE**2 - 1)

# 게임 중인지 판별
def is_playing():
    return st.session_state.start_time is not None and (time.time() - st.session_state.start_time < TIME_LIMIT)

# UI
st.title("🐹 두더지 잡기 게임")
st.caption("제한 시간 내에 최대한 많은 두더지를 잡아보세요!")

if not is_playing():
    if st.button("▶️ 게임 시작"):
        start_game()

# 게임 중이면 그리드 표시
if is_playing():
    remaining = TIME_LIMIT - int(time.time() - st.session_state.start_time)
    st.markdown(f"⏱️ 남은 시간: **{remaining}초**")
    st.markdown(f"📊 현재 점수: **{st.session_state.score}**")

    # 버튼 그리드
    cols = st.columns(GRID_SIZE)
    for i in range(GRID_SIZE):
        row = st.columns(GRID_SIZE)
        for j in range(GRID_SIZE):
            idx = i * GRID_SIZE + j
            if idx == st.session_state.target_index:
                if row[j].button("🐹", key=f"mole_{idx}_{random.random()}"):
                    st.session_state.score += 1
                    st.session_state.target_index = random.randint(0, GRID_SIZE**2 - 1)
            else:
                row[j].button("⬜", key=f"empty_{idx}_{random.random()}")

else:
    if st.session_state.start_time is not None:
        st.success(f"⏰ 게임 종료! 최종 점수: **{st.session_state.score}점**")
        st.session_state.start_time = None  # 재시작 가능하게 초기화
