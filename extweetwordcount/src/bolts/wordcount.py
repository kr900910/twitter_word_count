from __future__ import absolute_import, print_function, unicode_literals

from collections import Counter
from streamparse.bolt import Bolt
import psycopg2


class WordCounter(Bolt):

    def initialize(self, conf, ctx):
        self.counts = Counter()

    def process(self, tup):
        word = tup.values[0]

        # Write codes to increment the word count in Postgres
        # Use psycopg to interact with Postgres
        # Database name: Tcount
        # Table name: Tweetwordcount
        # you need to create both the database and the table in advance.
                
        #Connecting to tcount
        conn = psycopg2.connect(database="tcount", user="postgres", password="pass", host="localhost", port="5432")
        cur = conn.cursor()

        #Select
        count = 0
	uWord = word.replace("'","''")
        cur.execute("SELECT count from tweetwordcount WHERE word='{}' LIMIT 1".format(uWord))
        records = cur.fetchall()
        for rec in records:
            count = rec[0]
        conn.commit()

        if count == 0:
            #Insert
            cur.execute("INSERT INTO tweetwordcount (word,count) VALUES ('{}', 1)".format(uWord))
            conn.commit()
        else:
            #Using variables to update
            count+=1
            cur.execute("UPDATE tweetwordcount SET count={} WHERE word='{}'".format(count, uWord))
            conn.commit()

        conn.close()

        # Increment the local count
        self.counts[word] += 1
        self.emit([word, self.counts[word]])

        # Log the count - just to see the topology running
        self.log('%s: %d' % (word, self.counts[word]))

