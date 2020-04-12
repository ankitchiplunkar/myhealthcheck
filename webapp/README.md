# Webapp to check health of user
We use Euler Video Magnification to detect slight changes in the video to predict approximate health metrics.  

Inspired by: https://www.youtube.com/watch?v=EhZXDgG9oSk

# Local Setup

NOTE: The webapp currently only works locally on Firefow

0. Clone and enter the repo on your local machine
1. Create a virtual enviornment with `python3.7`
2. Install the required dependencies `pip install -r requirements.txt`
4. Run the webserver via `gunicorn -k eventlet -w 1 app:app --log-file=-`

# Demo:
Check out: https://myhealthcheck.uc.r.appspot.com/