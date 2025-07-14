import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(page_title="تحليل تداول ذكي", layout="wide")

st.title("📊 تطبيق تحليل تداول ذكي باستخدام الانحدار والذكاء الاصطناعي")

st.markdown("📁 ارفع ملف CSV يحتوي على الأعمدة التالية: Date, Close, Volume (يفضل أيضًا Open, High, Low)")

uploaded_file = st.file_uploader("Drag and drop file here", type=["csv"])

if uploaded_file is not None:
    try:
        # ✅ حل مشكلة الترميز
        df = pd.read_csv(uploaded_file, encoding='utf-8', errors='ignore')

        df.columns = [col.strip() for col in df.columns]  # إزالة الفراغات من أسماء الأعمدة
        df.dropna(inplace=True)  # حذف الصفوف الفارغة إن وجدت

        # ✅ تحويل العمود Date إلى نوع تاريخ
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])

        st.success("تم تحميل البيانات بنجاح!")

        st.subheader("🔍 عرض البيانات الأولية")
        st.dataframe(df.head())

        # ✅ رسم الأسعار
        st.subheader("📈 رسم بياني للسعر")
        plt.figure(figsize=(12, 5))
        plt.plot(df['Date'], df['Close'], label="Close Price", color="blue")
        plt.xlabel("التاريخ")
        plt.ylabel("السعر")
        plt.legend()
        st.pyplot(plt)

        # ✅ نموذج انحدار بسيط للتوقع
        st.subheader("🤖 نموذج انحدار للتوقع")
        df['Days'] = np.arange(len(df))  # تحويل التاريخ إلى أرقام

        model = LinearRegression()
        model.fit(df[['Days']], df['Close'])

        df['Predicted'] = model.predict(df[['Days']])

        # ✅ رسم التوقع
        plt.figure(figsize=(12, 5))
        plt.plot(df['Date'], df['Close'], label="Close Price", color="blue")
        plt.plot(df['Date'], df['Predicted'], label="Predicted", color="orange", linestyle='--')
        plt.xlabel("التاريخ")
        plt.ylabel("السعر")
        plt.legend()
        st.pyplot(plt)

        st.success("✅ تم إنشاء التوقع بنجاح")

    except Exception as e:
        st.error(f"حدث خطأ أثناء قراءة الملف أو معالجته: {str(e)}")
