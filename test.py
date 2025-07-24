import streamlit as st
import random
import time

st.set_page_config(page_title="🏇 경마 베팅 게임", layout="centered")

# 초기 잔액 설정
if "balance" not in st.session_state:
    st.session_state.balance = 100000  # 10만원

# 경주마 목록
horses = [f"말 {i+1}" for i in range(12)]

st.title("🏇 실시간 경마 베팅 게임")
st.caption("말을 선택하고 1등을 맞혀보세요!")

# 잔액 및 베팅 UI
st.markdown(f"**💰 현재 잔액:** {st.session_state.balance:,}원")

col1, col2 = st.columns(2)
with col1:
    selected_horse = st.selectbox("🐴 베팅할 말을 선택하세요:", horses)
with col2:
    bet_amount = st.number_input("💸 베팅 금액 (원)", min_value=10000, max_value=st.session_state.balance, step=10000)

start_button = st.button("🚦 경주 시작!")

# 경주 시작
if start_button:
    if bet_amount > st.session_state.balance:
        st.error("베팅 금액이 잔액보다 많습니다.")
    else:
        st.success(f"{selected_horse}에 {bet_amount:,}원 베팅하셨습니다!")
        st.write("🏁 경주 시작!")
        
        # 초기 위치
        positions = {horse: 0 for horse in horses}
        finish_line = 100

        progress_placeholder = st.empty()

        winner = None
        while True:
            time.sleep(0.2)
            # 각 말마다 랜덤한 속도 (약간의 확률 차이 부여)
            for horse in horses:
                positions[horse] += random.randint(1, 6 if horse != "말 1" else 7)  # 말 1이 약간 유리함

            # 말 위치 시각화 (텍스트 기반)
            lines = []
            for horse in horses:
                bar = "▰" * (positions[horse] // 3)
                lines.append(f"{horse}: {bar}")

            progress_placeholder.markdown("```\n" + "\n".join(lines) + "\n```")

            # 결승선 도달 확인
            for horse, pos in positions.items():
                if pos >= finish_line:
                    winner = horse
                    break
            if winner:
                break

        st.subheader(f"🏆 우승마: {winner}!")

        # 결과 처리
        if selected_horse == winner:
            reward = bet_amount * 10
            st.session_state.balance += reward
            st.success(f"🎉 정답! {reward:,}원 적중! 잔액: {st.session_state.balance:,}원")
        else:
            st.session_state.balance -= bet_amount
            st.error(f"❌ 아쉽습니다. {bet_amount:,}원 잃었습니다. 잔액: {st.session_state.balance:,}원")

        # 다시하기
        if st.session_state.balance <= 0:
            st.warning("💀 잔액이 0원이 되어 게임이 종료됩니다. 다시 시작하려면 앱을 새로고침하세요.")
