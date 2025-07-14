import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, LogisticRegression, Lasso
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="تحليل تداول ذكي", layout="wide")
st.title("📈 تطبيق تحليل تداول ذكي باستخدام الانحدار والذكاء الاصطناعي")

uploaded_file = st.file_uploader("📤 قم برفع ملف بيانات CSV يحتوي على الأعمدة: Date, Close, Volume, RSI, EMA", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📋 معاينة البيانات")
    st.dataframe(df.head())

    required_cols = {'Close', 'Volume', 'RSI', 'EMA'}
    if not required_cols.issubset(df.columns):
        st.error("❌ الملف لا يحتوي على الأعمدة المطلوبة.")
    else:
        df['Target'] = df['Close'].shift(-1) > df['Close']
        features = ['Close', 'Volume', 'RSI', 'EMA']
        df = df.dropna()
        X = df[features]
        y = df['Target'].astype(int)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        linear_model = LinearRegression().fit(X_train_scaled, y_train)
        logistic_model = LogisticRegression().fit(X_train_scaled, y_train)
        lasso_model = Lasso(alpha=0.1).fit(X_train_scaled, y_train)

        linear_preds = linear_model.predict(X_test_scaled)
        logistic_preds = logistic_model.predict_proba(X_test_scaled)[:, 1]
        lasso_preds = lasso_model.predict(X_test_scaled)

        st.subheader("📊 نتائج النماذج")
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(df['Date'].iloc[-len(y_test):], logistic_preds, label="Logistic Regression", color='blue')
        ax.plot(df['Date'].iloc[-len(y_test):], linear_preds, label="Linear Regression", color='green')
        ax.plot(df['Date'].iloc[-len(y_test):], lasso_preds, label="Lasso Regression", color='orange')
        ax.axhline(0.5, color='red', linestyle='--', label="Threshold 0.5")
        ax.set_title("تحليل إشارات التداول")
        ax.set_xlabel("التاريخ")
        ax.set_ylabel("إشارة النموذج")
        ax.legend()
        ax.grid(True)
        plt.xticks(rotation=45)
        st.pyplot(fig)

        st.subheader("🧠 التوصيات")
        latest_signal = logistic_preds[-1]
        if latest_signal > 0.6:
            st.success(f"🔼 النموذج يقترح: شراء (احتمال الصعود {latest_signal:.2%})")
        elif latest_signal < 0.4:
            st.error(f"🔽 النموذج يقترح: بيع (احتمال الهبوط {1 - latest_signal:.2%})")
        else:
            st.info(f"⏸️ النموذج يقترح: ترقب (الإشارة غير مؤكدة)")