import streamlit as st
import pandas as pd
import random

# 간단한 주가 시뮬레이션용 초기 데이터
price_data = {
    "삼성전자": random.randint(60000, 80000),
    "애플": random.randint(140, 180),
    "테슬라": random.randint(200, 300),
    "MSFT": random.randint(280, 320),
    "네이버": random.randint(160000, 200000)
}

# 세션 상태 초기화
if "cash" not in st.session_state:
    st.session_state.cash = 10_000_000
if "portfolio" not in st.session_state:
    st.session_state.portfolio = {}

st.set_page_config(page_title="📈 모의 주식 투자", layout="centered")
st.title("📈 Streamlit 모의 주식 투자 시뮬레이터")
st.markdown(f"**💰 보유 현금: {int(st.session_state.cash):,}원**")

# 종목 선택
stock_list = list(price_data.keys())
stock = st.selectbox("종목 선택", stock_list)
current_price = price_data[stock]
st.metric(label="📌 현재 가격", value=f"{current_price:,}원")

# 매수/매도 입력
col1, col2 = st.columns(2)
with col1:
    qty = st.number_input("매수 수량", min_value=1, value=1, key="buy_qty")
    if st.button("✅ 매수"):
        total_cost = qty * current_price
        if st.session_state.cash >= total_cost:
            st.session_state.cash -= total_cost
            old_qty, old_avg = st.session_state.portfolio.get(stock, (0, 0))
            new_qty = old_qty + qty
            new_avg = (old_avg * old_qty + current_price * qty) / new_qty
            st.session_state.portfolio[stock] = (new_qty, new_avg)
            st.success(f"{stock} {qty}주 매수 완료!")
        else:
            st.error("잔액 부족")

    if st.button("🧨 전액 매수"):
        max_qty = st.session_state.cash // current_price
        if max_qty > 0:
            total_cost = max_qty * current_price
            st.session_state.cash -= total_cost
            old_qty, old_avg = st.session_state.portfolio.get(stock, (0, 0))
            new_qty = old_qty + max_qty
            new_avg = (old_avg * old_qty + current_price * max_qty) / new_qty
            st.session_state.portfolio[stock] = (new_qty, new_avg)
            st.success(f"{stock} {max_qty}주 전액 매수 완료!")
        else:
            st.warning("살 수 있는 수량이 없습니다.")

with col2:
    sell_qty = st.number_input("매도 수량", min_value=1, value=1, key="sell_qty")
    if st.button("💼 매도"):
        if stock in st.session_state.portfolio:
            owned_qty, avg_price = st.session_state.portfolio[stock]
            if sell_qty <= owned_qty:
                st.session_state.cash += sell_qty * current_price
                remaining = owned_qty - sell_qty
                if remaining == 0:
                    del st.session_state.portfolio[stock]
                else:
                    st.session_state.portfolio[stock] = (remaining, avg_price)
                st.success(f"{stock} {sell_qty}주 매도 완료!")
            else:
                st.error("보유 수량보다 많습니다.")
        else:
            st.error("해당 종목 보유 중 아님")

# 🧹 전체 보유 주식 전량 매도
if st.button("🏃‍♂️ 모든 주식 전량 매도"):
    total_revenue = 0
    for s, (qty, avg) in list(st.session_state.portfolio.items()):
        now_price = price_data[s]
        revenue = qty * now_price
        total_revenue += revenue
        del st.session_state.portfolio[s]
    st.session_state.cash += total_revenue
    st.success(f"모든 종목 전량 매도 완료! {int(total_revenue):,}원 회수")

# 포트폴리오 표시
st.subheader("📂 나의 포트폴리오")
if st.session_state.portfolio:
    rows = []
    for s, (qty, avg) in st.session_state.portfolio.items():
        now = price_data[s]
        value = now * qty
        gain = (now - avg) * qty
        pct = (now - avg) / avg * 100
        rows.append({
            "종목": s,
            "수량": qty,
            "평균단가": int(avg),
            "현재가": now,
            "평가금액": int(value),
            "손익": int(gain),
            "수익률": f"{pct:.2f}%"
        })
    st.dataframe(pd.DataFrame(rows))
else:
    st.info("보유한 종목이 없습니다.")

# 하루 지나기 (주가 랜덤 변경)
if st.button("📉 하루 지나기 (주가 변동)"):
    for s in price_data:
        rate = random.uniform(-0.05, 0.05)
        price_data[s] = max(1, int(price_data[s] * (1 + rate)))
    st.success("하루가 지났습니다. 주가가 변동되었습니다.")

# 전체 초기화
if st.button("🔄 전체 초기화"):
    st.session_state.cash = 10_000_000
    st.session_state.portfolio = {}
    st.success("초기화 완료")
