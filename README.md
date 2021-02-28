# GroupCritter (for LMY Patreon)

This is a discord bot that will assist with doing group crits as well as tracking feedback in the LMY Patreon channel `#group-crit-submissions`.

The GroupCritter bot will add the following features:
- A submission queue system  -- to make it easier for @la_meme_young to find submissions in order among the chat
- A feedback tracking system -- any replies to a submission count as "feedback", you can track your submissions and feedbacks given/received with a single command
- A leveling system -- giving lots of feedback to others will level you up! Levels will unlock colors for your discord username and award you with medal emojis

Other features include:
- Ping the user when their livestream crit is next
- Ping the user when their submission was given feedback
- Post milestone announcements when people level up a certain amount

Commands:

- `!add <text>` - adds a new submission to the group crit queue
- `!addskip <text>` - adds a new submission with status 'skip' so it's not in the livestream queue
- `!count` - counts the number of submissions currently in the queue
- `!crit random` - sends you a random submission from the queue to critique (always returns a submission you haven't reviewed)
- `!crit next` - sends you the next submission from the the queue to critique (doesn't shift the queue position, useful if you want to do them in order)
- `!feedback [given|received|both]` - displays feedback you have given, received, or both
- `!stats` - displays your level and how much feedback you have given
- `!submissions` - displays your crit submissions and feedback received

Admin Commands:

- `!next` - moves the queue up one spot and displays a link to the submission
- `!info` - shows a list of all feedback given to the current queue submission

Database Structure can be found here:

https://github.com/marekceglowski/DiscordGroupCritter/blob/master/DB_INFO.md

Medal Ranking rules and commands can be found here:

https://github.com/marekceglowski/DiscordGroupCritter/blob/master/medals/MEDALS.md

Proposed Bot Permissions:

https://images2.imgbox.com/81/fe/mXucvb4t_o.png

