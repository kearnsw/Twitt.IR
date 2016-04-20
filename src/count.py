from Request import Request
import os

months = ["Jan", "Feb", "Mar", "Apr", "May",
          "Jun", "Jul", "Aug", "Sep", "Oct",
          "Nov", "Dec"]

q = Request()
q.connect()
count = -1
directory = os.path.dirname(os.getcwd())
f = open(directory + "/data/test.csv", "w+")
while count != 0:
    start_date = q.date
    # criteria = [{"$group": {"_id": "$created_at",
    #                        "count": {"$sum": 1}}}]
    criteria = {"created_at": {'$regex': start_date}}
    count = q.count(criteria)

    f.write(start_date + ", " + str(count) + "\n")

    date = start_date.split()
    month = date[0]
    day = date[1]
    if day == "31":
        for index in range(len(months)):
            if month == months[index]:
                month = months[index+1]
                day = "1"
                break
    else:
        day = str(int(day) + 1)

    date = month + " " + day
    q.date = date






