import db
import collections

def get_match_results(completed_matches):
    match_results = []
    for i in range(len(completed_matches)):
        get_sets_for_match = db.get_sets_for_match(completed_matches[i][0])
        match_results.append([])
        for j in range(len(get_sets_for_match)):
            result = str(get_sets_for_match[j][1]) + " - " + str(get_sets_for_match[j][2])
            match_results[i].append(result)
    return match_results



def get_winner(match_result, match_info):
    p1_score = 0
    p2_score = 0
    winner = []
    for j in range(len(match_result)):
        if int(match_result[j][:1]) > int(match_result[j][3:]):
            p1_score += 1
        else:
            p2_score += 1
    if p1_score > p2_score:
        winner.append(match_info[2])
    else:
        winner.append(match_info[3])
    return winner

def get_completed_matches_and_results():
    completed_matches = db.get_completed_matches()
    match_results = get_match_results(completed_matches)
    completed_matches_and_results_list = []

    for i in range(len(completed_matches)):
        match_info = list(completed_matches[i])
        match_result = match_results[i]
        winner = get_winner(match_result, match_info)

        completed_matches_and_results_list.append(match_info + match_result + winner)

    return completed_matches_and_results_list

def get_ranking(completed_matches_and_results_list):
    ranking = []
    for i in range(len(completed_matches_and_results_list)):
        ranking.append(completed_matches_and_results_list[i][7])
    return collections.Counter(ranking).most_common()

def get_uncompleted_matches_id():
    uncompleted_matches_id = []
    uncompleted_matches = db.get_uncompleted_matches()

    for i in range(len(uncompleted_matches)):
        uncompleted_matches_id.append(uncompleted_matches[i][0])
    return uncompleted_matches_id

def get_player_id():
    player_id = []

    for i in range(len(db.get_players())):
        player_id.append(db.get_players()[i][0])
    return player_id

def get_player_match_history(player_id):
    player_match_history = []
    completed_matches_and_results = get_completed_matches_and_results()
    player_name_from_id = db.get_player_name_from_id(player_id)

    for i in range(len(completed_matches_and_results)):
        if completed_matches_and_results[i][2] == player_name_from_id[0][0]:
            player_match_history.append(completed_matches_and_results[i])
    return player_match_history
