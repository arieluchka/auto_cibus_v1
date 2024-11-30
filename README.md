## Todo
- Add an option to upload csv/exel file with work schedule

[docker image](https://hub.docker.com/repository/docker/arieluchka/auto_cibus/general)


## Logic
User can choose type of job and when to run it.
type1 - daily job. will run every day and check for conditions (sunday-thursday/working day/not sick day). could also run by calendar (only days of month the user specified)

type2 - monthly job to finish all remaining money. (job will run at the last day of each month/at the last workday of each month). job will check remaining cibus money and use it all in wolt giftcards/cibus super gift cards

---

USERS_PATH - path to where user config files are stored
