import streamlit as st
import pandas as pd
import logic
import db

st.set_page_config(page_title="Easy Score", layout="wide")

db.init_db()

left_col, middle_col, right_col = st.columns([0.5,0.3,0.2])

left_col.title("Kommande Matcher")
matches_table = left_col.empty()

middle_col.title("Ranking")
ranking_table = middle_col.empty()

with right_col.form ("Lägg till set", clear_on_submit=True):
    st.write("Lägg till resultat (Spelare 1 först)")
    match_id = st.text_input(label="Match id", placeholder="Id")
    st.write("Set 1")
    set1_p1 = st.number_input(label="Spelare 1 Gem Set 1",step=1, max_value=6, min_value=0, label_visibility="collapsed")
    set1_p2 = st.number_input(label="Spelare 2 Gem Set 1",step=1, max_value=6, min_value=0, label_visibility="collapsed")
    st.write("Set 2")
    set2_p1 = st.number_input(label="Spelare 1 Gem Set 2",step=1, max_value=6, min_value=0, label_visibility="collapsed")
    set2_p2 = st.number_input(label="Spelare 2 Gem Set 2",step=1, max_value=6, min_value=0, label_visibility="collapsed")
    st.write("Set 3")
    set3_p1 = st.number_input(label="Spelare 1 Gem ",step=1, max_value=6, min_value=0, label_visibility="collapsed")
    set3_p2 = st.number_input(label="Spelare 2 Gem",step=1, max_value=6, min_value=0, label_visibility="collapsed")
    submitted = st.form_submit_button(label="Skicka")
    if submitted:
        if match_id != "":
            if int(match_id) in logic.get_uncompleted_matches_id():
                db.insert_match_set(match_id, set1_p1, set1_p2, set2_p1, set2_p2, set3_p1, set3_p2)
            else:
                st.error("Finns ingen match med det id")
        else:
            st.error("Lämna inte fälten tomma")

uncompleted_matches_df = pd.DataFrame(db.get_uncompleted_matches(), columns=["Id", "Tid/Datum", "Spelare 1", "Spelare 2"])
matches_table.table(uncompleted_matches_df)

completed_matches_and_results_list = logic.get_completed_matches_and_results()
ranking_df = pd.DataFrame(logic.get_ranking(completed_matches_and_results_list), columns=["Spelare", "Vinster"])
ranking_df.index.name = "Placering"
ranking_df.index += 1
ranking_df.reset_index(inplace=True)

ranking_table.table(ranking_df)