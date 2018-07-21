import sqlite3
import pandas as pd
import re
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import defaultdict
from multiprocessing import Process, Pool

start_time = time.time()

# Defining variables
i = 0
comments = []
extracted_comments = []
prox_comments = {}
analyzer = SentimentIntensityAnalyzer()

#Sqlite setup
conn = sqlite3.connect("/home/j_blrd/webscraping/database/database.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS filtered_guest_comments\
          (location_id int, property_id int, criteria_id int, date int, comment text, vader_score real)")

print(pd.read_sql_query("SELECT * FROM location_master_table", conn))

dest_name = input("Select location name from list above:\n")
c.execute("SELECT location_id FROM location_master_table WHERE location_name = ?", (dest_name,))
location_id = int(c.fetchone()[0])

c.execute("SELECT criteria_id FROM location_criteria WHERE location_id = ?", (location_id,))
criteria_ids = [x[0] for x in c.fetchall()] #This is the ids that we have to filter for

c.execute("SELECT property_name, property_id FROM property_master_table WHERE location_id = ?", (location_id,))
hotel_list = [list(x) for x in c.fetchall()]

def runInParallel(function, iteration):
    proc = []

    for x in iteration:
        p = Process(target = function(x))
        p.start()
        proc.append(p)
    for p in proc:
        p.join()

print(str(len(hotel_list)) + " Hotels in " + dest_name)
def clearVariables():
    global comment
    global comments
    global col
    global tmp_comment_list

    extracted_comments = []
    comments = []
    col = 9
    tmp_comment_list = []

def listToDict(criteria_detail): #Turns list of lists into dictionary eg. [[1, slope], [2, ski]] to {1, [slope] 2, [ski]}
    d = defaultdict(list)
    for k, v in criteria_detail:
        d[k].append(v)
    return(d)

def criteria(current_id):
    temp_extracted_comments = []

    c.execute("SELECT criteria_sub_id, criteria_detail FROM criteria_details WHERE criteria_id = ?", (current_id,))
    criteria_detail = [list(x) for x in c.fetchall()]
    criteria_detail = listToDict(criteria_detail)

    for b in range(0, len(comments)):
        if current_id == 1:
            #If any of 1 and any of 2 in comment
            if any(x in comments[b] for x in criteria_detail[1]):
                if any(x in comments[b] for x in criteria_detail[2]):
                    temp_extracted_comments.append(comments[b])
            #If all of 3 in comment
            elif all(x in comments[b] for x in criteria_detail[3]):
                temp_extracted_comments.append(comments[b])
            #if 4 in comment
            elif all(x in comments[b] for x in criteria_detail[4]):
                temp_extracted_comments.append(comments[b])

        if current_id == 2:
            #If any of 1 and any of 2 in comment
            if any(x in comments[b] for x in criteria_detail[1]):
                if any(x in comments[b] for x in criteria_detail[2]):
                    temp_extracted_comments.append(comments[b])

        if current_id == 3:
            #If any of 1 in comment
            if any(x in comments[b] for x in criteria_detail[1]):
                temp_extracted_comments.append(comments[b])
            #If any of 2 and 3 in comment
            if any(x in comments[b] for x in criteria_detail[2]):
                if any(x in comments[b] for x in criteria_detail[3]):
                    temp_extracted_comments.append(comments[b])
            #If any of 4 and 5 in comment
            if any(x in comments[b] for x in criteria_detail[4]):
                if any(x in comments[b] for x in criteria_detail[5]):
                    temp_extracted_comments.append(comments[b])

        if current_id == 4:
            #If 1 in comment and 2 not in comment
            if any(x in comments[b] for x in criteria_detail[1]):
                if (x not in comments[b] for x in criteria_detail[2]):
                    temp_extracted_comments.append(comments[b])

        if current_id == 5:
            #If any of 1 in comment
            if any(x in comments[b] for x in criteria_detail[1]):
                temp_extracted_comments.append(comments[b])

        if current_id == 6:
            #If any of 1 in comment and none of 2 not in comment
            if any(x in comments[b] for x in criteria_detail[1]):
                if all(x not in comments[b] for x in criteria_detail[2]):
                    temp_extracted_comments.append(comments[b])

        if current_id == 7:
            #If any of 1 in comment
            if any(x in comments[b] for x in criteria_detail[1]):
                temp_extracted_comments.append(comments[b])

        if current_id == 8:
            #If any of 1 is at the start of the comment
            if any(comments[b].startswith(x) for x in criteria_detail[1]):
                temp_extracted_comments.append(comments[b])

        if current_id == 9:
            #If any of 1 in comment and all of 2 not in comment
            if any(x in comments[b] for x in criteria_detail[1]):
                if all(x not in comments[b] for x in criteria_detail[2]):
                    temp_extracted_comments.append(comments[b])

        if current_id == 10:
            #If any of 1 or any of 2 and any of 3 in comment
            if any(x in comments[b] for x in criteria_detail[1]):
                temp_extracted_comments.append(comments[b])
            if any(x in comments[b] for x in criteria_detail[2]):
                if any(x in comments[b] for x in criteria_detail[3]):
                    temp_extracted_comments.append(comments[b])

        if current_id == 11:
            #If any of 1 in comment
            if any(x in comments[b] for x in criteria_detail[1]):
                temp_extracted_comments.append(comments[b])

        if current_id == 12:
            #If any of 1 in comment
            if any(x in comments[b] for x in criteria_detail[1]):
                temp_extracted_comments.append(comments[b])

        if current_id == 13:
            #If any of 1 and none of 2 in comment
            if any(x in comments[b] for x in criteria_detail[1]):
                if all(x not in comments[b] for x in criteria_detail[2]):
                    temp_extracted_comments.append(comments[b])

        if current_id == 14:
            #If any of 1 in comment or any of 2 and any of 3 in comment
            if any(x in comments[b] for x in criteria_detail[1]):
                temp_extracted_comments.append(comments[b])
            if any(x in comments[b] for x in criteria_detail[2]):
                if any(x in comments[b] for x in criteria_detail[3]):
                    temp_extracted_comments.append(comments[b])

        if current_id == 15:
            #If any of 1 in comment or any of 2 and none of 3 in comment
            if any(x in comments[b] for x in criteria_detail[1]):
                temp_extracted_comments.append(comments[b])
            if any(x in comments[b] for x in criteria_detail[2]):
                if all(x not in comments[b] for x in criteria_detail[3]):
                    temp_extracted_comments.append(comments[b])

        if current_id == 16:
            #If any of 1 in comment
            if any(x in comments[b] for x in criteria_detail[1]):
                temp_extracted_comments.append(comments[b])

    temp_extracted_comments = [x.split(" || ") for x in temp_extracted_comments]
    [x.extend([location_id, property_id, current_id]) for x in temp_extracted_comments]
    [x.append(analyzer.polarity_scores(x[0])['compound']) for x in temp_extracted_comments]
    extracted_comments.extend(temp_extracted_comments)


for i in range(0, len(hotel_list)):
    print(str(hotel_list[i][1]) + ": " + hotel_list[i][0]) #Prints hotel name and property_id
    property_id = int(hotel_list[i][1])
    c.execute("SELECT comment, date FROM unfiltered_guest_comments WHERE location_id = ? and property_id = ?",\
              (location_id, property_id,))
    entry = c.fetchall()
    #comments = [[item] for sublist in [list(x)[0].split(".") for x in entry] for item in sublist]
    comments = [list(x)[0].split(".") for x in entry] #Get comments from db
    dates = [list(x)[1] for x in entry]
    comments = [[item + " || " + dates[x] for item in comments[x]] for x in range(1, len(comments))] #Add date to end of every sentence
    comments = [x for sublist in comments for x in sublist] #Turn list of lists into flat list
    #pool.map(criteria, criteria_ids)
    #runInParallel(criteria, [0,1,2,3,4])
    for x in criteria_ids:
       criteria(x)

#for s in extracted_comments:
#    print(*s)

for x in range(0, len(extracted_comments)):
    c.execute("INSERT INTO filtered_guest_comments (comment, date, location_id, property_id, criteria_id, vader_score) \
                VALUES(?, ?, ?, ?, ?, ?)", \
                (extracted_comments[x][0], extracted_comments[x][1], extracted_comments[x][2], \
                extracted_comments[x][3], extracted_comments[x][4], extracted_comments[x][5]))
conn.commit()
print(time.time() - start_time)

