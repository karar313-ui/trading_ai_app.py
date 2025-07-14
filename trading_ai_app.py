import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from chardet import detect

st.set_page_config(page_title="تطبيق تحليل تداول ذكي", layout="wide")
st.title("📊 تطبيق تحليل تداول ذكي باستخدام الانحدار والذكاء الاصطناعي")

st.markdown("🔻 يرجى رفع ملف CSV يحتوي على الأعمدة التالية: Date, Open, High, Low, Close, Volume")

uploaded_file = st.file_uploader("ارفع ملف CSV هنا", type="csv")

if uploaded_file is not None:
    try:
        uploaded_file.seek(0)
        raw_data = uploaded_file.read()

        # نحاول كشف الترميز، وإذا لم نستطع، نستخدم ترميز آمن
        result = detect(raw_data)
        encoding = result['encoding'] if result['encoding'] else 'ISO-8859-1'

        uploaded_file.seek(0)
        decoded_data = raw_data.decode(encoding)

        # كشف الفاصل
        first_line = decoded_data.split('\n')[0]
        if ';' in first_line:
            sep = ';'
        elif '\t' in first_line:
            sep = '\t'
        else:
            sep = ','

        # إعادة الملف كنص قابل للقراءة
        from io import StringIO
        string_io = StringIO(decoded_data)

        df = pd.read_csv(string_io, sep=sep, on_bad_lines='skip')

        required_columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        df.columns = [col.strip().lower() for col in df.columns]  # تنظيف الأعمدة
        if not all(col in df.columns for col in required_columns):
            st.error(f"❌ الملف لا يحتوي على الأعمدة المطلوبة: {required_columns}")
        else:
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date').reset_index(drop=True)

            st.success("✅ تم تحميل الملف بنجاح!")
            st.dataframe(df.tail())

            fig, ax = plt.subplots(figsize=(12, 4))
            ax.plot(df['date'], df['close'], label='الإغلاق', color='blue')
            ax.set_title("سعر الإغلاق")
            ax.set_xlabel("التاريخ")
            ax.set_ylabel("السعر")
            ax.grid(True)
            ax.legend()
            st.pyplot(fig)

            fig2, ax2 = plt.subplots(figsize=(12, 2))
            ax2.bar(df['date'], df['volume'], color='orange')
            ax2.set_title("الفوليوم")
            ax2.set_xlabel("التاريخ")
            ax2.set_ylabel("الحجم")
            ax2.grid(True)
            st.pyplot(fig2)

    except Exception as e:
        st.error(f"❌ حدث خطأ أثناء قراءة الملف:\n\n{str(e)}")

else:
    st.info("📁 يرجى رفع ملف CSV لبدء التحليل.")
