import streamlit as st
import pandas as pd
import altair as alt

# إعداد الصفحة
st.set_page_config(page_title="IT Support System", page_icon="🎫", layout="wide")
st.title("🎫 IT Support System - Adaptiv")

# تهيئة جدول فارغ تماماً (لا توجد أي بيانات مسبقة)
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["ID", "UserEmail", "Issue", "Status", "Assignee"])

# --- الشريط الجانبي (Sidebar) ---
st.sidebar.header("Filters")
# استخراج الأسماء ديناميكياً
assignee_list = ["All", "Abdelrahman Younes", "Unassigned"]
selected_assignee = st.sidebar.selectbox("Filter by Assignee", assignee_list)

# --- قسم إضافة تيكت جديدة ---
with st.expander("➕ Add New Ticket"):
    with st.form("add_ticket_form", clear_on_submit=True):
        email = st.text_input("Your Work Email")
        issue = st.text_area("Describe the issue")
        assignee = st.selectbox("Assign to", ["Abdelrahman Younes", "Unassigned"])
        submitted = st.form_submit_button("Submit")

if submitted and email and issue:
    new_id = f"TICKET-{len(st.session_state.df) + 1001}"
    new_ticket = pd.DataFrame([{
        "ID": new_id,
        "UserEmail": email,
        "Issue": issue,
        "Status": "Open",
        "Assignee": assignee
    }])
    st.session_state.df = pd.concat([new_ticket, st.session_state.df], ignore_index=True)
    st.success(f"Ticket {new_id} added successfully!")
    st.rerun()

# --- عرض الجدول ---
st.header("Existing tickets")
df_display = st.session_state.df

# تطبيق الفلتر
if selected_assignee != "All":
    df_display = df_display[df_display["Assignee"] == selected_assignee]

# عرض الجدول مع إمكانية التعديل
edited_df = st.data_editor(
    df_display, 
    use_container_width=True,
    column_config={
        "Status": st.column_config.SelectboxColumn(options=["Open", "In Progress", "Closed"]),
        "Assignee": st.column_config.SelectboxColumn(options=["Abdelrahman Younes", "Unassigned"])
    }
)
st.session_state.df.update(edited_df)

# --- الإحصائيات والجرافس ---
st.header("Statistics")
if not st.session_state.df.empty:
    col1, col2 = st.columns(2)
    col1.metric("Total Tickets", len(st.session_state.df))
    col2.metric("Open Tickets", len(st.session_state.df[st.session_state.df["Status"] == "Open"]))

    # جراف الحالة (Status Chart) - شكل احترافي
    st.write("### Ticket Status Overview")
    chart_data = st.session_state.df["Status"].value_counts().reset_index()
    chart_data.columns = ["Status", "Count"]
    
    chart = alt.Chart(chart_data).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
        x=alt.X("Status", sort="-y"),
        y="Count",
        color="Status",
        tooltip=["Status", "Count"]
    ).properties(height=300)
    
    st.altair_chart(chart, use_container_width=True)
else:
    st.info("No tickets to display yet. Add your first ticket to get started!")
