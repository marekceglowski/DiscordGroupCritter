class User:
    def __init__(self, id, discord_user_id, completed_crits, queue_pos, rank_id):
        self.id = id
        self.discord_user_id = discord_user_id
        self.completed_crits = completed_crits
        self.queue_pos = queue_pos
        self.rank_id = rank_id  # FK ranks.id
