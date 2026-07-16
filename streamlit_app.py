import streamlit as st
import pandas as pd
import numpy as np
import datetime

# إعداد الصفحة
st.set_page_config(page_title="IT Support System", page_icon="🎫", layout="wide")
st.title("🎫 IT Support System - Erada Finance")

# تهيئة البيانات (في حالة عدم وجود بيانات)
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame({
        "ID": ["TICKET-1001"],
        "UserEmail": ["admin@erada.com"],
        "Issue": ["Welcome to the system"],
        "Status": ["Open"],
        "Assignee": ["Abdelrahman Younes"]
    })

# --- الشريط الجانبي (Sidebar) ---
st.sidebar.header("Filters")
# استخراج الأسماء الفريدة من الجدول عشان الفلتر يكون ديناميكي
all_assignees = ["All"] + list(st.session_state.df["Assignee"].unique())
selected_assignee = st.sidebar.selectbox("Filter by Assignee", all_assignees)

# --- قسم إضافة تيكت جديدة ---
with st.expander("➕ Add New Ticket"):
    with st.form("add_ticket_form", clear_on_submit=True):
        email = st.text_input("Your Work Email")
        issue = st.text_area("Describe the issue")
        submitted = st.form_submit_button("Submit")

if submitted and email and issue:
    new_id = f"TICKET-{len(st.session_state.df) + 1001}"
    new_ticket = pd.DataFrame([{
        "ID": new_id,
        "UserEmail": email,
        "Issue": issue,
        "Status": "Open",
        "Assignee": "Abdelrahman Younes"
    }])
    st.session_state.df = pd.concat([new_ticket, st.session_state.df], ignore_index=True)
    st.success(f"Ticket {new_id} submitted successfully!")

# --- عرض الجدول ---
st.header("Existing tickets")
# تطبيق الفلتر
df_display = st.session_state.df
if selected_assignee != "All":
    df_display = df_display[df_display["Assignee"] == selected_assignee]

edited_df = st.data_editor(
    df_display,
    use_container_width=True,
    column_config={
        "Status": st.column_config.SelectboxColumn(options=["Open", "In Progress", "Closed"]),
        "Assignee": st.column_config.SelectboxColumn(options=["Abdelrahman Younes"]) # اسمك هنا
    }
)

# تحديث البيانات الأصلية بعد التعديل
st.session_state.df.update(edited_df)

# --- الإحصائيات ---
st.header("Statistics")
col1, col2 = st.columns(2)
col1.metric("Total Tickets", len(st.session_state.df))
col2.metric("Open Tickets", len(st.session_state.df[st.session_state.df["Status"] == "Open"]))
