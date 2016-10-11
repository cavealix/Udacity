# Write a query that returns all the species in the zoo, and how many animals of
# each species there are, sorted with the most populous species at the top.
# 
# The result should have two columns:  species and number.
#
# The animals table has columns (name, species, birthdate) for each individual.
# 
QUERY = "select count(species) as num, species from animals group by species order by num desc"

############################################################################

#
# Insert a newborn baby opossum into the animals table and verify that it's been added.
# To do this, fill in the rest of SELECT_QUERY and INSERT_QUERY.
# 
# SELECT_QUERY should find the names and birthdates of all opossums.
# 
# INSERT_QUERY should add a new opossum to the table, whose birthdate is today.
# (Or you can choose any other date you like.)
#
# The animals table has columns (name, species, birthdate) for each individual.
#

SELECT_QUERY = "select name, birthdate from animals where species = 'opossum';"

INSERT_QUERY = "insert into animals values('alix', 'opossum', '2016-09-16')"

############################################################################

#
# Find the names of the individual animals that eat fish.
#
# The animals table has columns (name, species, birthdate) for each individual.
# The diet table has columns (species, food) for each food that a species eats.
#

QUERY = '''
select animals.name from animals, diet where animals.species = diet.species and food = 'fish';
'''
############################################################################

#
# Find the one food that is eaten by only one animal.
#
# The animals table has columns (name, species, birthdate) for each individual.
# The diet table has columns (species, food) for each food that a species eats.
#

QUERY = '''
select diet.food, count(diet.food) as num from animals, diet where animals.species = diet.species group by food having num=1;
'''

############################################################################

#
# List all the taxonomic orders, using their common names, sorted by the number of
# animals of that order that the zoo has.
#
# The animals table has (name, species, birthdate) for each individual.
# The taxonomy table has (name, species, genus, family, t_order) for each species.
# The ordernames table has (t_order, name) for each order.
#
# Be careful:  Each of these tables has a column "name", but they don't have the
# same meaning!  animals.name is an animal's individual name.  taxonomy.name is
# a species' common name (like 'brown bear').  And ordernames.name is the common
# name of an order (like 'Carnivores').

QUERY = '''
select ordernames.name, count (taxonomy.t_order) as t_orders 
from animals, taxonomy, ordernames
where animals.species = taxonomy.name and taxonomy.t_order = ordernames.t_order
group by taxonomy.t_order
order by t_orders desc
;
'''

############################################################################

# To see how the various functions in the DB-API work, take a look at this code,
# then the results that it prints when you press "Test Run".
#
# Then modify this code so that the student records are fetched in sorted order
# by student's name.
#

import sqlite3

# Fetch some student records from the database.
db = sqlite3.connect("students")
c = db.cursor()
query = "select name, id from students order by name asc;"
c.execute(query)
rows = c.fetchall()

# First, what data structure did we get?
print "Row data:"
print rows

# And let's loop over it too:
print
print "Student names:"
for row in rows:
  print "  ", row[0]

db.close()


############################################################################

# This code attempts to insert a new row into the database, but doesn't
# commit the insertion.  Add a commit call in the right place to make
# it work properly.
# 

import sqlite3

db = sqlite3.connect("testdb")
c = db.cursor()
c.execute("insert into balloons values ('blue', 'water') ")
db.commit()
db.close()


############################################################################

#
# Roommate Finder v0.9
#
# This query is intended to find pairs of roommates.  It almost works!
# There's something not quite right about it, though.  Find and fix the bug.
#

QUERY = '''
select a.id, b.id, a.building, a.room
       from residences as a, residences as b
 where a.building = b.building
   and a.room = b.room ''' +
   #don't show results of students as their own roommates
   #and don't show duplicates a/b and b/a, therefore group by room
'''and a.id != b.id
   group by a.room
 order by a.building, a.room;
'''

#
# To see the complete residences table, uncomment this query and press "Test Run":
#
# QUERY = "select id, building, room from residences;"
# 

######################################################################

# Here are two tables describing bugs found in some programs.
# The "programs" table gives the name of each program and the files
# that it's made of.  The "bugs" table gives the file in which each
# bug was found.
#
# create table programs (
#    name text,
#    filename text
# );
# create table bugs (
#    filename text,
#    description text,
#    id serial primary key
# );
#
# The query below is intended to count the number of bugs in each
# program. But it doesn't return a row for any program that has zero
# bugs. Try running it as it is.  Then change it so that the results
# will also include rows for the programs with no bugs.  These rows
# should have a 0 in the "bugs" column.

select programs.name, count(bugs.filename) as num
   from programs left join bugs
        on programs.filename = bugs.filename
   group by programs.name
   order by num;

######################################################################

# Find the players whose weight is less than the average.
# 
# The function below performs two database queries in order to find the right players.
# Refactor this code so that it performs only one query.
#

def lightweights(cursor):
    """Returns a list of the players in the db whose weight is less than the average."""
    #original way in two queries
    #cursor.execute("select avg(weight) as av from players;")
    #av = cursor.fetchall()[0][0]  # first column of first (and only) row
    #cursor.execute("select name, weight from players where weight < " + str(av))"""
    
    #perform in single query 
    cursor.execute("select name, weight from players where weight < (select avg(weight) as av from players) ;")
    return cursor.fetchall()
