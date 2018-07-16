import sqlite3

conn = sqlite3.connect("/home/j_blrd/webscraping/database/database.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS location_master_table \
          (location_id integer primary key, location_name text)")

c.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_location_name ON location_master_table (location_name)")


new_name = input("Press enter to see current locations, else type in new location name \n")

if(new_name == ""):
    c.execute("SELECT * FROM location_master_table")
    results = "\n".join(str(s).replace("(", "").replace(")", "").replace("'", "").replace(",", ":") for s in c.fetchall())
    print(results)

else:

    c.execute("INSERT INTO location_master_table (location_name) VALUES(?)", (new_name,))
    conn.commit()

