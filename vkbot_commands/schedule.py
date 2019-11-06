import pytz
import datetime
import vk_api
from vk_api import keyboard
def schedule(arguments, user_session, db):
    # TEMPLATE BLOCK
    session_vars = user_session.session_variables
    teachers = db["teachers"]
    groups = db["groups"]
    location = db["locations"]
    returndict = {
        "message": "",
        "keyboard": "",
        "new_curcommand": "",
        "new_arguments": ""
    }
    # TEMPLATE BLOCK END
    if not session_vars["arguments"]:  # Если аргументов нет
        returndict["message"] = "Введите школу"
    else:
        print(session_vars["arguments"][0])
        found = location.find(name=session_vars["arguments"][0])
        didfind = False
        for i in found:
            if i:
                didfind = True
        if didfind:  # Если написали заданную фразу
            msg = []
            loctable = db.query("SELECT g.time_start, g.time_end, g.id 'group_id', school.id 'loc_id', "
                                "school.name 'school_name', teach.id 'teacher_id', "
                                "teach.last_name 'last_name' \n"
                                "FROM groups AS g INNER JOIN locations school ON school.id = g.location_id \n"
                                "INNER JOIN teachers teach ON teach.id = g.teacher_id \n"
                                "WHERE school.name = '" + session_vars["arguments"][0] + "'")
            for i in loctable:
                print(i)
            #timerows = db.query
            #for i in loctable:
            #    if i["school_name"] == session_vars["arguments"][0]:
            #        timerows.insert(i)
            #        print(i)
            #print(timerows.columns)

            weekdays = {
                "1": "Понедельник: ",
                "2": "Вторник: ",
                "3": "Среда: ",
                "4": "Четверг: ",
                "5": "Пятница: ",
                "6": "Суббота: ",
                "7": "Воскресенье: ",
                "8": "АА СТРАШНА ВЫРУБАЙ"
            }
            for i in range(1, 7):
                result = db.query("SELECT g.time_start, g.time_end, g.id 'group_id', school.id 'loc_id', "
                                "school.name 'school_name', teach.id 'teacher_id', dof.name 'dayofweek', "
                                "teach.last_name 'last_name' \n"
                                "FROM groups AS g INNER JOIN locations school ON school.id = g.location_id \n"
                                "INNER JOIN teachers teach ON teach.id = g.teacher_id \n"
                                "INNER JOIN groups_days gd ON g.id = gd.group_id \n"
                                "INNER JOIN daysofweek dof ON gd.day_id = dof.id \n"
                                "WHERE school.name = '" + session_vars["arguments"][0] + "' AND gd.day_id = " + str(i))
                # помогите :(
                didfind = False
                result1 = []
                for j in result:
                    if j:
                        print("j : ", j)
                        didfind = True
                        result1.append(j)
                if didfind:
                    msg.append(db["daysofweek"].find_one(id=i)["name"])
                    msg.append(' ')
                    for j in result1:
                        print(j)
                        print(type(j["time_start"]))
                        time_start = (pytz.utc.localize(datetime.datetime.min + j["time_start"])).astimezone(pytz.timezone('Etc/GMT-5'))
                        time_end = (pytz.utc.localize(datetime.datetime.min + j["time_end"])).astimezone(pytz.timezone('Etc/GMT-5'))
                        time_start = time_start.strftime("%H:%M")
                        time_end = time_end.strftime("%H:%M")
                        startzrs = 1 if len(time_start.split(":")[1]) == 1 else 0
                        endzrs = 1 if len(time_end.split(":")[1]) == 1 else 0
                        time_start = time_start.split(":")[0] + ":" + "0" * startzrs + time_start.split(":")[1]
                        time_end = time_end.split(":")[0] + ":" + "0" * endzrs + time_end.split(":")[1]
                        msg.append(time_start + "-" + time_end + " " + j["last_name"] + ", ")
            print(msg)
            db["timerows"].drop()
            returndict["message"] = "".join(msg)
        else:
            returndict["message"] = "Школа не найдена. Попробуйте обратиться к списку адресов."
    return returndict