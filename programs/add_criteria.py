import sqlite3

conn = sqlite3.connect("/home/j_blrd/webscraping/database/database.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS criteria_master_table \
          (criteria_id integer primary key, criteria_label text)")
c.execute("CREATE TABLE IF NOT EXISTS criteria_details \
          (criteria_id int, criteria_sub_id int, criteria_detail)")
c.execute("CREATE TABLE IF NOT EXISTS location_criteria \
          (location_id int, criteria_id int)")

new_criteria = input("Press enter to see current critera, else type in new critera \n")

if(new_criteria == ""):
    c.execute("SELECT * FROM criteria_master_table")
    results = "\n".join(str(s).replace("(", "").replace(")", "").replace("'", "").replace(",", "|") for s in c.fetchall())
    print(results)

else:
     c.execute("INSERT INTO criteria_master_table (criteria_label) VALUES(?)", (new_criteria,))
     conn.commit()
     print("Put in criteria details manualy")
