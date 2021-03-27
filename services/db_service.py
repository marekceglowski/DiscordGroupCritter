from datetime import datetime
from pymongo import MongoClient
from models.submission import Submission
from models.user import User
from models.feedback import Feedback
from models.submission_info import SubmissionInfo
import utils.date_util as date_util
from utils.dict_to_obj import DictToObject
from utils.list_dict_to_obj import ListDictToObj

client = MongoClient('mongodb://localhost:27017')
db = client['lmy']


# General #

def get_max_id(db_table):
    if db_table.count() == 0:
        return 0
    else:
        return DictToObject(list(db_table.find().sort([("created_at", -1)]).limit(1))[0]).id


# Submissions #

def add_submission(message, status="pending"):
    submission = Submission(
        message.id,
        message.author.id,
        message.jump_url,
        date_util.datetime_to_str(datetime.now()),
        status
    )

    db.submissions.insert_one(submission.__dict__)
    return submission


def add_submission_obj(submission):
    if isinstance(submission, Submission):
        db.submissions.insert_one(submission.__dict__)
    return submission


def get_submissions_by_user_id(user_id):
    submissions = db.submissions.find({'user_id': user_id})  # find() returns a cursor
    if submissions.count() < 1:
        return None
    else:
        return ListDictToObj(list(submissions))

def get_submission_by_message_id(message_id):
    submission = db.submissions.find_one({"message_id" : message_id})
    if submission is None:
        return None
    else:
        return DictToObject(submission)

def get_ordered_queue_submissions(not_user_id=None, check_user_feedback_id=None):

    message_ids = []

    if check_user_feedback_id is not None:
        feedback = get_feedbacks_given(check_user_feedback_id)

        if feedback is not None:
            message_ids = [entry.submission_id for entry in feedback]

    submissions = db.submissions.find(
        {
            "status": "pending",
            "user_id": {"$ne": not_user_id},
            "message_id": {"$nin": message_ids},
        }
    ).sort([("created_at", 1)])
    
    if submissions.count() < 1:
        return None
    else:
        return ListDictToObj(list(submissions))


def get_submission_position_in_queue(message_id):
    submission = db.submissions.find_one({'message_id': message_id})
    if submission is None:
        return -1
    else:
        submission = DictToObject(submission)
        queue_subs = get_ordered_queue_submissions()
        if queue_subs is None:
            return -1
        else:
            for idx, item in enumerate(queue_subs):
                if submission.message_id == item.message_id:
                    return idx+1
            return -1


def get_submission_positions_in_queue_multi(submission_list):
    subs_and_positions = []  # list of tuples (submission, queue_pos)

    queue_subs = get_ordered_queue_submissions()
    if queue_subs is None:
        return None
    else:
        for idx, item in enumerate(queue_subs):
            current_pos = -1
            for submission in submission_list:
                if submission.message_id == item.message_id:
                    current_pos = idx
                    subs_and_positions.append((submission, current_pos))
        return subs_and_positions


def get_submissions_with_info_by_user_id(user_id):
    user_sub_infos = []  # list(SubmissionInfo() obj)
    user_subs = get_submissions_by_user_id(user_id)
    user_subs_with_positions = get_submission_positions_in_queue_multi(user_subs)
    feedbacks = db.feedbacks.find({'received_user_id': user_id})
    if feedbacks.count() > 0:
        feedbacks = ListDictToObj(list(feedbacks))

    for user_sub_with_pos in user_subs_with_positions:
        sub_feedbacks = []
        for fb in feedbacks:
            if fb.submission_id == user_sub_with_pos[0].message_id:
                sub_feedbacks.append(fb)
        user_sub_infos.append(SubmissionInfo(
            user_sub_with_pos[0],
            sub_feedbacks,
            user_sub_with_pos[1]
        ))
    return user_sub_infos


def set_submission_complete(submission):

    message_id = submission.message_id
    item_query = {"message_id": message_id}
    update = {"$set": {"status": "complete"}}
    db.submissions.update_one(item_query, update)


# Users #

def user_exists(user_id):
    user = db.users.find_one({'user_id': user_id})
    if user is None:
        return False
    else:
        return True


def get_user_by_author_id(user_id):
    user = db.users.find_one({'user_id': user_id})
    if user is None:
        user = add_new_user(user_id)
        return user
    else:
        return DictToObject(user)


def add_new_user(user_id):
    user = User(
        user_id,
        None  # Lowest level rank
    )
    db.users.insert_one(user.__dict__)
    return user

def user_toggle_feedback_dm(user):
    item_query = {"user_id": user.user_id}
    update = {"$set": {"dm_on_feedback": not(user.dm_on_feedback)}}
    db.users.update_one(item_query, update)
    
# Ranks #

def get_rank_by_user(user_id):
    user = db.users.find_one({'user_id': user_id})
    if user is not None:
        return DictToObject(user).rank_id
    else:
        return None


def get_rank_by_name(name):
    rank = db.ranks.find_one({'rank_name': name})
    if rank is None:
        return None
    return DictToObject(rank)


# Feedbacks #

def add_feedback(message):
    feedback = Feedback(
        message.id,
        message.reference.message_id,
        message.author.id,
        message.reference.resolved.author.id,
        message.jump_url
    )
    db.feedbacks.insert_one(feedback.__dict__)


def get_feedbacks_received(user_id):
    feedbacks = db.feedbacks.find({'received_user_id': user_id})
    if feedbacks.count() < 1:
        return None
    else:
        return ListDictToObj(list(feedbacks))


def get_feedbacks_given(user_id):
    feedbacks = db.feedbacks.find({'user_id': user_id})  # returns a cursor
    if feedbacks.count() < 1:
        return None
    else:
        return ListDictToObj(list(feedbacks))
