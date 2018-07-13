import sqlite3

conn = sqlite3.connect("/home/j_blrd/webscraping/database/database.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS review_site_master_table \
           (review_site_id integer primary key, review_site_name text)")

new_review_site = input("Press enter to see current review sites, else type in new review site \n")
if(new_review_site == ""):
    c.execute("SELECT * FROM review_site_master_table")
    results = "\n".join(str(s).replace("(", "").replace(")", "").replace("'", "").replace(",", ":") for s in c.fetchall())
    print(results)

else:
    c.execute("INSERT INTO review_site_master_table (review_site_name) VALUES(?)", (new_review_site,))
    conn.commit()
