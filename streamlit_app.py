import streamlit as st
import requests
import msal

# 1. إعدادات الربط من الـ Secrets
client_id = st.secrets["AZURE_CLIENT_ID"].strip()
client_secret = st.secrets["AZURE_CLIENT_SECRET"].strip()
tenant_id = st.secrets["AZURE_TENANT_ID"].strip()
site_id = st.secrets["SHAREPOINT_SITE_ID"].strip()
list_id = st.secrets["SHAREPOINT_LIST_ID"].strip()

# 2. إعداد الـ Authentication - تم تعديل الـ Authority ليكون الرابط القياسي المباشر
# بدلاً من استخدام f-string قد يحتوي على مسافات، نستخدم الرابط بشكل صريح
authority = f"https://login.microsoftonline.com/{tenant_id}"
scope = ["https://graph.microsoft.com/.default"]

try:
    app = msal.ConfidentialClientApplication(
        client_id, 
        authority=authority, 
        client_credential=client_secret
    )
except Exception as e:
    st.error(f"Error initializing MSAL: {e}")
    st.stop()

# 3. واجهة التطبيق
st.title("Adaptiv IT Support System")

issue = st.text_input("Issue Title")
user_email = st.text_input("Your Email")
description = st.text_area("Description")

if st.button("Submit Ticket"):
    # محاولة الحصول على الـ Token
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
                "Title": issue,
                "Issue": issue,
                "UserEmail": user_email,
                "Description": description,
                "Status": "Open"
            }
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 201:
            st.success("Ticket saved to SharePoint successfully!")
        else:
            st.error(f"Error: {response.text}")
    else:
        error_msg = token_response.get("error_description", "Unknown error")
        st.error(f"Authentication failed: {error_msg}")
