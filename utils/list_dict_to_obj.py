from utils.dict_to_obj import DictToObject


def ListDictToObj(list_of_dict):
    list_of_obj = []
    for dict in list_of_dict:
        list_of_obj.append(DictToObject(dict))
    return list_of_obj
