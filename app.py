import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(
    page_title="Doji Tarayıcı",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Peş Peşe Doji Tarayıcı")

st.write("Günlük mumlarda son mumdan geriye doğru peş peşe doji yapan hisseleri tarar.")

tickers_text = st.text_area(
    "Hisse listesi",
    value="""FRIGO.IS
SNGYO.IS
TURSG.IS
THYAO.IS
ASELS.IS
SISE.IS
KCHOL.IS
SAHOL.IS
EREGL.IS
BIMAS.IS""",
    height=220
)

doji_ratio = st.slider(
    "Doji hassasiyeti",
    min_value=0.01,
    max_value=0.20,
    value=0.05,
    step=0.01
)

min_consecutive = st.number_input(
    "Minimum peş peşe doji",
    min_value=1,
    max_value=10,
    value=2
)

period = st.selectbox(
    "Veri aralığı",
    ["1mo", "3mo", "6mo", "1y"],
    index=1
)

def clean_yfinance_df(df):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df.loc[:, ~df.columns.duplicated()]
    return df

if st.button("🚀 Taramayı Başlat"):
    tickers = [
        x.strip().upper().replace('"', "").replace(",", "")
        for x in tickers_text.splitlines()
        if x.strip()
    ]

    results = []
    errors = []
    progress = st.progress(0)
    status = st.empty()

    for i, ticker in enumerate(tickers):
        try:
            status.write(f"Taranıyor: {ticker}")

            df = yf.download(
                ticker,
                period=period,
                interval="1d",
                auto_adjust=False,
                progress=False
            )

            if df.empty or len(df) < min_consecutive:
                progress.progress((i + 1) / len(tickers))
                continue

            df = clean_yfinance_df(df)
            df = df.dropna()

            open_ = df["Open"].astype(float)
            high = df["High"].astype(float)
            low = df["Low"].astype(float)
            close = df["Close"].astype(float)

            body = (open_ - close).abs()
            candle_range = high - low

            doji = (
                (candle_range > 0) &
                (body <= candle_range * doji_ratio)
            )

            consecutive = 0

            for val in reversed(doji.tolist()):
                if bool(val):
                    consecutive += 1
                else:
                    break

            if consecutive >= min_consecutive:
                last_body = float(body.iloc[-1])
                last_range = float(candle_range.iloc[-1])
                last_ratio = last_body / last_range if last_range > 0 else 0

                results.append({
                    "Hisse": ticker,
                    "Peş Peşe Doji": consecutive,
                    "Son Tarih": df.index[-1].strftime("%Y-%m-%d"),
                    "Son Kapanış": round(float(close.iloc[-1]), 2),
                    "Doji Oranı": round(last_ratio, 4)
                })

        except Exception as e:
            errors.append(f"{ticker}: {e}")

        progress.progress((i + 1) / len(tickers))

    result_df = pd.DataFrame(results)

    status.write("Tarama tamamlandı.")

    if errors:
        with st.expander("Hata veren hisseler"):
            for err in errors:
                st.write(err)

    if result_df.empty:
        st.error("Sonuç bulunamadı.")
    else:
        st.success(f"{len(result_df)} hisse bulundu.")
        st.dataframe(result_df, use_container_width=True)
