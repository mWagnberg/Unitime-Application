import json
import os
import requests
import sqlite3
import time

db = sqlite3.connect(os.path.curdir + '/unitime2.db')
cu = db.cursor()

cu.execute("DROP TABLE if EXISTS Courses")
cu.execute("""CREATE TABLE Courses (
                course_code TEXT,
                semester TEXT,
                course_language TEXT,
                course_location TEXT,
                name_en TEXT,
                course_url TEXT)""")

cu.execute("DROP TABLE if EXISTS Schedules")
cu.execute("""CREATE TABLE Schedules (
                course TEXT,
                semester TEXT,
                start_time TEXT,
                end_time TEXT,
                date TEXT,
                room TEXT,
                type TEXT,
                teacher TEXT)""")

cu.execute("DROP TABLE if EXISTS Rooms")
cu.execute("""CREATE TABLE Rooms (
                room_code TEXT,
                building TEXT,
                floor INTEGER,
                longitude REAL,
                lattitude REAL,
                city TEXT)""")

start_time = time.time()
courses = requests.get('http://127.0.0.1:8000/api/course/')
length = 0
for obj in courses.json():
    length += 1
    print(length)
    cu.execute("""INSERT INTO Courses(course_code, semester, course_language,
               course_location, name_en, course_url) VALUES(?,?,?,?,?,?)""",
               (obj['course_code'], obj['semester'], obj['course_language'],
                obj['course_location'], obj['name_en'], obj['url']))
    schedule = requests.get('http://127.0.0.1:8000/api/event/' + obj['course_code'] + '/')
    if (schedule.text is not ''):
        for event in schedule.json():
            
            cu.execute("""INSERT OR IGNORE INTO Schedules(course, semester, start_time,
                   end_time, date, room, type, teacher) VALUES(?,?,?,?,?,?,?,?)""",
                       (obj['course_code'], obj['semester'], event['starttime'], event['endtime'],
                        event['startdate'], event['room'],
                        event['info'], event['teacher']))
            
            if event['room'] is not '':
                split = event['room'].split(',')
                for room in split:
                    rooms = requests.post('http://127.0.0.1:8000/api/room/', data={'room': room})
                    if(rooms.text is not '' and rooms.ok):
                        for room in rooms.json():
                            cu.execute("""INSERT OR IGNORE INTO Rooms(room_code, building, floor,
                                           longitude, lattitude, city) VALUES(?,?,?,?,?,?)""",
                                           (room['name'], 'Building ' + room['name'][:1], room['floor'],
                                            room['lon'], room['lat'], room['city']))
    
print((time.time() - start_time)/60)
db.commit()
db.close

