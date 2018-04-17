import os
import sqlite3
import pprint as pp

db = sqlite3.connect(os.path.curdir + '/unitime.db')
cu = db.cursor()

def print_menu():
  print("-" * 50)
  print(" " * 23 + "MENU" + " " * 23)
  print("-" * 50)
  print("1. Search for a course")
  print("2. Search for a schedule")
  print("3. Search for a room")
  print("4. Search schedule for a room")
  print("5. Search schedule for a room on a specific date")
  print("6. Search schedule for a teacher")
  print("7. Exit")
  print("-" * 50 + "\n")

def print_data(rows):
  rows_list = list(set(rows))

  for row in rows_list:
    print("-" * 50)
    print("\n".join(row))
    print("-" * 50)

def start_menu():
  print_menu()
  value = raw_input("Answer: ")
  if value == "1":
    ask_search_for_course()
  elif value == "2":
    ask_search_for_schedule()
  elif value == "3":
    ask_search_for_a_room()
  elif value == "4":
    ask_search_schedule_for_a_room()
  elif value == "5":
    ask_search_schedule_for_a_room_on_date()
  elif value == "6":
    ask_search_schedule_for_a_teacher()
  elif value == "7":
    db.close()
    SystemExit(0)

def ask_search_for_course():
  value = raw_input("Please enter course code? (Back to menu: 7)\nAnswer: ")
  if value == "7":
    start_menu()
  else:
    search_for_course(cu, value)

def search_for_course( cursor, course ):
    cursor.execute("SELECT * FROM Courses WHERE course_code = :course", {'course': course})
    rows = cursor.fetchall()

    print_data(rows)
    
    ask_search_for_course()

def ask_search_for_schedule():
  value = raw_input("Please enter course code and semester seperated with a ',' (Back to menu: 7)\nAnswer: ")
  if value == "7":
    start_menu()
  else:
    value_list = value.split(",")
    course_code = value_list[0]
    semester = value_list[1]
    search_for_schedule(cu, course_code, semester)

def search_for_schedule( cursor, course, semester ):
    cursor.execute("SELECT * FROM Schedules WHERE course = :course AND semester = :semester" , {'course': course, 'semester': semester})
    rows = cursor.fetchall()

    print_data(rows)
    
    ask_search_for_schedule()

def ask_search_for_a_room():
  value = raw_input("Please enter the room (room code) you want to check (Back to menu: 7)\nAnswer: ")
  if value == "7":
    start_menu()
  else:
    search_for_a_room(cu, value)

def search_for_a_room( cursor, room ):
    cursor.execute("SELECT * FROM Rooms WHERE room_code LIKE :room" , {'room': '%' + room + '%'})
    rows = cursor.fetchall()
    rows_list = list(set(rows))

    for row in rows_list:
      print("".join(unicode(row)))
    
    ask_search_for_a_room()

def ask_search_schedule_for_a_room():
  value = raw_input("Please enter the room (room code) you want to check the schedule for (Back to menu: 7)\nAnswer: ")
  if value == "7":
    start_menu()
  else:
    search_schedule_for_a_room(cu, value)

def search_schedule_for_a_room( cursor, room ):
    cursor.execute("SELECT * FROM Schedules WHERE room LIKE :room" , {'room': '%' + room + '%'})
    rows = cursor.fetchall()
    
    print_data(rows)
    
    ask_search_schedule_for_a_room()

def ask_search_schedule_for_a_room_on_date():
  value = raw_input("Please enter the room (room code) and a date to check the schedule, seperated with a ',' (Back to menu: 7)\nAnswer: ")
  if value == "7":
    start_menu()
  else:
    value_list = value.split(",")
    room_code = value_list[0]
    date = value_list[1]
    search_schedule_for_a_room_on_date(cu, room_code, date)

def search_schedule_for_a_room_on_date( cursor, room, date ):
    cursor.execute("SELECT * FROM Schedules WHERE room LIKE :room AND date = :date"  , {'room': '%' + room + '%', 'date': date})
    rows = cursor.fetchall()
    
    print_data(rows)
    
    ask_search_schedule_for_a_room_on_date()

def ask_search_schedule_for_a_teacher():
  value = raw_input("Please enter the name of the teacher you want to check the schedule on (Back to menu: 7)\nAnswer: ")
  if value == "7":
    start_menu()
  else:
    search_schedule_for_a_teacher(cu, value)

def search_schedule_for_a_teacher( cursor, teacher ):
    cursor.execute("SELECT * FROM Schedules WHERE teacher = :teacher", {'teacher': teacher})
    rows = cursor.fetchall()

    print_data(rows)
    
    ask_search_schedule_for_a_teacher()

start_menu()
