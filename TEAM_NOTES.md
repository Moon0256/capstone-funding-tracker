# Team notes

Notes from our team.

- **Moon:** I asked my AI to add an Urgency column with Overdue / Due today / Due in N days labels. It found `days_left()` was off by one (today gave -1), so we fixed it and added tests for yesterday, today and tomorrow. Then I checked every label on the page against the deadlines and ran `python -m pytest` (7 passed).
