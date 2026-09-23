import streamlit as st

st.set_page_config(page_title="3D Baskı Maliyet & Fiyat Hesaplayıcı", page_icon="🧊", layout="centered")

st.title("🧊 3D Baskı Fiyat Hesaplayıcı")
st.write("Ürün parametrelerini girerek net maliyet ve tavsiye edilen satış fiyatını hesaplayın.")

st.markdown("---")

st.sidebar.header("⚙️ Sabit Maliyet Ayarları")
filament_kg_fiyati = st.sidebar.number_input("Filament Makara Fiyatı (TL / kg)", value=500.0, step=10.0)
yazici_watt = st.sidebar.number_input("Yazıcı Gücü (Watt)", value=150, step=10)
elektrik_kwh_fiyati = st.sidebar.number_input("Elektrik kWh Fiyatı (TL)", value=2.60, step=0.1)
saatlik_yipranma = st.sidebar.number_input("Makine Aşınma Payı (TL / Saat)", value=2.0, step=0.5)

st.subheader("📦 Ürün Detayları")
col1, col2 = st.columns(2)

with col1:
    gram = st.number_input("Harcanan Filament (Gram)", min_value=1.0, value=50.0, step=1.0)
    sure_saat = st.number_input("Baskı Süresi (Saat)", min_value=0.1, value=3.0, step=0.5)

with col2:
    fire_orani = st.slider("Fire / Risk Payı (%)", min_value=0, max_value=30, value=10)
    kar_marji = st.slider("Hedeflenen Kâr Marjı (%)", min_value=0, max_value=500, value=150)

st.markdown("---")

filament_maliyeti = (gram / 1000.0) * filament_kg_fiyati
elektrik_maliyeti = (yazici_watt / 1000.0) * sure_saat * elektrik_kwh_fiyati
yipranma_maliyeti = sure_saat * saatlik_yipranma

ara_toplam = filament_maliyeti + elektrik_maliyeti + yipranma_maliyeti
fire_maliyeti = ara_toplam * (fire_orani / 100.0)
net_maliyet = ara_toplam + fire_maliyeti

satis_fiyati = net_maliyet * (1 + (kar_marji / 100.0))
net_kar = satis_fiyati - net_maliyet

st.subheader("📊 Maliyet ve Fiyat Özeti")

m1, m2, m3 = st.columns(3)
m1.metric(label="Net Maliyet", value=f"{net_maliyet:.2f} TL")
m2.metric(label="Tavsiye Edilen Fiyat", value=f"{satis_fiyati:.2f} TL")
m3.metric(label="Tahmini Kâr", value=f"{net_kar:.2f} TL")

st.markdown("---")

with st.expander("🔍 Maliyet Detaylarını Gör"):
    st.write(f"- **Filament Tüketimi:** {filament_maliyeti:.2f} TL")
    st.write(f"- **Elektrik Tüketimi:** {elektrik_maliyeti:.2f} TL")
    st.write(f"- **Makine Amortismanı:** {yipranma_maliyeti:.2f} TL")
    st.write(f"- **Fire / Risk Payı (%{fire_orani}):** {fire_maliyeti:.2f} TL")
