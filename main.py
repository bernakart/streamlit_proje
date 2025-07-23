import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tarz_mesajlari = {
    "kurumsal": "Metni profesyonel ve resmi algılanan bir dil ile yeniden yaz.",
    "akademik": "Metni akademik, tarafsız ve bilimsel bir dille yeniden yaz.",
    "samimi": "Metni doğal, sıcak ve arkadaşça bir dille yeniden yaz.",
    "mail": "Metni düzgün, resmi ve etkili bir e-posta haline getir.",
    "hicbiri": "Metni olduğu gibi koru, yalnızca çeviri, başlık ve özet işlemleri yap."
}

dil_mesajlari = {
    "türkce": "Metni Türkçe olarak sun.",
    "ingilizce": "Metni İngilizce olarak sun.",
    "almanca": "Metni Almanca olarak sun.",
    "diğer": "Metni kullanıcı tarafından belirtilen farklı bir dile çevir."
}

st.title("Yapay Zeka Yazı Editörü")

metin = st.text_area("✍️ Metni Giriniz:", height=200)

# "SEÇİNİZ" seçenek olarak eklendi
tarz_options = ["SEÇİNİZ"] + list(tarz_mesajlari.keys())
dil_options = ["SEÇİNİZ"] + list(dil_mesajlari.keys())

tarz = st.selectbox(
    "🎯 Yazı Tarzı:",
    options=tarz_options,
    index=0  # Başlangıçta "SEÇİNİZ" seçili
)

dil = st.selectbox(
    "🌐 Hedef Dil:",
    options=dil_options,
    index=0  # Başlangıçta "SEÇİNİZ" seçili
)

baslik = st.checkbox("🏷️ Başlık eklemek ister misiniz?")
ozet = st.checkbox("✂️ Metni özetlememi ister misiniz?")

if st.button("✅ Metni Düzenle"):
    if not metin.strip():
        st.warning("Lütfen metin giriniz.")
    elif tarz == "SEÇİNİZ":
        st.warning("Lütfen bir yazı tarzı seçiniz.")
    elif dil == "SEÇİNİZ":
        st.warning("Lütfen bir hedef dil seçiniz.")
    else:
        sistem_prompt = "Sen profesyonel bir yazı editörüsün. "
        sistem_prompt += dil_mesajlari.get(dil, "")
        sistem_prompt += " " + tarz_mesajlari.get(tarz, tarz_mesajlari["hicbiri"])
        if baslik:
            sistem_prompt += " Metne uygun etkileyici ve öz bir başlık oluştur."
        if ozet:
            sistem_prompt += " Ayrıca metni kısaca özetle ve önemli detayları vurgula."

        mesajlar = [
            {"role": "system", "content": sistem_prompt},
            {"role": "user", "content": metin}
        ]

        try:
            cevap = client.chat.completions.create(
                model="gpt-4o",
                messages=mesajlar,
                temperature=0.7,
                max_tokens=800
            )
            st.subheader("📄 Düzenlenmiş Metin:")
            st.text_area("", cevap.choices[0].message.content.strip(), height=300)
        except Exception as e:
            st.error(f"Hata: {str(e)}")
