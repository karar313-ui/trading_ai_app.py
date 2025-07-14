import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="تطبيق تحليل تداول ذكي", layout="wide")

st.title("📊 تطبيق تحليل تداول ذكي باستخدام الانحدار والذكاء الاصطناعي")

st.markdown("🔻 يرجى رفع ملف CSV يحتوي على الأعمدة التالية: Date, Open, High, Low, Close, Volume")

uploaded_file = st.file_uploader("ارفع ملف CSV هنا", type="csv")

if uploaded_file is not None:
    try:
        # محاولة قراءة الملف بترميز آمن
        df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
        
        # التأكد من وجود الأعمدة المطلوبة
        required_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        if not all(col in df.columns for col in required_columns):
            st.error("❌ الملف لا يحتوي على الأعمدة المطلوبة: Date, Open, High, Low, Close, Volume")
        else:
            # تحويل التاريخ
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.sort_values('Date')

            st.success("✅ تم تحميل الملف بنجاح!")
            st.dataframe(df.tail())

            # رسم السعر والإغلاق
            fig, ax = plt.subplots(figsize=(12, 4))
            ax.plot(df['Date'], df['Close'], label='الإغلاق', color='blue')
            ax.set_title("سعر الإغلاق")
            ax.set_xlabel("التاريخ")
            ax.set_ylabel("السعر")
            ax.grid(True)
            ax.legend()
            st.pyplot(fig)

            # رسم الفوليوم
            fig2, ax2 = plt.subplots(figsize=(12, 2))
            ax2.bar(df['Date'], df['Volume'], color='orange')
            ax2.set_title("الفوليوم")
            ax2.set_xlabel("التاريخ")
            ax2.set_ylabel("الحجم")
            ax2.grid(True)
            st.pyplot(fig2)

    except Exception as e:
        st.error(f"❌ حدث خطأ أثناء قراءة الملف:\n\n{str(e)}")
else:
    st.info("📁 يرجى رفع ملف CSV لبدء التحليل.")
