from datetime import datetime


def datetime_to_str(datetime):
    return datetime.strftime("%Y-%m-%d %H:%M:%S")


def str_to_datetime(str):
    return datetime.strptime(str, "%Y-%m-%d %H:%M:%S")
