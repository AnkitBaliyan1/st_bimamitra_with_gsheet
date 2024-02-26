import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date, datetime

def udpate_database(user, query, prompt ,response, rating="NA"):

    rating = submit_rating(query, response)
    print("rating is:",rating)

    # if rating != "NA" and rating is not None:
    # with st.spinner("in progress"):
    conn = st.connection("gsheets", type=GSheetsConnection)
    worksheet = "bimamitra"

    existing_data = conn.read(worksheet=worksheet, usecols = list(range(7)), ttl=5)


    today_date = date.today().strftime("%Y-%m-%d")
    time_now = datetime.now().strftime("%H:%M:%S")

    tem_df = pd.DataFrame(
        {
            "date": [today_date],
            "time": [time_now],
            "username": [user],
            "query": [query],
            "prompt": [prompt],
            "response": [response],
            "rating": [rating],
        }
    )

    tem_df.columns = existing_data.columns

    updated_data = pd.concat([tem_df,existing_data], ignore_index=True)

    conn.update(worksheet=worksheet, data=updated_data)

    return("Successfully updated")

