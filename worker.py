import sched, time
from sqlalchemy.orm import Session
from mydb import get_db, mark_expired_keys_inactive, sweep_expired_keys

s = sched.scheduler(time.time, time.sleep)

def endAPIsession():
  db: Session = get_db()
  mark_expired_keys_inactive(db)
  sweep_expired_keys(db)

# Calculate the number of seconds in a month (approximated to 30 days)
seconds_in_month = 30 * 24 * 60 * 60  # 30 days * 24 hours * 60 minutes * 60 seconds

# Set up the task to run every month (approximated to 30 days)
s.enter(seconds_in_month, 1, endAPIsession)

# Start the scheduler
s.run()