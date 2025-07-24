import streamlit as st
import random
import time

st.set_page_config(page_title="🏇 경마 베팅 전략 게임", layout="centered")

# 초기 잔액 설정
if "balance" not in st.session_state:
    st.session_state.balance = 200000

horses = [f"말 {i+1}" for i in range(12)]

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

st.title("🏇 전략 경마 게임")
st.markdown(f"**💰 잔액: {st.session_state.balance:,}원**")

# 말 상태
if "conditions" not in st.session_state:
    st.session_state.conditions = generate_conditions()

with st.expander("🐴 이번 경기 말 컨디션 보기"):
    for horse, cond in st.session_state.conditions.items():
        st.write(f"{horse}: {cond}")

# 게임 모드 선택
mode = st.radio("🎮 게임 모드 선택", ["1등만 맞추기 (Easy)", "1~3등 순서 맞추기 (Hard)"])

# 유저 입력
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
    finish_line = 100
    rankings = []
    race_box = st.empty()

    st.session_state.conditions = generate_conditions()
    st.success(f"{' / '.join([pick1, pick2, pick3]) if mode != '1등만 맞추기 (Easy)' else pick} 에 {bet_amount:,}원 베팅 완료!")

    while True:
        time.sleep(0.15)
        for horse in horses:
            if horse not in rankings:
                cond = st.session_state.conditions[horse]
                spd_range = condition_speed_modifier[cond]
                positions[horse] += random.randint(*spd_range)

                if positions[horse] >= finish_line and horse not in rankings:
                    rankings.append(horse)

        # 화면 표시
        display = ""
        for horse in horses:
            bar = "▰" * (positions[horse] // 3)
            display += f"{horse}: {bar}\n"
        race_box.markdown(f"```\n{display}\n```")

        # 경기 종료 조건
        if (mode == "1등만 맞추기 (Easy)" and len(rankings) >= 1) or \
           (mode == "1~3등 순서 맞추기 (Hard)" and len(rankings) >= 3):
            break

    st.subheader("🏁 경기 결과")
    for i, horse in enumerate(rankings[:3]):
        medal = ["🥇", "🥈", "🥉"][i]
        st.markdown(f"{medal} {horse}")

    # 결과 판단 및 보상
    if mode == "1등만 맞추기 (Easy)":
        if rankings[0] == pick:
            payout = bet_amount * 5
            st.success(f"🎉 1등 적중! {payout:,}원 획득!")
            st.session_state.balance += payout
        else:
            st.warning(f"❌ 아쉽게도 틀렸습니다. {bet_amount:,}원 손실")
            st.session_state.balance -= bet_amount
    else:
        guess = [pick1, pick2, pick3]
        correct = rankings[:3]
        if guess == correct:
            payout = bet_amount * 50
            st.balloons()
            st.success(f"🎯 완벽 적중! {payout:,}원 획득!")
            st.session_state.balance += payout
        elif all(p in correct for p in guess):
            payout = bet_amount * 3
            st.success(f"✨ 순서는 다르지만 1~3등 안에 모두 포함! {payout:,}원 획득!")
            st.session_state.balance += payout
        else:
            st.warning(f"😢 틀렸습니다. {bet_amount:,}원 손실")
            st.session_state.balance -= bet_amount

    # 게임 종료 처리
    if st.session_state.balance <= 0:
        st.error("💀 자본이 모두 사라졌습니다. 새로고침하여 재시작하세요.")
