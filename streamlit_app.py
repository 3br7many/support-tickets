import streamlit as st
import pandas as pd
from shareplum import Site
from shareplum.auth.ntlm import NtlmSite

# إعدادات الموقع
SITE_URL = "https://netorgft1653627.sharepoint.com/sites/AbdelrahmanYounes"
USERNAME = st.secrets["SHAREPOINT_USERNAME"]
PASSWORD = st.secrets["SHAREPOINT_PASSWORD"]

st.title("🎫 IT Support System - Adaptiv")

with st.form("ticket_form"):
    email = st.text_input("Your Work Email")
    issue = st.text_area("Describe the issue")
    submit = st.form_submit_button("Submit")

if submit:
    try:
        # الاتصال بـ SharePoint
        auth = NtlmSite(SITE_URL, username=USERNAME, password=PASSWORD)
        sp_site = Site(SITE_URL, auth=auth)
        sp_list = sp_site.List('SupportTickets')
        
        # إضافة التيكت
        sp_list.update_list_items([{'Title': issue, 'UserEmail': email, 'Status': 'Open'}], None)
        st.success("Ticket saved! The Flow will now trigger automatically.")
    except Exception as e:
        st.error(f"Error: {e}")
