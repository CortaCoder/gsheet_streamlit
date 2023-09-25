from google.oauth2 import service_account
from gsheetsdb import connect
from pandas import json_normalize
import pandas as pd
import streamlit as st

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)

# Perform SQL query on the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
def run_query(query):
    try:
        rows = conn.execute(query, headers=1)
        rows = rows.fetchall()
        print(rows)
    except Exception as e:
        return [str(e),]
    return rows

st.header("Import Google Sheet Data")
st.write("Give 'gstreamli@streamlitsheetdemo.iam.gserviceaccount.com' viewer access to your google sheet to get started")

gsheet_form = st.form("gsheet_apply")
sheet_url = gsheet_form.text_input("Google Sheet URL")
submit = gsheet_form.form_submit_button()

rows = ["Enter a sheet url to get started",]

if submit:
    rows = run_query(f'SELECT * FROM "{sheet_url}"')
    # Keys = rows[0].keys()


st.write("<hr>",unsafe_allow_html=True)
# Print results.
if len(rows)>1:
    df_sheet = pd.json_normalize(rows, orient = 'index')
    st.write(df_sheet)
    st.write(rows)
    # for row in rows:
    #     st.write(row)
        # st.write(f"Log folder - {row.folder_name} has a file '{row.file_name}'")
else:
    st.write(rows[0])
