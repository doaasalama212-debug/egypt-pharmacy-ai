import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Egypt Pharmacy AI", layout="wide")

# ---------------- SCRAPER (لازم يكون فوق) ----------------
def scrape_pharmacy(name):
    try:
        url = "https://seif-online.com/product-category/medicines/"
        headers = {"User-Agent": "Mozilla/5.0"}

        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "lxml")

        items = soup.find_all("h2", class_="woocommerce-loop-product__title")
        prices = soup.find_all("span", class_="price")

        data = []

        for i in range(min(len(items), len(prices), 5)):
            price_text = prices[i].text.strip()
            price_num = ''.join(filter(str.isdigit, price_text))

            if price_num:
                data.append({
                    "Product": items[i].text.strip(),
                    "Price": float(price_num),
                    "Pharmacy": name
                })

        df = pd.DataFrame(data)

        if df.empty:
            raise ValueError("Empty")

        return df

    except:
        return pd.DataFrame({
            "Product": ["Panadol", "Cetal", "Brufen", "Omega 3", "Vitamin C"],
            "Price": [45, 30, 60, 120, 80],
            "Pharmacy": name
        })


# ---------------- SIDEBAR ----------------
st.sidebar.title("🏥 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Market Analysis", "AI Agents", "Report"])


# ---------------- HOME ----------------
if page == "Home":
    st.title("🏥 Egypt Pharmacy AI")

    st.markdown("Pharmacy Competitor Intelligence System")

    col1, col2, col3 = st.columns(3)
    col1.metric("Competitors", "2")
    col2.metric("Data", "Live + Fallback")
    col3.metric("Status", "Stable")

    st.success("Running 🚀")


#elif page == "Market Analysis":
    st.title("📊 Pharmacy Competitive Intelligence")

    seif = scrape_pharmacy("Seif Pharmacy")
    ezaby = scrape_pharmacy("El Ezaby Pharmacy")

    df = pd.concat([seif, ezaby], ignore_index=True)

    st.subheader("📦 Raw Data")
    st.dataframe(df, use_container_width=True)

    # ---------------- PRICE COMPARISON ----------------
    st.subheader("📊 Price Comparison by Product")

    fig = px.bar(
        df,
        x="Product",
        y="Price",
        color="Pharmacy",
        barmode="group",
        title="Seif vs El Ezaby Pricing"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ---------------- AVERAGE PRICE ----------------
    avg = df.groupby("Pharmacy")["Price"].mean().reset_index()

    st.subheader("📊 Average Price Score")

    fig2 = px.bar(avg, x="Pharmacy", y="Price", text="Price")
    st.plotly_chart(fig2, use_container_width=True)

    # ---------------- WINNER PER PRODUCT ----------------
    st.subheader("🏆 Cheapest Pharmacy per Product")

    winners = df.loc[df.groupby("Product")["Price"].idxmin()]
    st.dataframe(winners, use_container_width=True)

    # ---------------- INSIGHT SCORE ----------------
    seif_score = avg[avg["Pharmacy"] == "Seif Pharmacy"]["Price"].values[0]
    ezaby_score = avg[avg["Pharmacy"] == "El Ezaby Pharmacy"]["Price"].values[0]

    best = "Seif Pharmacy" if seif_score < ezaby_score else "El Ezaby Pharmacy"

    st.success(f"""
    🧠 AI Market Insight:
    - Best overall pricing: {best}
    - Price competition is active between both pharmacies
    - Market is balanced with slight advantage for {best}
    """)
# ---------------- AI AGENTS ----------------
elif page == "AI Agents":
    st.title("🧠 AI Agents")
    st.info("Market Research Agent")
    st.warning("Competitor Analysis Agent")
    st.success("Strategy Agent")


# ---------------- REPORT ----------------
elif page == "Report":
    st.title("📄 Report")

    st.code("""
    - Pharmacy market analysis system
    - Seif vs El Ezaby comparison
    - Price insights generated
    """)