import streamlit as st
import pandas as pd
import altair as alt
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.listitems.listitem_creation_information import ListItemCreationInformation

# إعداد الصفحة
st.set_page_config(page_title="IT Support System", page_icon="🎫", layout="wide")
st.title("🎫 IT Support System - Adaptiv")

# إعدادات الشير بوينت من الـ Secrets
SITE_URL = st.secrets["SHAREPOINT_URL"]
USERNAME = st.secrets["SHAREPOINT_USERNAME"]
PASSWORD = st.secrets["SHAREPOINT_PASSWORD"]
LIST_NAME = "SupportTickets"

# دالة الحفظ في SharePoint
def save_to_sharepoint(email, issue, assignee):
    credentials = UserCredential(USERNAME, PASSWORD)
    ctx = ClientContext(SITE_URL).with_credentials(credentials)
    
    list_obj = ctx.web.lists.get_by_title(LIST_NAME)
    
    # إضافة عنصر جديد باستخدام التنسيق الصحيح للمكتبة
    item = list_obj.add_item(ListItemCreationInformation())
    item.set_property("Title", issue)
    item.set_property("UserEmail", email)
    item.set_property("Assignee", assignee)
    item.set_property("Status", "Open")
    item.update()
    ctx.execute_query()

# تهيئة جدول البيانات في الجلسة
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["UserEmail", "Issue", "Status", "Assignee"])

# --- الشريط الجانبي ---
st.sidebar.header("Filters")
selected_assignee = st.sidebar.selectbox("Filter by Assignee", ["All", "Abdelrahman Younes", "Unassigned"])

# --- قسم إضافة تيكت ---
with st.expander("➕ Add New Ticket"):
    with st.form("add_ticket_form", clear_on_submit=True):
        email = st.text_input("Your Work Email")
        issue = st.text_area("Describe the issue")
        assignee = st.selectbox("Assign to", ["Abdelrahman Younes", "Unassigned"])
        submitted = st.form_submit_button("Submit")

if submitted and email and issue:
    with st.spinner("Saving to SharePoint..."):
        try:
            save_to_sharepoint(email, issue, assignee)
            new_ticket = pd.DataFrame([{"UserEmail": email, "Issue": issue, "Status": "Open", "Assignee": assignee}])
            st.session_state.df = pd.concat([new_ticket, st.session_state.df], ignore_index=True)
            st.success("Ticket saved successfully to SharePoint!")
        except Exception as e:
            st.error(f"Error: {e}")

# --- عرض الجدول ---
st.header("Existing tickets")
df_display = st.session_state.df
if selected_assignee != "All":
    df_display = df_display[df_display["Assignee"] == selected_assignee]
st.data_editor(df_display, use_container_width=True)

# --- الإحصائيات ---
st.header("Statistics")
if not st.session_state.df.empty:
    col1, col2 = st.columns(2)
    col1.metric("Total Tickets", len(st.session_state.df))
    col2.metric("Open Tickets", len(st.session_state.df[st.session_state.df["Status"] == "Open"]))
    
    chart = alt.Chart(st.session_state.df["Status"].value_counts().reset_index()).mark_bar().encode(
        x="Status", y="count()", color="Status"
    )
    st.altair_chart(chart, use_container_width=True)
