import streamlit as st
import pandas as pd
import logic
import db


st.title("Färdiga Matcher")

left_col,right_col = st.columns([0.8,0.2])

matches_table = left_col.empty()

with right_col.form ("Lägg till match",clear_on_submit=True):
    st.write("Lägg till Match")
    player1_id = st.text_input(label="Spelare 1",placeholder="Id")
    player2_id = st.text_input(label="Spelare 2",placeholder="Id")
    time = st.datetime_input(label="Tid/datum")
    submitted = st.form_submit_button(label="Skicka")
    if submitted:
        if player1_id != "" and player2_id != "":
            if player1_id != player2_id:
                if int(player1_id) in logic.get_player_id() and int(player2_id) in logic.get_player_id():
                    db.insert_match(player1_id, player2_id, time)
                else:
                    st.error("En eller flera av spelarna finns inte")
            else:
                st.error("Spelarnas id måste vara olika")
        else:
            st.error("Lämna inte fälten tomma")

completed_matches_and_results_list = logic.get_completed_matches_and_results()
completed_matches_and_results_df = pd.DataFrame(completed_matches_and_results_list, columns=["Id","Tid","Spelare 1", "Spelare 2", "Set 1", "Set 2", "Set 3", "Vinnare"])
left_col.table(completed_matches_and_results_df)