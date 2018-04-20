#!/usr/bin/env python
import sqlite3
import time
import datetime
from flask import Flask, render_template, Response, url_for, request
import picamera 

app = Flask(__name__)
 
@app.route("/", methods=['GET','POST'])
def main():
    return render_template('test.html')

@app.route("/takePic", methods=['GET','POST'])
def takePic():
    # connect to picture database
    try:
        db = sqlite3.connect('/home/pi/ELSpring2018/code/pics.db')
        cursor = db.cursor()
        currentTime=time.strftime('%x %X %Z') 

        # take new photo
        camera = picamera.PiCamera()
        pic = camera.capture('static/pic3.jpg')
        picPath = "static/pic3.jpg"
        # store new photo in database
        cursor.execute('''INSERT INTO pics(picPath, datetime)
                  VALUES(?,?)''', (picPath, currentTime))
        db.commit()

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

    return render_template('test.html')

# method to display all pics taken so far
@app.route("/showPics")
def showPics():
   # if request.method == 'POST':
        db = sqlite3.connect('/home/pi/ELSpring2018/code/pics.db')
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM pics''')
        rows = cursor.fetchall();
        db.close()
        return render_template('showPics.html',rows = rows)
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
