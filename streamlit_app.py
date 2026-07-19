import streamlit as st
import requests
import msal

# إعدادات الربط من الـ Secrets
client_id = st.secrets["AZURE_CLIENT_ID"]
client_secret = st.secrets["AZURE_CLIENT_SECRET"]
tenant_id = st.secrets["AZURE_TENANT_ID"]
site_id = st.secrets["SHAREPOINT_SITE_ID"]
list_id = st.secrets["SHAREPOINT_LIST_ID"]

# إعداد الـ Authentication
authority = f"https://login.microsoftonline.com/{tenant_id}"
scope = ["https://graph.microsoft.com/.default"]

app = msal.ConfidentialClientApplication(
    client_id, 
    authority=authority, 
    client_credential=client_secret
)

# واجهة التطبيق
st.title("Adaptiv IT Support System")

issue = st.text_input("Issue Title")
user_email = st.text_input("Your Email")
description = st.text_area("Description")

if st.button("Submit Ticket"):
    token_response = app.acquire_token_for_client(scopes=scope)
    
    if "access_token" in token_response:
        token = token_response["access_token"]
        url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{list_id}/items"
        
        headers = {
            "Authorization": f"Bearer {token}", 
            "Content-Type": "application/json"
        }
        
        # ربط البيانات بالأعمدة الموجودة في SharePoint
        payload = {
            "fields": {
                "Title": issue,         # هذا الحقل إجباري في SharePoint
                "Issue": issue,         # العمود المخصص في الـ List
                "UserEmail": user_email,
                "Description": description,
                "Status": "Open"        # حالة افتراضية للتيكت الجديد
            }
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 201:
            st.success("Ticket saved to SharePoint successfully!")
        else:
            st.error(f"Error: {response.json()}")
    else:
        st.error("Authentication failed. Check your Secrets.")
