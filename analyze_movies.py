#!/usr/bin/env python # required to run programs from command line without the "python " prefix
#
# analyze_movies.py
#
# run as: ./analyze_movies.py (gender|agegroup) <number>

from myArgparser import *
import sqlite3


def create_db(table_dic, tablename, conn, curs):
    # Define table name
    t = tablename

    # Define path and open file
    path = 'data/ml-1m/' + t + '.dat'
    f = open(path, "r")
    lines = f.readlines()
    f.close

    # Create SQL table with right no. of cols
    s1 = ''
    s2 = ''
    for i in table_dic.keys():
        s1 += i + ', '
        s2 += '?, '
    s1 = s1.strip(', ')
    s2 = s2.strip(', ')

    print "INFO: CREATE TABLE " + t + " (" + s1 + ");"
    curs.execute("CREATE TABLE " + t + " (" + s1 + ");")

    # loop over lines, split them and create columns
    for i in lines:
        to_db = i.replace('/n', '').split("::")
        to_db = list(to_db[j] for j in table_dic.values())
        # print "INSERT INTO " + t + " (" + s1 + ") VALUES (" + s2 + ");"
        # print to_db
        curs.execute("INSERT INTO " + t + " (" + s1 + ") VALUES (" + s2 + ");", to_db)
    print 'INFO: Finished creating table ' + t
    conn.commit()

# Print queries
def printq(query):
    for row in curs.execute(query):
        print row


def build_query(c1, i, N):
    query = "SELECT movies.Title, AVG(ratings.Rating)" \
            "FROM ((users " \
            "INNER JOIN ratings ON users.UserID = ratings.UserID) " \
            "INNER JOIN movies ON ratings.MovieID = movies.MovieID) " \
            "WHERE {id1} " \
            "GROUP BY {id2}, ratings.MovieID " \
            "ORDER BY AVG(ratings.Rating) DESC " \
            "LIMIT {n};".format(id1=c1+"="+i, id2=c1, n=N)
    printq(query)


############ Start of main()

# Create connection to db
conn = sqlite3.connect(":memory:")
conn.text_factory = str # to fix the bug with quotes in movies title
# conn = sqlite3.connect('data/ratings.db') # if not wanting to load to memory
curs = conn.cursor()


# These are all the fields available in the tables
# dic_all = {'ratings': {'UserID': 0, 'MovieID': 1, 'Rating': 2, 'Timestap': 3},
#               'users': {'UserID': 0, 'Gender': 1, 'Age': 2, 'Occupation': 3, 'ZipCode': 4},
#               'movies': {'MovieID': 0, 'Title': 1, 'Genres': 2}
#               }

# Selection of fields in the tables
dic_sel = {'ratings': {'UserID': 0, 'MovieID': 1, 'Rating': 2},
           'users': {'UserID': 0, 'Gender': 1, 'Age': 2},
           'movies': {'MovieID': 0, 'Title': 1}
           }

# Create a database for each table
for key, dic in dic_sel.iteritems():
    print key, dic
    create_db(dic, key, conn, curs)

# Vars imported from myArgparser
N = args.N_movies
grouping = args.grouping
print N, grouping
# N = 10
# grouping = 'agegroup'

print "INFO:: printing top {n} movies for grouping={g}".format(n=N, g=grouping)

if grouping == 'gender':
    for i in ["'F'", "'M'"]:
        build_query("users.Gender", i, N)
elif grouping == 'agegroup':
    ageID = [1, 18, 25, 35, 45, 50, 56]
    for i in ageID:
        print "INFO:: AGE GROUP "+str(i)
        build_query("users.Age", "'" + str(i) + "'", N)

# Close connection
conn.close()