import os
from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
import numpy as np
import pandas as pd
import data_process
from datetime import datetime
import floods


app = Flask(__name__)


def update_metadata():

    urls = {'Malaysia': 'https://reliefweb.int/updates?advanced-search=%28PC147%29_%28DT4611%29',
            'Philippines': 'https://reliefweb.int/updates?advanced-search=%28C188%29_%28DT4611%29',
            'Indonesia': 'https://reliefweb.int/updates?advanced-search=%28PC120%29_%28DT4611%29'}

    floods.update_reliefweb(urls)
    logdownload()
    return 0


def logdownload():
    # log everytime a job is done
    with open("metadata/logtime.txt", "a") as myfile:
        myfile.write("TIME: {} \n".format(datetime.now()))
    print("Logged!")


def sensor():
    """ Function for test purposes. """
    with open("static/time-log.txt", "w") as myfile:
        myfile.write("TIME: {}".format(np.random.randint(10)))
    print("Scheduler is alive!")


def save_latest_frequencies():
    df = data_process.count_article_daily_freq(pd.read_pickle('flood_dat.pickle'))
    df.to_csv('static/news_frequencies.csv')
    print('Saving news frequencies')


@app.route("/")
def hello_world():
    name = os.environ.get("NAME", "World")

    return render_template('index.html')


if __name__ == "__main__":

    sensor()
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(sensor, 'interval', seconds=2)
    sched.add_job(logdownload, 'interval', seconds=10)
    sched.add_job(update_metadata, 'interval', seconds=10*60)

    sched.start()

    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 9090)))
