import streamlit as st
import pandas as pd

st.set_page_config(page_title="IT Support System", layout="wide")
st.title("🎫 IT Support System - Adaptiv")

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["UserEmail", "Issue", "Status"])

with st.expander("➕ Add New Ticket"):
    with st.form("ticket_form", clear_on_submit=True):
        email = st.text_input("Your Work Email")
        issue = st.text_area("Describe the issue")
        submit = st.form_submit_button("Submit")

if submit and email and issue:
    new_row = pd.DataFrame([{"UserEmail": email, "Issue": issue, "Status": "Open"}])
    st.session_state.df = pd.concat([new_row, st.session_state.df], ignore_index=True)
    st.success("Ticket added locally! (Integration with SharePoint pending IT approval)")

st.header("Existing tickets")
st.table(st.session_state.df)

# زر لتحميل البيانات كـ Excel لإرسالها للـ IT
csv = st.session_state.df.to_csv(index=False)
st.download_button("Download Tickets as CSV", data=csv, file_name="tickets.csv", mime="text/csv")
