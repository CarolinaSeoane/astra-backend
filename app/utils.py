def handle_object_id(_id, convert_id_to_str):
    return str(_id) if convert_id_to_str else _id

def handle_object_ids(ids_list, convert_id_to_str):
    return [str(_id) for _id in list(ids_list)] if convert_id_to_str else list(ids_list)
    
