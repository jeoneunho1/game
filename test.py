import streamlit as st
import pandas as pd
import random

# 주식 종목별 초기 주가 (간이 시뮬레이션용)
price_data = {
    "삼성전자": random.randint(60000, 80000),
    "애플": random.randint(140, 180),
    "테슬라": random.randint(200, 300),
    "MSFT": random.randint(280, 320),
    "네이버": random.randint(160000, 200000)
}

# 상태 초기화
if "cash" not in st.session_state:
    st.session_state.cash = 10_000_000
if "portfolio" not in st.session_state:
    st.session_state.portfolio = {}
if "history" not in st.session_state:
    st.session_state.history = []

st.set_page_config(page_title="📈 오프라인 모의 주식 투자", layout="centered")
st.title("📈 오프라인 모의 주식 투자 시뮬레이터")
st.markdown(f"**💰 보유 현금: {int(st.session_state.cash):,}원**")

# 종목 선택
stock_list = list(price_data.keys())
stock = st.selectbox("종목 선택", stock_list)
current_price = price_data[stock]
st.metric(label="📌 현재 가격", value=f"{current_price:,}원")

# 매수/매도
col1, col2 = st.columns(2)
with col1:
    buy_qty = st.number_input("매수 수량", min_value=1, value=1)
    if st.button("✅ 매수"):
        cost = buy_qty * current_price
        if st.session_state.cash >= cost:
            st.session_state.cash -= cost
            if stock in st.session_state.portfolio:
                old_qty, old_avg = st.session_state.portfolio[stock]
                total_qty = old_qty + buy_qty
                avg_price = (old_avg * old_qty + current_price * buy_qty) / total_qty
                st.session_state.portfolio[stock] = (total_qty, avg_price)
            else:
                st.session_state.portfolio[stock] = (buy_qty, current_price)
            st.success(f"{stock} {buy_qty}주 매수 완료!")
        else:
            st.error("잔액 부족!")

with col2:
    sell_qty = st.number_input("매도 수량", min_value=1, value=1, key="sell_qty")
    if st.button("💼 매도"):
        if stock in st.session_state.portfolio:
            owned_qty, avg_price = st.session_state.portfolio[stock]
            if sell_qty <= owned_qty:
                st.session_state.cash += sell_qty * current_price
                new_qty = owned_qty - sell_qty
                if new_qty == 0:
                    del st.session_state.portfolio[stock]
                else:
                    st.session_state.portfolio[stock] = (new_qty, avg_price)
                st.success(f"{stock} {sell_qty}주 매도 완료!")
            else:
                st.error("보유 수량 부족")
        else:
            st.error("보유하지 않은 종목입니다")

# 포트폴리오
st.subheader("📂 포트폴리오")
if st.session_state.portfolio:
    rows = []
    for stock, (qty, avg) in st.session_state.portfolio.items():
        now = price_data[stock]
        total_val = now * qty
        gain = (now - avg) * qty
        pct = (now - avg) / avg * 100
        rows.append({
            "종목": stock,
            "수량": qty,
            "평균단가": int(avg),
            "현재가": now,
            "평가금액": int(total_val),
            "손익": int(gain),
            "수익률": f"{pct:.2f}%"
        })
    st.dataframe(pd.DataFrame(rows))
else:
    st.info("보유 종목이 없습니다.")

# 새 주가 시뮬레이션
if st.button("📉 하루 지나기 (가격 변동)"):
    for stock in price_data:
        delta = random.uniform(-0.07, 0.07)  # 최대 ±7%
        price_data[stock] = max(1, int(price_data[stock] * (1 + delta)))
    st.success("하루가 지났습니다! 주가가 변동되었습니다.")

# 리셋
if st.button("🔄 전체 초기화"):
    st.session_state.cash = 10_000_000
    st.session_state.portfolio = {}
    st.success("초기화 완료")
