# DiscordGroupCritter

This is a discord bot that will assist with doing group crits as well as tracking feedback in the LMY Patreon channel `#group-crit-submissions`.

GroupCritter lets users keep track of their own submissions and feedback they have recieved and given. Anytime a submission is replied to using Discord's "reply" option, that will count as feedback.

Commands:

- `!add <text>` - adds a new submission to the queue
- `!count` - counts the number of submissions currently in the queue
- `!check` - lists all of your submissions and all feedback recieved
- `!crit random` - sends you a random submission from the queue to critique

Admin Commands:

- TBD
- These commands will help Max with doing the livestream group crits.

TinyDB Database Structure:

```
submissions
- id
- user_id
- jump_url
- created_at

feedback
- id
- submission_id
- user_id
- jump_url

crit_stats
- user_id
- completed_crits
- queue_pos

completed_crits
- user_id
- submission_id
```
