import streamlit as st
import logic
import pandas as pd
import db

st.title("Spelare")


left_col ,right_col = st.columns([0.8,0.2])

player_table = left_col.empty()

with right_col.form ("Lägg till spelare",clear_on_submit=True):
    st.write("Lägg till spelare")
    player_name = st.text_input(label="Spelar namn",placeholder="Namn", label_visibility="collapsed")
    submitted = st.form_submit_button(label="Skicka")
    if submitted:
        if player_name != "":
                db.insert_player(player_name)
        else:
            st.error("Lämna inte fälten tomma")
        
with right_col.form("Sök spelare"):
    st.write("Sök Spelare")
    search_player = st.text_input(label="Sök",placeholder="Namn", label_visibility="collapsed")
    submitted = st.form_submit_button(label="Sök")
    if submitted:
         st.rerun()

@st.dialog("Historik", width="large")
def history_dialog(player_id):
     player_match_history_df = pd.DataFrame(logic.get_player_match_history(player_id) ,columns=["Id","Tid","Spelare 1", "Spelare 2", "Set 1", "Set 2", "Set 3", "Vinnare"])
     st.table(player_match_history_df)

with right_col.form("Visa historik"):
    st.write("Visa historik")
    player_id = st.text_input(label="Visa",placeholder="Id", label_visibility="collapsed")
    submitted = st.form_submit_button(label="Visa")
    if submitted:
        if player_id != "":
            history_dialog(int(player_id))
        else:
            st.error("Lämna inte fälten tomma")

players_df = pd.DataFrame(db.get_players(),columns=["Id","Namn"])
players_df_filtered = players_df[players_df['Namn'].str.contains(search_player)]
player_table.table(players_df_filtered)