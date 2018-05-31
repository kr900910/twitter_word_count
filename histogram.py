import psycopg2
import sys

# Print everything
if len(sys.argv) == 3:
    k1 = sys.argv[1]
    k2 = sys.argv[2]
    
    #Connecting to tcount
    conn = psycopg2.connect(database="tcount", user="postgres", password="pass", host="localhost", port="5432")
    cur = conn.cursor()

    #Select
    word=''
    count=0
    cur.execute("SELECT word, count from tweetwordcount where count >= {} and count <= {}".format(k1,k2))
    records = cur.fetchall()
    for rec in records:
        word = rec[0]
        count = rec[1]
        print "(", word, ",", count, ")"
    conn.commit()
    conn.close()
