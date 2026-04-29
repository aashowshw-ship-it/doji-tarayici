import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(
    page_title="Doji Tarayıcı",
    page_icon="📊",
    layout="wide"
)

DEFAULT_TICKERS = [
"A1CAP.IS","A1YEN.IS","ACSEL.IS","ADEL.IS","ADESE.IS","ADGYO.IS","AEFES.IS","AFYON.IS","AGESA.IS","AGHOL.IS",
"AGROT.IS","AGYO.IS","AHGAZ.IS","AHSGY.IS","AKBNK.IS","AKCNS.IS","AKENR.IS","AKFGY.IS","AKFIS.IS","AKFYE.IS",
"AKGRT.IS","AKMGY.IS","AKSA.IS","AKSEN.IS","AKSGY.IS","AKSUE.IS","AKYHO.IS","ALARK.IS","ALBRK.IS","ALCAR.IS",
"ALCTL.IS","ALFAS.IS","ALGYO.IS","ALKA.IS","ALKIM.IS","ALKLC.IS","ALTNY.IS","ALVES.IS","ANELE.IS","ANGEN.IS",
"ANHYT.IS","ANSGR.IS","ARASE.IS","ARCLK.IS","ARDYZ.IS","ARENA.IS","ARMGD.IS","ARSAN.IS","ARZUM.IS","ASELS.IS",
"ASGYO.IS","ASTOR.IS","ASUZU.IS","ATAKP.IS","ATATP.IS","AVGYO.IS","AVHOL.IS","AVOD.IS","AVPGY.IS","AYDEM.IS",
"AYGAZ.IS","AZTEK.IS","BAGFS.IS","BAKAB.IS","BANVT.IS","BARMA.IS","BASGZ.IS","BERA.IS","BEYAZ.IS","BFREN.IS",
"BIENY.IS","BIGCH.IS","BIMAS.IS","BINHO.IS","BIOEN.IS","BIZIM.IS","BJKAS.IS","BLCYT.IS","BMSCH.IS","BMSTL.IS",
"BOBET.IS","BORLS.IS","BOSSA.IS","BRISA.IS","BRKSN.IS","BRLSM.IS","BRSAN.IS","BRYAT.IS","BSOKE.IS","BTCIM.IS",
"BUCIM.IS","BURCE.IS","BURVA.IS","BVSAN.IS","BYDNR.IS","CANTE.IS","CATES.IS","CCOLA.IS","CEMAS.IS","CEMTS.IS",
"CIMSA.IS","CLEBI.IS","CMBTN.IS","CMENT.IS","CONSE.IS","CRFSA.IS","CUSAN.IS","CVKMD.IS","CWENE.IS","DAPGM.IS",
"DARDL.IS","DENGE.IS","DERHL.IS","DESA.IS","DESPC.IS","DEVA.IS","DGATE.IS","DGNMO.IS","DMRGD.IS","DOAS.IS",
"DOCO.IS","DOFER.IS","DOHOL.IS","DOKTA.IS","DURDO.IS","DYOBY.IS","EBEBK.IS","ECILC.IS","ECZYT.IS","EDATA.IS",
"EFORC.IS","EGEEN.IS","EGGUB.IS","EGPRO.IS","EGSER.IS","EKGYO.IS","EKOS.IS","EKSUN.IS","ENERY.IS","ENJSA.IS",
"ENKAI.IS","EUPWR.IS","EREGL.IS","ESCAR.IS","ESCOM.IS","EUPWR.IS","FENER.IS","FONET.IS","FORTE.IS","FROTO.IS",
"GARAN.IS","GEDIK.IS","GENIL.IS","GESAN.IS","GLYHO.IS","GOKNR.IS","GOLTS.IS","GOODY.IS","GOZDE.IS","GSDHO.IS",
"GSRAY.IS","GUBRF.IS","GWIND.IS","HALKB.IS","HATSN.IS","HEDEF.IS","HEKTS.IS","HUNER.IS","HURGZ.IS","INDES.IS",
"INFO.IS","IPEKE.IS","ISCTR.IS","ISDMR.IS","ISFIN.IS","ISGYO.IS","ISMEN.IS","ISSEN.IS","IZMDC.IS","JANTS.IS",
"KAREL.IS","KARSN.IS","KCAER.IS","KCHOL.IS","KERVN.IS","KFEIN.IS","KIMMR.IS","KLKIM.IS","KLSER.IS","KMPUR.IS",
"KONTR.IS","KONYA.IS","KORDS.IS","KOZAA.IS","KOZAL.IS","KRDMA.IS","KRDMB.IS","KRDMD.IS","KRVGD.IS","KTLEV.IS",
"KUYAS.IS","KZBGY.IS","LIDER.IS","LINK.IS","LOGO.IS","MACKO.IS","MAGEN.IS","MAKIM.IS","MAVI.IS","MEDTR.IS",
"MEGMT.IS","MEKAG.IS","MERCN.IS","MGROS.IS","MIATK.IS","MNDTR.IS","MOBTL.IS","MPARK.IS","MTRKS.IS","NATEN.IS",
"NETAS.IS","NTGAZ.IS","NTHOL.IS","NUHCM.IS","OBAMS.IS","ODAS.IS","ORGE.IS","OTKAR.IS","OYAKC.IS","OZKGY.IS",
"PAPIL.IS","PARSN.IS","PASEU.IS","PATEK.IS","PENTA.IS","PETKM.IS","PGSUS.IS","PNLSN.IS","PNSUT.IS","POLHO.IS",
"PRKME.IS","PSGYO.IS","QUAGR.IS","REEDR.IS","RYGYO.IS","RYSAS.IS","SAHOL.IS","SASA.IS","SDTTR.IS","SELEC.IS",
"SISE.IS","SKBNK.IS","SMRTG.IS","SNGYO.IS","SOKM.IS","TABGD.IS","TATEN.IS","TATGD.IS","TAVHL.IS","TCELL.IS",
"THYAO.IS","TKFEN.IS","TKNSA.IS","TOASO.IS","TRGYO.IS","TSKB.IS","TTKOM.IS","TTRAK.IS","TUKAS.IS","TUPRS.IS",
"TURSG.IS","ULKER.IS","VAKBN.IS","VESBE.IS","VESTL.IS","YEOTK.IS","YKBNK.IS","YYLGD.IS","ZOREN.IS"
]

st.title("📊 Peş Peşe Doji Tarayıcı")

st.write("Günlük mumlarda son mumdan geriye doğru peş peşe doji yapan hisseleri tarar.")

tickers_text = st.text_area(
    "Hisse listesi",
    value="\n".join(DEFAULT_TICKERS),
    height=260
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

if st.button("🚀 Taramayı Başlat"):
    tickers = [
        x.strip().upper()
        for x in tickers_text.splitlines()
        if x.strip()
    ]

    results = []
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

            df = df.dropna()

            body = (df["Open"] - df["Close"]).abs()
            candle_range = df["High"] - df["Low"]

            df["doji"] = (
                (candle_range > 0) &
                (body <= candle_range * doji_ratio)
            )

            consecutive = 0

            for val in reversed(df["doji"].tolist()):
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
                    "Açılış": round(float(df["Open"].iloc[-1]), 2),
                    "Yüksek": round(float(df["High"].iloc[-1]), 2),
                    "Düşük": round(float(df["Low"].iloc[-1]), 2),
                    "Kapanış": round(float(df["Close"].iloc[-1]), 2),
                    "Doji Oranı": round(last_ratio, 4)
                })

        except Exception as e:
            st.warning(f"{ticker} hata verdi: {e}")

        progress.progress((i + 1) / len(tickers))

    result_df = pd.DataFrame(results)

    status.write("Tarama tamamlandı.")

    if result_df.empty:
        st.error("Sonuç bulunamadı.")
    else:
        st.success(f"{len(result_df)} hisse bulundu.")
        st.dataframe(result_df, use_container_width=True)