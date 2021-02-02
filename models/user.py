class User:
    def __init__(self, user_id, rank_id):
        self.user_id = user_id  # PK discord's user id
        self.rank_id = rank_id  # FK ranks.id
