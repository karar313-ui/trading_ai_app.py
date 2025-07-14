import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(page_title="تحليل تداول ذكي", layout="wide")

st.title("📈 تطبيق تحليل تداول ذكي باستخدام الانحدار والذكاء الاصطناعي")

uploaded_file = st.file_uploader("📤 ارفع ملف CSV يحتوي على الأعمدة التالية: Date, Close, Volume (اختياري: Open, High, Low)", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, encoding='utf-8')

        # تحويل التاريخ
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index('Date', inplace=True)

        # عرض بيانات عامة
        st.subheader("📊 نظرة عامة على البيانات")
        st.write(df.head())

        # رسم إغلاق السعر
        if 'Close' in df.columns:
            st.subheader("📉 رسم بياني لسعر الإغلاق")
            plt.figure(figsize=(12, 5))
            plt.plot(df['Close'], label='Close Price')
            plt.legend()
            st.pyplot(plt)

        # نموذج انحدار بسيط لتوقع الإغلاق
        if 'Close' in df.columns:
            st.subheader("🤖 توقع سعر الإغلاق (انحدار خطي)")
            df = df.reset_index()
            df['Time'] = np.arange(len(df))
            model = LinearRegression()
            model.fit(df[['Time']], df['Close'])
            df['Prediction'] = model.predict(df[['Time']])

            plt.figure(figsize=(12, 5))
            plt.plot(df['Date'], df['Close'], label='Actual')
            plt.plot(df['Date'], df['Prediction'], label='Predicted', linestyle='--')
            plt.legend()
            st.pyplot(plt)

    except Exception as e:
        st.error(f"حدث خطأ في قراءة الملف أو معالجته: {e}")
