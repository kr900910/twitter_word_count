import psycopg2
import sys

# Print everything
if len(sys.argv) == 1:
    #Connecting to tcount
    conn = psycopg2.connect(database="tcount", user="postgres", password="pass", host="localhost", port="5432")
    cur = conn.cursor()

    #Select
    word=''
    count=0
    cur.execute("SELECT word, count from tweetwordcount ORDER BY word asc")
    records = cur.fetchall()
    for rec in records:
        word = rec[0]
        count = rec[1]
        print "(", word, ",", count, ")"
    conn.commit()
    conn.close()
else:
    word = sys.argv[1]
    
    #Connecting to tcount
    conn = psycopg2.connect(database="tcount", user="postgres", password="pass", host="localhost", port="5432")
    cur = conn.cursor()

    #Select
    count=0
    cur.execute("SELECT count from tweetwordcount WHERE word='{}' LIMIT 1".format(word))
    records = cur.fetchall()
    for rec in records:
        count = rec[0]
    conn.commit()
    conn.close()
    
    print "Total number of occurrences of of", word, ":", count
