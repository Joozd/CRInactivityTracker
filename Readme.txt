Clash Royale Activity Tracker, by Joozd.
https://github.com/Joozd/CRInactivityTracker

Needs a valid Clash Royale API key, make your own at https://developer.clashroyale.com/
Then, copy-paste that key into a file called "ClashRoyaleAPIKey.txt" and place with the inactivityFinder.py.

Also, you might want to chang the tag of the clan you wnat to track to another (less cool) one.

Now: how it works:
- Will create a shelve file containing the amount of battles fought, total donations and todays date.
- Next time you run it, it will check if either of those has changed, if so, it will change the shelve accordingly, including date.
- Finally, it will show (print) how long ago it was when any changes were seen by the program. Might want to keep the window open if not running through IDLE.

