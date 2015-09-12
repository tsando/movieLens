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





##############################################################################################
## APPENDIX
##############################################################################################

# # Print 5 rows in query
# for row in curs.execute("SELECT * FROM ratings  LIMIT 5;"):
#     print row
# print 'INFO:: finished printing 5 rows'


# dic1 = {'ratings': {'Timestamp': 3, 'MovieID': 1}}
# create_db(dic1, conn, curs)

# f = open('data/ml-1m/ratings.dat', "r")
# lines = f.readlines()
# f.close
# for i in lines:
#     values = i.split("::")

# for i in tables_dic:
#     create_db(i, tables_dic[i], conn, curs)
# create_db('movies', 'MovieID, Title, Genres', conn, curs)
# print 'INFO:: finished creating database for'+i
# for row in curs.execute("SELECT * FROM "+i+"  LIMIT 5;"):
#     print row
# print 'INFO:: finished printing 5 rows'

# for row in reader:
#     to_db = [unicode(row[0], 'utf8'), unicode(row[1], 'utf8'), unicode(row[2], 'utf8')]
#     curs.execute("INSERT INTO t (col1, col2) VALUES (?, ?);", to_db)
# conn.commit()


# def create_db(table_name, conn, curs):
#     # Open file and set csv reader
#     t = '{table}'
#     t = t.format(table = table_name)
#     path = 'data/ml-1m/'+t+'.dat'
#     f = open(path.format(table=table_name), "r")
#     lines = f.readlines()
#     f.close
#     # reader only works for double-pipe separated table
#     reader = csv.reader((line.replace('::', ':') for line in lines), delimiter=':')
#
#     # Create SQL table with right no. of cols
#     s1='' # First create string with dummy names
#     s2=''
#     n_cols = len(next(reader))
#     for i in range (n_cols):
#         s1+='col'+str(i+1)
#         s2+='?'
#         if i+1 == n_cols:
#             break
#         s1+=', '
#         s2+=', '
#     curs.execute("CREATE TABLE "+t+" ("+s1+");")
#
#     for row in reader:
#         to_db = []
#         for i in range(len(row)):
#             to_db += [unicode(row[i], 'utf8')]  # create list with row and columns entry
#         curs.execute("INSERT INTO "+t+" ("+s1+") VALUES ("+s2+");", to_db)
#     conn.commit()

# def create_db(table_name, col_names, conn, curs):
#     # Open file and set csv reader
#     t = '{table}'
#     t = t.format(table = table_name)
#     path = 'data/ml-1m/'+t+'.dat'
#     f = open(path.format(table=table_name), "r")
#     lines = f.readlines()
#     f.close
#     # reader only works for double-pipe separated table
#     reader = csv.reader((line.replace('::', ':') for line in lines), delimiter=':')
#
#     # Create SQL table with right no. of cols
#     s2=''
#     n_cols = len(next(reader))
#     for i in range (n_cols):
#         s2+='?'
#         if i+1 == n_cols:
#             break
#         s2+=', '
#     print "CREATE TABLE "+t+" ("+col_names+");"
#     curs.execute("CREATE TABLE "+t+" ("+col_names+");")
#
#     for row in reader:
#         to_db = []
#         for i in range(len(row)):
#             to_db += [unicode(row[i], 'utf8')]  # create list with row and columns entry
#         print to_db, t, col_names, s2
#         curs.execute("INSERT INTO "+t+" ("+col_names+") VALUES ("+s2+");", to_db)
#     conn.commit()

# query = "SELECT users.UserID, users.Gender, ratings.MovieID, AVG(ratings.Rating), movies.Title " \
#         "FROM ((users " \
#         "INNER JOIN ratings ON users.UserID = ratings.UserID) " \
#         "INNER JOIN movies ON ratings.MovieID = movies.MovieID) " \
#         "WHERE users.Gender='F' " \
#         "GROUP BY users.Gender, ratings.MovieID " \
#         "LIMIT 10;"


# query = "SELECT UserID,  FROM ratings LIMIT 5;"
# query = "SELECT * FROM users LIMIT 5;"

# Committing changes and closing the connection to the database file
# conn.close()

# # - Gender is denoted by a "M" for male and "F" for female
#
# if grouping == "gender":
#     print "top %s movies rated by men" % N
#     print "top %s movies rated by women" % N
#
#
# # - Age is chosen from the following ranges:
# #
# # 	*  1:  "Under 18"
# # 	* 18:  "18-24"
# # 	* 25:  "25-34"
# # 	* 35:  "35-44"
# # 	* 45:  "45-49"
# # 	* 50:  "50-55"
# # 	* 56:  "56+"
#
# if grouping == "agegroup":
#     print "7 lists above"