# MongoDB Database Structure:

## submissions
- id [PK]
- message_id -- message id from discord
- user_id [FK]
- jump_url
- created_at
- status -- queue status: options are 'pending', 'complete', or 'skip'

## users
- id [PK]
- discord_user_id -- (the id from discord)
- completed_crits
- queue_pos -- default: 1, crit next command will bump, admin next command may de-bump
- rank_id [FK] -- default: 1, this will be the lowest possible rank

## ranks
- id [PK]
- rank_name
- feedback_count -- number of feedbacks to reach rank
- medal_code -- the medal emoji code (eg. :23:)
- color -- will contain color (not sure how to format yet)

## feedbacks
- id [PK]
- message_id
- submission_id [FK]
- user_id [FK] -- user id of the person that sent feedback
- received_user_id [FK] -- user id of the person that received feedback 
- jump_url
