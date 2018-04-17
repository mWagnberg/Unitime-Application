import json
import os
import requests
import sqlite3
import time

db = sqlite3.connect(os.path.curdir + '/unitime.db')
cu = db.cursor()


cu.execute("PRAGMA foreign_keys=ON")
cu.execute("PRAGMA synchronous=OFF")

cu.execute("""CREATE TABLE Courses (
                course_code TEXT NOT NULL,
                semester TEXT NOT NULL,
                course_language TEXT,
                course_location TEXT,
                name_en TEXT NOT NULL,
                course_url TEXT,
                PRIMARY KEY (course_code, semester))""")


cu.execute("""CREATE TABLE Rooms (
                room_code TEXT UNIQUE,
                building TEXT,
                floor INTEGER,
                longitude REAL,
                lattitude REAL,
                city TEXT,
                PRIMARY KEY (room_code))""")


cu.execute("""CREATE TABLE Schedules (
                course TEXT NOT NULL,
                semester TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                date TEXT NOT NULL,
                room TEXT NOT NULL,
                type TEXT,
                teacher TEXT,
                FOREIGN KEY(course, semester) REFERENCES Courses(course_code, semester),
                FOREIGN KEY(room) REFERENCES Rooms(room_code),
                PRIMARY KEY (course, semester, date, start_time, room))""")


start_time = time.time()

print("starting populating the database")
#Get all courses from the API
courses = requests.get('http://127.0.0.1:8000/api/course/')
for obj in courses.json():
    cu.execute("""INSERT INTO Courses(course_code, semester, course_language,
               course_location, name_en, course_url) VALUES(?,?,?,?,?,?)""",
               (obj['course_code'], obj['semester'], obj['course_language'],
                obj['course_location'], obj['name_en'], obj['url']))

    schedule = requests.get('http://127.0.0.1:8000/api/event/' + obj['course_code'] + '/')
    
    #Check if we get any schedule back from the request
    if (schedule.text is not ''):

        #For each of these events we want to get its rooms
        for event in schedule.json():

            #if the schedules room is empty we skip this, else we check each of the rooms ( can be comma seperated )
            if event['room'] is '':

                # add the schedule but with empty room as we dont know the room yet.
                cu.execute("""INSERT OR IGNORE INTO Schedules(course, semester, start_time,
                            end_time, date, room, type, teacher) VALUES(?,?,?,?,?,?,?,?)""",
                            (obj['course_code'], obj['semester'], event['starttime'], event['endtime'],
                            event['startdate'], '' , event['info'], event['teacher']))

            else:
                
                #We split the rooms on "," so if we have more then one room we get that as a list
                split = event['room'].split(',')

                #for each of the rooms in our split list we call the API for that room
                for room in split:
                       
                    rooms = requests.post('http://127.0.0.1:8000/api/room/', data={'room': room})

                    #if the API gives us a empty list or an 404 we add the schedule but with an empty room
                    if(rooms.text is '' or not rooms.ok):
                        
                        # need to insert a empty room for the foreign key
                        cu.execute("""INSERT OR IGNORE INTO Rooms(room_code, building, floor,
                                           longitude, lattitude, city) VALUES(?,?,?,?,?,?)""",
                                           ('', '','','','',''))
                         
                        cu.execute("""INSERT OR IGNORE INTO Schedules(course, semester, start_time,
                                            end_time, date, room, type, teacher) VALUES(?,?,?,?,?,?,?,?)""",
                                            (obj['course_code'], obj['semester'], event['starttime'], event['endtime'],
                                            event['startdate'], '', event['info'], event['teacher']))
                    else:
                        #if we get more then one room from a query we insert both
                        for room in rooms.json():
                            
                            cu.execute("""INSERT OR IGNORE INTO Rooms(room_code, building, floor,
                                           longitude, lattitude, city) VALUES(?,?,?,?,?,?)""",
                                           (room['name'], 'Building ' + room['name'][:1], room['floor'],
                                            room['lon'], room['lat'], room['city']))

                            cu.execute("""INSERT OR IGNORE INTO Schedules(course, semester, start_time,
                                            end_time, date, room, type, teacher) VALUES(?,?,?,?,?,?,?,?)""",
                                            (obj['course_code'], obj['semester'], event['starttime'], event['endtime'],
                                            event['startdate'], room['name'], event['info'], event['teacher']))
                            
                            
print("Done populated the database" + str((time.time() - start_time)/60))
db.commit()
db.close

