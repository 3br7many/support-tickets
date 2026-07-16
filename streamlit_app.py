import streamlit as st
import pandas as pd
import numpy as np
import datetime
import requests

st.set_page_config(page_title="IT Support System", page_icon="🎫")
st.title("🎫 IT Support System")

# تهيئة البيانات
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame({
        "ID": [f"TICKET-{i}" for i in range(1100, 1090, -1)],
        "UserEmail": ["user@erada.com"] * 10,
        "Issue": ["Example issue"] * 10,
        "Status": ["Open"] * 10,
        "Assignee": ["Unassigned"] * 10
    })

# Sidebar للفلترة
st.sidebar.header("Filters")
assignee_filter = st.sidebar.selectbox("Filter by Assignee", ["All", "Ahmed", "Mohamed", "Sara", "Unassigned"])

# عرض التيكتس بناءً على الفلتر
df_display = st.session_state.df
if assignee_filter != "All":
    df_display = df_display[df_display["Assignee"] == assignee_filter]

# فورم إضافة تيكت جديدة
with st.form("add_ticket_form"):
    email = st.text_input("Your Work Email")
    issue = st.text_area("Describe the issue")
    submitted = st.form_submit_button("Submit")

if submitted and email:
    new_ticket = {
        "ID": f"TICKET-{int(st.session_state.df.ID.str.split('-').str[1].max()) + 1}",
        "UserEmail": email,
        "Issue": issue,
        "Status": "Open",
        "Assignee": "Unassigned"
    }
    st.session_state.df = pd.concat([pd.DataFrame([new_ticket]), st.session_state.df], axis=0)
    
    # ربط Power Automate (ضع رابط الـ Webhook الخاص بك هنا)
    webhook_url = "https://defaulte2a3de6f89e24f578064e4a0661b86.f9.environment.api.powerplatform.com:443/powerautomate/automations/direct/cu/23/workflows/c88a09eb95dd4ac98dc075a293e4a842/triggers/manual/paths/invoke?api-version=1"
    requests.post(webhook_url, json=new_ticket)
    st.success("Ticket submitted and notification sent!")

# تعديل التيكتس
edited_df = st.data_editor(df_display, use_container_width=True, column_config={
    "Status": st.column_config.SelectboxColumn(options=["Open", "In Progress", "Closed"]),
    "Assignee": st.column_config.SelectboxColumn(options=["Ahmed", "Mohamed", "Sara", "Unassigned"])
})
st.session_state.df.update(edited_df)
