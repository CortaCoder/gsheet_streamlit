import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect

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

sheet_url = st.secrets["private_gsheets_url"]
print(sheet_url)
rows = run_query(f'SELECT * FROM "{sheet_url}"')

# Print results.
if len(rows)>1:
    for row in rows:
        st.write(row)
        st.write(f"Log folder - {row.folder_name} has a file '{row.file_name}'")
else:
    st.write(rows[0])
