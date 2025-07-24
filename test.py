import streamlit as st
import random
import time

st.set_page_config(page_title="🏇 경마 베팅 게임", layout="centered")

# 초기 세션 상태
if "balance" not in st.session_state:
    st.session_state.balance = 200000

if "conditions" not in st.session_state:
    st.session_state.conditions = {}

if "history" not in st.session_state:
    st.session_state.history = []

horses = [f"말 {i+1}" for i in range(12)]
finish_line = 100

# 말 컨디션 생성 함수
def generate_conditions():
    return {horse: random.choice(["매우 좋음", "좋음", "보통", "나쁨", "매우 나쁨"]) for horse in horses}

condition_speed_modifier = {
    "매우 좋음": (4, 7),
    "좋음": (3, 6),
    "보통": (2, 5),
    "나쁨": (1, 4),
    "매우 나쁨": (1, 3)
}

condition_display = {
    "매우 좋음": "🟢 매우 좋음",
    "좋음": "🟢 좋음",
    "보통": "🟡 보통",
    "나쁨": "🔴 나쁨",
    "매우 나쁨": "🔴 매우 나쁨"
}

st.title("🏇 전략 경마 게임")
st.markdown(f"**💰 잔액: {st.session_state.balance:,}원**")

# 말 컨디션 표시
if not st.session_state.conditions:
    st.session_state.conditions = generate_conditions()

with st.expander("🐴 이번 경기 말 컨디션 보기"):
    for horse, cond in st.session_state.conditions.items():
        st.markdown(f"**{horse}**: {condition_display[cond]}")

# 게임 모드
mode = st.radio("🎮 게임 모드 선택", ["1등만 맞추기 (Easy)", "1~3등 순서 맞추기 (Hard)"])

# 선택 입력
if mode == "1등만 맞추기 (Easy)":
    pick = st.selectbox("🥇 1등 예상", horses)
else:
    st.subheader("🎯 베팅할 말 선택 (1, 2, 3등 순서대로)")
    col1, col2, col3 = st.columns(3)
    with col1:
        pick1 = st.selectbox("🥇 1등 예상", horses, key="pick1")
    with col2:
        pick2 = st.selectbox("🥈 2등 예상", [h for h in horses if h != pick1], key="pick2")
    with col3:
        pick3 = st.selectbox("🥉 3등 예상", [h for h in horses if h not in [pick1, pick2]], key="pick3")

bet_amount = st.number_input("💸 베팅 금액 (만원 단위)", min_value=10000, max_value=st.session_state.balance, step=10000)

start_race = st.button("🚦 경주 시작!")

# 경주 실행
if start_race:
    positions = {horse: 0 for horse in horses}
    rankings = []
    race_box = st.empty()

    st.session_state.conditions = generate_conditions()
    if mode == "1등만 맞추기 (Easy)":
        st.success(f"{pick}에 {bet_amount:,}원 베팅 완료!")
    else:
        st.success(f"{pick1} / {pick2} / {pick3} 에 {bet_amount:,}원 베팅 완료!")

    while True:
        time.sleep(0.1)
        for horse in horses:
            if horse not in rankings:
                cond = st.session_state.conditions[horse]
                spd = random.randint(*condition_speed_modifier[cond])
                positions[horse] += spd
                if positions[horse] >= finish_line:
                    rankings.append(horse)

        # 시각화
        display = ""
        for horse in horses:
            pos = min(positions[horse], finish_line)
            bar = "▰" * (pos // 2)
            space = " " * ((finish_line // 2) - len(bar))
            goal = "┊"
            display += f"{horse}: {bar}{space}{goal}\n"
        race_box.markdown(f"```\n{display}```")

        if (mode == "1등만 맞추기 (Easy)" and len(rankings) >= 1) or \
           (mode == "1~3등 순서 맞추기 (Hard)" and len(rankings) >= 3):
            break

    st.subheader("🏁 경기 결과")
    medals = ["🥇", "🥈", "🥉"]
    for i, horse in enumerate(rankings[:3]):
        st.markdown(f"{medals[i]} {horse}")

    # 보상 계산
    if mode == "1등만 맞추기 (Easy)":
        if rankings[0] == pick:
            payout = bet_amount * 5
            st.success(f"🎯 정답! {payout:,}원 획득!")
            st.session_state.balance += payout
            result = "적중 (1등)"
        else:
            st.warning(f"❌ 틀렸습니다. {bet_amount:,}원 손실")
            st.session_state.balance -= bet_amount
            result = "실패"
    else:
        guess = [pick1, pick2, pick3]
        correct = rankings[:3]
        if guess == correct:
            payout = bet_amount * 50
            st.balloons()
            st.success(f"🎉 완벽 적중! {payout:,}원 획득!")
            st.session_state.balance += payout
            result = "정확 적중"
        elif all(p in correct for p in guess):
            payout = bet_amount * 3
            st.success(f"✨ 3등 안에 모두 포함! {payout:,}원 획득!")
            st.session_state.balance += payout
            result = "부분 적중"
        else:
            st.warning(f"😢 틀렸습니다. {bet_amount:,}원 손실")
            st.session_state.balance -= bet_amount
            result = "실패"

    # 경기 기록 저장
    record = {
        "모드": mode,
        "예상": pick if mode == "1등만 맞추기 (Easy)" else [pick1, pick2, pick3],
        "결과": rankings[:3],
        "베팅": bet_amount,
        "결과 판정": result
    }
    st.session_state.history.append(record)

    if st.session_state.balance <= 0:
        st.error("💀 자본이 모두 사라졌습니다. 새로고침하여 재시작하세요.")

# 경기 히스토리 보기
with st.expander("📊 지난 경기 기록 보기"):
    if st.session_state.history:
        for i, rec in enumerate(reversed(st.session_state.history[-10:]), 1):
            st.markdown(f"**경기 {len(st.session_state.history) - i + 1}**")
            st.markdown(f"- 모드: {rec['모드']}")
            st.markdown(f"- 내 베팅: {rec['예상']}")
            st.markdown(f"- 실제 결과: {rec['결과']}")
            st.markdown(f"- 결과: **{rec['결과 판정']}**, 베팅금: {rec['베팅']:,}원")
            st.markdown("---")
    else:
        st.info("아직 경기 기록이 없습니다.")
