# Introduction to Spatial Databases with PostGIS

Database systems can make spatial operations much simpler, and are more efficient for handling a large number of records. Working in a large spreadsheet or CSV can be quite difficult. Shapefiles have a size limit of 2 GB. Working with large spatial layers in a spatial database system such as PostGIS is both easier and much more efficient. There are many available relational database management systems (RDBMS) and a growing number of NoSQL (non-relational) database systems. We will focus on the PostGIS extension to PostgreSQL, arguably the most popular open source spatial RDBMS. (MySQL and its fork, MariaDB, continue to outpace PostgreSQL in popularity as a general RDBMS). We will learn about directly querying a database, then learn how to query a database using Python. You will learn some basic SQL suitable for spatial analysis. If you have already taken GUS 8067 - Spatial Database Design, some of this will already be familiar to you.

## 1. Installing Postgres/PostGIS

In this class we will run PostGIS in a Docker container. Docker is a virtualization technology that allows you to run a complete operating system inside another operating system. Docker has become reasonably widespread in the data science world because it is possible to share a Docker container with a configured server, a development environment, and even preloaded data, making it very easy for other researchers to reproduce your analysis without installing a lot of software. Of course, you will have to install Docker first if you don't already have it installed, but once you do, it gives you a "no installation" way to run a Postgres server, web server, Python development environment, or anything else that someone has already created a Docker container for.

Please follow my instructions for [Creating a PostGIS Server in Docker](https://leehach.github.io/spatialdb/creating_a_postgis_server_in_docker).

A PostGIS server can be created in several different ways. Briefly:

* PostGIS can be installed natively, i.e. installed to the OS so that your laptop (or other computer) is an actual PostGIS server. The easiest way to do this is on Windows or Mac is with the EnterpriseDB installer: <https://www.enterprisedb.com/downloads/postgres-postgresql-downloads>
* PostGIS can be run in a virtual machine. I recommend using OSGeoLive, a Linux-based OS that comes with a wide variety of open source GIS software and data preinstalled, including a full PostGIS server with several spatial databases. Instructions for setting up OSGeoLive in VirtualBox are available here: <https://live.osgeo.org/en/quickstart/virtualization_quickstart.html>
* PostGIS can be run in a Docker container. Use my instructions linked above.

There are two reasons for using Docker in this course. The first is that I have found that of the above three setup methods, this is probably the easiest. The second, more important reason, is that Docker is an increasingly important data science tool. Researchers, developers, and data scientists are increasingly using Docker to deliver a fully configured environment with software (not necessarily PostGIS), development environments, and data ready-to-go. You will probably encounter it elsewhere, and this experience will be useful.

The Docker instructions above also show how to connect to the database from the DBeaver management client. You can download and install DBeaver from <https://dbeaver.io/download/>.

You may see instructions online telling you to run the command `CREATE EXTENSION postgis;` when setting up a PostGIS server. You do *not* have to run this command if you use the Kartoza PostGIS container per the instructions linked above.

You can connect to the database from a variety of clients, including QGIS, ogr2ogr, and Python. When connecting from your local machine, the connections settings for any client are:

* Host: `localhost`
* Port: `5433`
* Database: `gis`
* User: `docker`
* Password: `docker`

This tells the client to attempt to connect to the database `gis` on port `5433` on your local machine (`localhost`) using the username and the password `docker`. Obviously, connecting to other PostGIS servers will require different settings.

## 2. Connect to the `gis` Database Using `psql`

Postgres comes with a native command line client `psql`. When you run it, you can issue commands in the database. We will view some basic `psql` commands.

Lauch a terminal (Mac Terminal, Windows Command Prompt, Windows Power Shell, etc.). Run a shell inside the container with the following command:

```sh
docker exec -it my_postgis /bin/bash
```

This assumes that you followed my instructions in creating the Docker container, and named the container `my_postgis`. If you named it something different, you will see `Error: No such container: my_postgis`. If you have the correct container name and still get that error, the container may not be running. Refer to the PostGIS setup instructions for starting and stopping the container, or open Docker Desktop and check the list of containers there to see if it is running.

You should see a banner for the container, and a prompt that begins `root@...`.

![](images/psql_inside_docker.png)\ 

You can now use `psql` inside the container to connect to the PostGIS server with the following command:

```sh
psql -h 127.0.0.1 -d gis -U docker
```

You will be prompted for the password which is also `docker`. You will then get the `psql` prompt, which begins with the name of the database you are connected to (`gis` in this case). Refer to the screenshot above.

Now give a SQL command at the prompt:

```sql
SELECT 'Hello, world!';
```

This is a very basic SQL statement. It does not query any table, it's just selects an expression (the value `'Hello, world!'`, a traditional first program to test in any language) into an unnamed column. It is very uninteresting, but it does prove that we are able to successfully issue SQL commands and 
have the database evaluate them and return a resultset.

Note that the semicolon (`;`) is required as a command terminator in `psql`. SQL statements can be complex and for ease of entry and reading are often typed on multiple lines. Hitting Enter does *not* cause the SQL statement to be evaluated unless the line ends with a semicolon.

Now lets issue some basic commands. `psql` has a number of "meta-commands" that begin with a backslash (`\`), and allow you to get information on database objects or perform actions *other than* SQL commands.


```sh
\l
```

This command lists all databases in the cluster. You should see `gis`, `postgres`, `template0`, and `template1`. `gis` is the database we are currently connected to, and the one we will work in for the remainder of this exercise. `postgres` is the maintenance database, which is present in every PostgreSQL cluster, and which should not be used to store data. The template databases can be configured for use as templates for other databases that you create. They should not be used to store data.

```sh
\dt
```

This command lists all tables in the current schema of the current database. As we haven't loaded any data yet, you should see only a small number of PostGIS maintenance tables such as `spatial_ref_sys`.

```
SELECT version();
SELECT PostGIS_Full_Version();
```

These commands provide information on the installed version of PostgreSQL and the installed version of PostGIS, including supporting libraries such as GEOS and GDAL.

When you are ready to quit, you can do so with `\q`, *but don't do this right now*. This will exit `psql` and return to the container shell. When you are done working in the container, you can use `exit` at the prompt to exit the container. Note that the container is still running, but you are no longer connected to its terminal.


## 3. Load Spatial Layers into the Database

As shown in the previous exercise, we can create database tables using SQL commands. When working with research data, we often need to import prexisting data (frequently, publicly available data). This section is about loading spatial layers such as shapefiles and GeoPackages into a spatial database. There are two GeoPackages in the repository data folder, a polygon layer "census3652.shp" and a point layer "philadata3652.shp". We will demonstrate two ways to import them, one using a GUI tool (QGIS) and one using a command line tool (`ogr2ogr`).

### 3.1. Load a Spatial Layer Using QGIS

#### 3.1.1. Connect to the Database

Before you can use QGIS to load, display, and anlayze data in your PostGIS database, you need to create a connection to the database. You can open the Create a New PostGIS Connection dialog in two ways:

1. In the Browser pane in QGIS, right-click PostgreSQL (might be called PostGIS in some versions of QGIS) and select New Conection….
2. Hit `Ctrl` + `Shift` + `D` to open the Data Source Manager, and under the dropdown list of connections, hit the New button.

You will see the following dialog. The connection settings are the same ones used earlier to connect to DBeaver. Some notes follow.

![](images/qgis_create_docker_postgis_connection.png)\ 

* **Name:** This can be anything you want. Name it something that will be clear and easy to understand, and don't worry about being verbose. As you do more research, you may make use of multiple PostGIS databases, so don't name it something generic like "PostGIS"! Including the server name, database name, or a project name for a single-purpose database, are all good options.
* **User name** and **password**: Click the Basic tab to display the user name and password textboxes. For this database---a local database used for learning purposes---we don't care about security, so click the checkboxes to Store the user name and password. This will save you from having to input your credentials every time you add a layer from this database. If you are working with a production database, make sure to follow your organization's security policy.

You might want to hit Test Connection and make sure everything is working before hitting OK.

#### 3.1.2. Use DB Manager to Upload Your Data

1. Open DB Manager in QGIS using the Database→DB Manager… menu.
2. In the left-hand Providers pane, expand the PostGIS tree, then expand the tree for the database connection you just added. Information about the database should load in the right-hand pane.
3. Click the Import Layer/File toolbar button. The Import Vector Layer dialog will appear.

The import dialog allows you to upload a layer currently displayed in QGIS (layers loaded in the current project, if any, will appear in the Input dropdown) or a file on your hard drive. Use the file browser (click the button with three dots to the right of the dropdown) to select `census3653.gpkg` from the course data folder.

Settings in the dialog should look like this. More explanation follows.

![](images/qgis_import_vector_layer.png)\ 

* **Schema:** Postgres uses schemas to organize tables and other database objects. The import dialog defaults to the public schema, and that is the one we will use.
* **Table:** The table name will default to the name of the layer being imported, minus any file extension. You can rename the table here, but the table name should not include special characters or spaces. Postgres table names should use `lower_case_with_underscores`. Note that we have checked **Convert field names to lowercase** below, so even if the table name has uppercase characters, they will be folded to lowercase.
* **Primary key:** Postgres developers prefer the name `gid` for the primary key of spatial tables.
* **Target SRID:** Although we are retaining the original projection, we could reproject the data during the load process by setting a different target SRID.
* **Create spatial index:** Spatial indices will speed up your spatial queries. There is almost never a reason to *not* create a spatial index right away.

### 3.2 Load a Spatial Layer Using `ogr2ogr`

**NOTE:** these are *not* SQL commands.

When you created your `geospatial` conda environment, conda also installed a handful of command line tools. We are going to demonstrate two of them, ogrinfo and ogr2ogr, which are used to display information on vector data sources and convert between vector data formats.

> **WARNING FOR WINDOWS USERS:** As of March 2023, ogrinfo and ogr2ogr on not working properly when run in PowerShell due to problems with the PROJ library (<https://github.com/conda-forge/pyproj-feedstock/issues/130>). For this section, please run all commands in Anaconda Prompt (Miniconda), ***not***  Anaconda PowerShell Prompt (Miniconda). Everything should be working correctly on Mac or Linux, and you should just use the usual terminal application for your OS. These notes also only apply to those using Anaconda for environment management. If you have installed Python, PyProj, and/or PROJ another way, I have no information as to whether ogrinfo and other utitlities dependent on PROJ will work for you. This problem is likely to go away as other projects accommodate changes to the PROJ library.

In Anaconda Prompt, activate the `geospatial` environment if it is not already activated. (You might want to open a new terminal window, as we will need to use `psql` again shortly.) 

First we need to add a dependency to the `geospatial` Anaconda environment. Run the following in your Anaconda shell (be sure the `geospatial` environment is activated): `conda install -c conda-forge libgdal-pg`. Wait for it to install before proceeding.

To get info on the PostGIS data source, we use the same connection parameters (host, port, dbname, user, and password) that we used previously. Get used to this! You will use these connection parameters next week when we connect to the database from Python.

The command below gets info on the spatial database using the given connection string. The `-so` switch means summary only, and reduces the amount of information displayed. It is especially useful when querying *layers*, as the result will otherwise include all attribute and geometry information on all features in the layer. When querying a *container*, it is less crucial. The results 

```sh
ogrinfo -so PG:"host=localhost port=5433 dbname=gis user=docker password=docker"
```

```
INFO: Open of `PG:host=localhost port=5433 user=docker password=docker dbname=gis'
      using driver `PostgreSQL' successful.
1: census3652 (Multi Polygon)
```

If you have uploaded other data, you may see more results in the list.

Now let's get information on the data set that we want to import, `philadata3652.gpkg`. Make sure that your working directory is the course repository. The statement below uses to relative paths to find `philadata3652.gpkg` in the `data` directory of the current directory. If your current working directory is different, you will have to either change directories or adjust the path in the command.

```sh
ogrinfo -so data/philadata3652.gpkg 
```

```
INFO: Open of `data/philadata3652.gpkg'
      using driver `GPKG' successful.
1: philadata3652 (Point)
```

Finally, we can import the data as follows. The format is:

```sh
ogr2ogr -f <output format> <destination> <source>
```

The output format will be PostgreSQL. The destination will use the same PG connection string that we used as input to ogrinfo above, and the source will be `philadata3652.gpkg` (with the appropriate path).

```sh
ogr2ogr -f PostgreSQL PG:"host=localhost port=5433 user=docker password=docker dbname=gis" data/philadata3652.gpkg -t_srs EPSG:3652
```
> **WARNING ** `-t_srs EPSG:3652` ensures that ogr2ogr does not add the wrong SRID to table.

Once the command runs, you can refresh the connection in QGIS DB Manager and preview the table and spatial data.

<!--
> **WARNING:** For reasons which are unclear to me, when I imported this data, it came in with an incorrect coordinate reference system. You can check the CRS in QGIS. If it is not SRID 3652, the import was incorrect. In this case you can either do the import in QGIS DB Manager, or you can use the ogr2ogr flag `-a_srs 3652` to override the SRID when you do the import:
>
> 
    ```sh
    ogr2ogr -f PostgreSQL PG:"host=localhost port=5433 user=docker password=docker dbname=gis" data/census3652.gpkg -a_srs 3652
    ```
-->

Back in `psql`, you can use `\dt` to see that both tables are now present in the database, or repeat your ogrinfo command against the database.

## 4. Querying in PostGIS

After importing the spatial layers into PostGIS tables, we can query the tables using spatial SQL.

### 4.1 Check the number of records in a layer

```sql
SELECT count(*) from philadata3652;
```

```
 count 
-------
 51686
(1 row)
```

### 4.2 Display Table Sturcture

```sh
\d philadata3652;
```

```
                               Table "big_geospatial_data.philadata3652"
   Column   |         Type         | Collation | Nullable |                  Default                   
------------+----------------------+-----------+----------+--------------------------------------------
 gid        | integer              |           | not null | nextval('philadata3652_gid_seq'::regclass)
 geom       | geometry(Point,3652) |           |          | 
 fid        | bigint               |           |          | 
 panoid     | character varying    |           |          | 
 year       | character varying    |           |          | 
 month      | character varying    |           |          | 
 lon        | double precision     |           |          | 
 lat        | double precision     |           |          | 
 pano_yaw   | double precision     |           |          | 
 tilt_yaw   | character varying    |           |          | 
 tilt_pitch | character varying    |           |          | 
 gvi        | double precision     |           |          | 
Indexes:
    "philadata3652_pkey" PRIMARY KEY, btree (gid)
    "sidx_philadata3652_geom" gist (geom)

~
(END)
```

When the SQL command returns a long result, the result is displayed one "page" at a time. You can use the spacebar to page through the results. When you see `(END)`, as above, the results are complete. At any point (even if you do not see `(END)`), you can type `q` to quit the display of results. The display will return to the SQL prompt.

### 4.3 Spatial Analysis in PostGIS

Now we are ready to run spatial queries against the database tables. The following query is a standard GIS point-in-polygon operation. It counts the number of points in `philadata3652` (representing traffic accidents) in polygon (representing a Census tract) in `census3652`.

The first form is more verbose. The second form uses **aliasing** to shorten the name of each table in the `FROM` clause for easier us when it is referenced elsewhere in the query.

```sql
SELECT census3652.tract, count(*)
FROM philadata3652 LEFT JOIN census3652 
    ON ST_Intersects(census3652.geom, philadata3652.geom)
GROUP BY census3652.tract;
```

And the same query with aliasing, followed by the result:

```sql
SELECT c.tract, count(*)
FROM philadata3652 p LEFT JOIN census3652 c
    ON ST_Intersects(c.geom, p.geom)
GROUP BY c.tract;

```

The first screen of results:

```
 tractce | count 
---------+-------
         |   303
 000801  |    21
 008702  |    76
 024000  |   107
 031502  |    50
 001500  |    69
 004102  |   106
 021300  |   112
 019000  |   188
 024300  |   115
 014200  |   182
 020102  |    92
 008802  |    82
 015700  |   143
 033300  |   212
 035301  |   116
 024100  |    53
 024600  |   133
 028902  |   106
 010000  |   126
 034801  |   166

```

We often want to add more attribute data, specifically, attributes of the container geography. That is, we really want to *add* the accident count to the Census tract layer. We usually want to retain the geometry (the `geom` column) of the container so that we can map the results.  Because `geom` displays a lengthy binary representation of the geometry, the display is not very readable, so the results will not be shown here. But our purpose will be to display this in a GIS or use it as input to further analysis.

The easiest way to include these additional columns from `census3652` is to add them to the `SELECT` list. Because of the grouping, these columns would have to also be added to the `GROUP BY` clause. We should also alias the output column `count(*)` for clarity. (In the following selection we limit the resultset to 1 just for display purposes.)

```sql
SELECT c.tract, c.county, c.state, c.geom, count(*) AS accident_count
FROM philadata3652 p LEFT JOIN census3652 c 
    ON ST_Intersects(c.geom, p.geom)
GROUP BY c.tract, c.county, c.state, c.geom
LIMIT 1;
```

\[**Results omitted**\]

There is a shortcut for including additional columns in the display without having to explicity include them in the `GROUP BY`. If you use a table's **primary key** as a grouping column, you can include additional columns (including all of them!) in the `SELECT` list without adding them to the `GROUP BY` clause. This query uses the `*` to request all columns from the table `census3652`:

```sql
SELECT c.*, count(*) AS accident_count
FROM philadata3652 p LEFT JOIN census3652 c 
    ON ST_Intersects(c.geom, p.geom)
GROUP BY c.id
LIMIT 1;
```

\[**Results omitted**\]

### 4.4 Making Results Available to External Tools

So far, we have merely displayed the results in `psql`. What we really want is to be able to access the results in another tool, such as a desktop GIS or a geospatial programming language.

There are several ways to do this.

1. We could use this query in another tool to extract the results for use in that tool. For example, QGIS DB Manager has a SQL Window that allows you to execute a SQL statement against the database. If the result returns a geometry column, QGIS can add it to the Canvas as a spatial layer.
2. The query could be persisted in the database as a new table using `CREATE TABLE ... AS ...`. There are two disadvantages to doing so:
    1. If the source data changes, the created table does not reflect the new data.
    2. If you create many such result tables for ad hoc analyses, your database will become filled with a lot of data that is redundant and has low reusability.
3. The query could be persisted as a **view**, which is instructions for running a specific query. If the underlying data changes, you will always get a query result based on the new data. The main disadvantage is that for a time-consuming query, you have to take the time hit every time you access the data. (A solution to this is a **materialized view**, but other than mentioning this so that you know about it, we won't pursue it further.)

We will use option 3, creating a view. The statement looks exactly like our last query, except that it starts with `CREATE VIEW <view_name> AS ...`. We also omit the `LIMIT`, because we do want all Census tracts in our result for mapping purposes.

```sql
CREATE VIEW vw_phila_accidents_by_tract AS
SELECT c.*, count(*) AS accident_count
FROM philadata3652 p LEFT JOIN census3652 c 
    ON ST_Intersects(c.geom, p.geom)
GROUP BY c.id;
```

If you go to QGIS, you can now see this view as another spatial layer in the database, add it to the Canvas, and make a choropleth map of the accidents. You can also export it to other formats such as GeoPackage or shapefile using QGIS, ogr2ogr, or other tools.

When you are through working with `psql`, use `\q` to quit `psql`. Then use `exit` to exit from the Docker container.

### Exercises
 - Use PostgreSQL and PostGIS queries against the database created in this lab to complete the exercises below. Include your SQL query code along with your solutions.

 1. What years and months are represented in the traffic accident data?
 
 2. In each year, summing all months on that year, which census tract had the most traffic accidents?

 3. In each month, cumulative across years, which census tract had the most traffic accidents?
 
 4. What is the mean traffic accidents per census tract per month and per year?
 
 5. What percentage of traffic accidents occured in the 5 most high-incident census tracts cumulative across all months and years?  
