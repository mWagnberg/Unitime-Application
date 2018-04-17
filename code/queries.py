import os
import sqlite3
import pprint as pp

db = sqlite3.connect(os.path.curdir + '/unitime.db')
cu = db.cursor()

def search_for_course( cursor, course ):
    cursor.execute("SELECT * FROM Courses WHERE course_code = :course", {'course': course})
    rows = cursor.fetchall()
    pp.pprint(rows)

def search_for_schedule( cursor, course, semester ):
    cursor.execute("SELECT * FROM Schedules WHERE course = :course AND semester = :semester" , {'course': course, 'semester': semester})
    rows = cursor.fetchall()
    pp.pprint(rows)

def search_for_a_room( cursor, room ):
    cursor.execute("SELECT * FROM Rooms WHERE room_code LIKE :room" , {'room': '%' + room + '%'})
    rows = cursor.fetchall()
    pp.pprint(rows)

def search_schedule_for_a_room( cursor, room ):
    cursor.execute("SELECT * FROM Schedules WHERE room LIKE :room" , {'room': '%' + room + '%'})
    rows = cursor.fetchall()
    pp.pprint(rows)

def search_schedule_for_a_room_on_date( cursor, room, date ):
    cursor.execute("SELECT * FROM Schedules WHERE room LIKE :room AND date = :date"  , {'room': '%' + room + '%', 'date': date})
    rows = cursor.fetchall()
    pp.pprint(rows)

def search_schedule_for_a_teacher( cursor, teacher ):
    cursor.execute("SELECT * FROM Schedules WHERE teacher = :teacher", {'teacher': teacher})
    rows = cursor.fetchall()
    pp.pprint(rows)


#search_for_course(cu, '1DV701')
#search_for_schedule(cu, '1DV701','VT18')
search_for_a_room(cu, 'd1142v')
#search_schedule_for_a_room( cu, 'Datorsal D1142V (PC)' )
#search_schedule_for_a_room_on_date( cu, 'Datorsal D1142V (PC)', '2018-03-14' )
#search_schedule_for_a_teacher( cu, 'Stepan Shevtsov' )

db.close()
