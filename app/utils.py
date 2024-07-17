def handle_object_id(_id, convert_id_to_str):
    return str(_id) if convert_id_to_str else _id

def handle_object_ids(teams_list, convert_id_to_str):
    if convert_id_to_str and teams_list:
        for team in teams_list:
            team["team"] = str(team["team"])  
    return teams_list
