# Introduction to Spatial Databases with PostGIS

Database systems can make spatial operations much simpler, and are more efficient to handle a large number of records. Working in a large spreadsheet or CSV can be quite difficult. Shapefiles have a size limit of 2 GB. Working with large spatial layers in a spatial database system such as PostGIS is both easier and much more efficient. There are many available relational database management systems (RDBMS) and a growing number of NoSQL (non-relational) database systems. We will focus on the PostGIS extension to PostgreSQL, arguably the most popular open source spatial RDBMS. (MySQL and its fork, MariaDB, continue to outpace PostgreSQL as a general RDBMS). We will learn about directly querying a database, then learn how to query a database using Python. You will learn some basic SQL suitable for spatial analysis. If you have already taken GUS 8067 - Spatial Database Design, some of this will already be familiar to you.

## 1. Installing Postgres/PostGIS

In this class we will run PostGIS in a Docker container. Docker is a virtualization technology that allows you to run a complete operating system inside another operating system. Docker has become reasonably widespread in the data science world because it is possible to share a Docker container with a configured server, preloaded data, and a development environment, making it very easy for other researchers to reproduce your analysis without installing a lot of software. Of course, if you don't have Docker installed, you will have to install it first, but once you do it gives you a "no installation" way to run a Postgres server, web server, Python development environment, or anything else that someone has already created a Docker container for.

Please follow my instructions for [Creating a PostGIS Server in Docker](https://leehach.github.io/spatialdb/creating_a_postgis_server_in_docker).

> **TEMPORARY:** In class I will discuss other methods of installing PostGIS. These instructions will be updated with brief descriptions in the future.
> 
> https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

The instructions above show how to connect to the database from the DBeaver management client. You can download and install DBeaver from < https://dbeaver.io/download/>.

You can connect to the database from a variety of clients, including QGIS, ogr2ogr, and Python. When connecting from your local machine, the connections settings for any client are:

* Host: `localhost`
* Port: `5433`
* Database: `gis`
* User: `docker`
* Password: `docker`

This tells the client to attempt to connect to the database `gis` on port `5433` on your local machine (`localhost`) using the user and the password `docker`. Obviously, except for this particular Docker container, all of these settings are likely to be different.

## Connect to the `gis` Database Using `psql`

Postgres comes with a native command line client `psql`. When you run it, you can issue commands in the database. We will view some basic `psql` commands.

2. Be familiar with the databaseFor Windows user, Open PSQL shell,
Window ->Postgres -> PSQL Shell
For Mac user, type the command in your terminal,
psql -U postgres
Type in your password,Once you login to the database, let’s be familiar with the basic commands in psql,
List all databases,
\l
Connect to a certain database, \c databasename
\c dbname
List all tables,
\c dbname
\dt
The terminal return nothing using the above commands because there is nothing in your
database. Let’s first create a database for the following datasets.
create database phila;
Create extension of PostGIS
CREATE EXTENSION IF NOT EXISTS PostGIS CASCADE;
Then you can check the version of the installed PostGIS,
SELECT PostGIS_version();
3. Build a database and convert the shapefile into tables,
Although we can create our database and tables using commands, a simpler method to build a
database is to import existing tables into the database. This section is about converting shapefiles
into a spatial database. There are two shapefiles in the data folder, “census3652.shp” and
“philadata3652.shp”. Let’s input them into our PostGIS database.
First create a database of phila through the command,
create database phila;
Then you can import the shapefiles into the database of phila.
1. For windows users,Download
the
tool
to
convert
the
shapefile
to
spatial
data
base
table,
http://download.osgeo.org/postgis/windows/. Make sure put the exe file to the folder of the your
postgres. For example, on my computer, C:\Program Files\PostgreSQL. Then double click it to
install the tool,
Then let’s connect to the database in the postgis-bundle tool, by click ‘View Connection
details’,Fill the table using your username, password, localhost, and db name.
Then you need to enable the extension of PostGIS by typing in the PSQL shell,
CREATE EXTENSION POSTGIS;
After enabling the PostGIS, then you can import the shapefile to PostGIS table. Click the
“Add File”, and select the shapefile you want to convert to Postgres database table, and set the
“SRID” as the epsg code of the shapefile.Click the add File and select one shapefile, then you can click import. You can then check your
database in the PSQL shell,
\c phila;
\dt
You will find you have the table imported successfully.
Reference: https://postgis.net/workshops/postgis-intro/loading_data.html
For Mac users
You can just stay in the terminal and use the command line to convert the shapefile into
Postgres table. First cd to the directory of your shapefile, and then type in,Convert the shapefile of philadata3652.shp into a PostGIS table. First cd to the directory of the
philadata.shp file, and type in,
shp2pgsql -s 3652 philadata3652> philadata.sql
You will find that there is a file “philadata.sql” created. This is a series of Postgres commands.
We need to enable the PostGIS before running these commands. Open the “philadata.sql” using
text editor, and add the statement on top,
CREATE EXTENSION postgis;
Then you can run the .sql and import the shapefile into Postgres database table,
psql -h localhost -U postgres -d phila -p 5432 -f philadata.sql
-h: the host of localhost
-U: the username
-d: the database name
-p: portal, default of 5432
-f: the .sql file
Convert the shapefile of the census tract of Philadelphia into the table
shp2pgsql -s 3652 census3652> census3652.sql
Then you will find there is a census3652.sql file. The next step is to run the commands and
insert the data to your database, make sure you start the PostGIS service first in your psql terminal,
CREATE EXTENSION postgis;Then you can run the .sql in your Mac/Linux terminal,
psql -h localhost -U postgres -d phila -p 5432 -f census3652.sql
You can check if the shapefile has been imported into the database in the terminal,
\c phila;
\dt
4. A spatial query using PostGIS
After you imported the shapefiles into postgres tables, we can then get started to do our
queries using SQL.
4.1 Check the number of records in your point shapefile
select count(*) from philadata3652;4.2 Preview the structure of the table
\d philadata3652;
Now we are ready for the spatial database tables. Then we can use the database tables to do
the spatial join between the point shapefile and the census tract polygon file. Here is an example
of counting the number of points in each polygon,
SELECT census3652.tractce, count(philadata3652.panoid)
FROM philadata3652
LEFT JOIN census3652 ON ST_Intersects(census3652.geom, philadata3652.geom)
GROUP BY census3652.tractce;
We can make our statement shorter,
SELECT c.tractce, count(p.panoid)
FROM philadata3652 p
LEFT JOIN census3652 c ON ST_Intersects(c.geom, p.geom)
GROUP BY c.tractce;If we want more attribute to be saved, then you can use the statement of,
SELECT c2.tractce, c2.countyfp, c2.statefp, c2.geom, t.num
FROM (
SELECT c.tractce, count(p.panoid) as num
FROM philadata3652 p
LEFT JOIN census3652 c ON ST_Intersects(c.geom, p.geom)
GROUP BY c.tractce) t
JOIN census3652 c2 ON c2.tractce = t.tractce limit 4;
Since we want to save the result as a new shapefile, we need to create a new table of the
queried result,
CREATE TABLE CensusPntNum AS
SELECT c2.tractce, c2.countyfp, c2.statefp, c2.geom, t.num
FROM (
SELECT c.tractce, count(p.panoid) as num
FROM philadata3652 p
LEFT JOIN census3652 c ON ST_Intersects(c.geom, p.geom)
GROUP BY c.tractce) t
JOIN census3652 c2 ON c2.tractce = t.tractce;
Then you will find you have a new table “censuspntnum” created,You can check the structure of the newly created table by,
We can use the same commands to export the table to a shapefile,
Let’s save the table as a shapefile, using the following command in terminal (not your psql
command),pgsql2shp -u postgres -h localhost -P 5424796 -f pntshp phila "SELECT
* FROM censuspntnum;"
-u: the username of the database
-h: the host, here is the localhost
-P: is your password
-f: the file you going to save
phila: the database name
