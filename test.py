import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# 초기 세션 상태
if "cash" not in st.session_state:
    st.session_state.cash = 10_000_000  # 초기 자본 1000만원
if "portfolio" not in st.session_state:
    st.session_state.portfolio = {}  # 종목별 보유 정보

st.set_page_config(page_title="📈 모의 주식 투자 프로그램", layout="wide")
st.title("📈 실시간 모의 주식 투자 시뮬레이터")

# 종목 선택
ticker_input = st.text_input("🔍 주식 종목 티커 입력 (예: AAPL, TSLA, 005930.KS)", value="AAPL")
stock = yf.Ticker(ticker_input)

# 가격 정보 가져오기
data = stock.history(period="1mo")
if data.empty:
    st.error("주식 데이터를 가져올 수 없습니다. 티커를 확인하세요.")
    st.stop()

current_price = data["Close"][-1]
st.metric(label="📌 현재 가격", value=f"${current_price:.2f}" if "." in str(current_price) else f"{int(current_price):,}원")

# 주가 차트 시각화
with st.expander("📊 최근 1개월 주가 차트 보기"):
    fig, ax = plt.subplots()
    data["Close"].plot(ax=ax)
    ax.set_title(f"{ticker_input} 종가 추이")
    st.pyplot(fig)

# 거래 UI
st.subheader("🛒 매수 / 매도")
col1, col2 = st.columns(2)
with col1:
    qty_buy = st.number_input("매수 수량", min_value=1, value=1)
    if st.button("✅ 매수"):
        total_cost = qty_buy * current_price
        if st.session_state.cash >= total_cost:
            st.session_state.cash -= total_cost
            if ticker_input in st.session_state.portfolio:
                old_qty, old_avg = st.session_state.portfolio[ticker_input]
                new_qty = old_qty + qty_buy
                new_avg = (old_avg * old_qty + current_price * qty_buy) / new_qty
                st.session_state.portfolio[ticker_input] = (new_qty, new_avg)
            else:
                st.session_state.portfolio[ticker_input] = (qty_buy, current_price)
            st.success(f"{qty_buy}주 매수 완료!")
        else:
            st.error("💸 잔액 부족")

with col2:
    qty_sell = st.number_input("매도 수량", min_value=1, value=1, key="sell_qty")
    if st.button("💼 매도"):
        if ticker_input in st.session_state.portfolio:
            owned_qty, avg_price = st.session_state.portfolio[ticker_input]
            if qty_sell <= owned_qty:
                st.session_state.cash += qty_sell * current_price
                new_qty = owned_qty - qty_sell
                if new_qty == 0:
                    del st.session_state.portfolio[ticker_input]
                else:
                    st.session_state.portfolio[ticker_input] = (new_qty, avg_price)
                st.success(f"{qty_sell}주 매도 완료!")
            else:
                st.error("❌ 보유 수량보다 많이 매도할 수 없습니다.")
        else:
            st.error("❌ 해당 종목을 보유하고 있지 않습니다.")

# 포트폴리오 표시
st.subheader("📂 나의 포트폴리오")
st.markdown(f"**💰 보유 현금:** {int(st.session_state.cash):,}원")

if st.session_state.portfolio:
    df = []
    for ticker, (qty, avg_price) in st.session_state.portfolio.items():
        current = yf.Ticker(ticker).history(period="1d")["Close"][-1]
        total = qty * current
        profit = (current - avg_price) * qty
        profit_pct = (current - avg_price) / avg_price * 100
        df.append({
            "종목": ticker,
            "수량": qty,
            "평균단가": round(avg_price, 2),
            "현재가": round(current, 2),
            "평가금액": round(total),
            "수익률(%)": round(profit_pct, 2),
            "손익": round(profit)
        })
    st.dataframe(pd.DataFrame(df))
else:
    st.info("현재 보유 종목이 없습니다.")
