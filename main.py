import os
from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
import numpy as np


app = Flask(__name__)

def sensor():
    """ Function for test purposes. """
    with open("static/time-log.txt", "w") as myfile:
        myfile.write("TIME: {}".format(np.random.randint(10)))
    print("Scheduler is alive!")


@app.route("/")
def hello_world():
    name = os.environ.get("NAME", "World")

    return render_template('index.html')


if __name__ == "__main__":
    sensor()
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(sensor, 'interval', seconds=2)
    sched.start()

    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
