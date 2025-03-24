## Lab 9. Visualizing half-million building blocks online

This week we are going to talk about using Mapbox to visualize data on the web and Github to publish a web map to a public webpage. 

## 1. Prepare the data

### 1.1 Download the datasets

Download GTFS data for Septa buses

 - Visit https://opendataphilly.org/datasets/septa-gtfs/
 - Select `Current GTFS File` and download the zipfile.
 - Unzip the file (`gtfs_public.zip`), it contains 2 mote zipfiles (`google_bus.zip` & `google_rail.zip`)
 - Unzip `google_bus.zip` into `data/` folder in your local copy of the `big-geospatial-data` repo. After you unzip, the `google_bus` folder should be in the `data` folder (eg. `data/google_bus`). 
 - The `google_bus` folder should contain the following files `agency.txt`,`calendar.txt`,`calendar_dates.txt`,`feed_info.txt`,`routes.txt`,`shapes.txt`,`stops.txt`,`stop_times.txt`,`trips.txt`.

 Download and Run Python Script
 - Visit https://github.com/kotrc/GTFS-route-shapes, download `GenerateSimpleRouteShapes.py`.
 - Put the script into the `data/google_bus` folder
 - Activate you `geospatial` conda environment
 - Add the geojson package, run `conda install geojson`
 - Run the script `python3 GenerateSimpleRouteShapes.py`. You must run the script from within the directory containing the csv files of the gtfs archive.
 - The script will output a file called `route_shapes.geojson`.
 - You can inspect the file in QGIS or geojson.io.

### 1.2 Convert the geojson file into mbtile file
We are going to use mapbox to visualize the but routes in Philadelphia. Mapbox has developed an efficient format to using tiling system to visualize big spatial data. So, we are going to convert the geojson file into mbtiles. Here, you need to tool of `tippecanoe `

 - Install tippecanoe in the `geospatial` conda environment, run `conda install -c conda-forge tippecanoe`.
 - Copy the path the tipplecanoe executable, from within the `geospatial` conda environment run `which tippecanoe` 
 - Use tippecanoe to convert to mbtiles, run `/path/to/anaconda3/tippecanoe/executable -zg -o septa_bus.mbtiles --drop-densest-as-needed data/google_bus/route_shapes.geojson`
 - Inspect the .mbtiles in QGIS.
   - Open QGIS 

## 2. Visualize on the web with Mapbox

### 2.1 Upload to Mapbox Studio
 - Go to Mapbox Studio https://www.mapbox.com/mapbox-studio
 - Sign up for an account and login
 - Navigate to data manager, select tilesets
 - Note there are some tilesets included, check them out
 - Click `New Tileset`, and upload your mbtiles file
 - When the upload completes, select the tileset to view it plotted on a map
 - Select the Share button (top right corner) and note the tileset ID, you will use this later

### Create a Mapbox web application
 - Navigate outside your copy `big-geospatial-data` repository on your local machine
 - create a new folder, you can name it something like `geospatial-app`
 - Create a file named `index.html`
 - The following template uses the `Mapbox GL JS` javascript library to show a webmap and tileset layer
   - Paste the template below into `index.html` (you will make some modifications in future steps)

```
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Add a vector tile source</title>
<meta name="viewport" content="initial-scale=1,maximum-scale=1,user-scalable=no">
<link href="https://api.mapbox.com/mapbox-gl-js/v3.10.0/mapbox-gl.css" rel="stylesheet">
<script src="https://api.mapbox.com/mapbox-gl-js/v3.10.0/mapbox-gl.js"></script>
<style>
body { margin: 0; padding: 0; }
#map { position: absolute; top: 0; bottom: 0; width: 100%; }
</style>
</head>
<body>
<div id="map"></div>
<script>
	// TO MAKE THE MAP APPEAR YOU MUST
	// ADD YOUR ACCESS TOKEN FROM
	// https://account.mapbox.com
	mapboxgl.accessToken = 'YOUR_DEFAULT_MAPBOX_TOKEN_HERE';
    const map = new mapboxgl.Map({
        container: 'map',
        // Choose from Mapbox's core styles, or make your own style with Mapbox Studio
        style: 'mapbox://styles/mapbox/light-v11',
        zoom: 9,
        center: [-75.3464, 39.9835]
    });

    map.on('load', () => {
        map.addSource('septa-routes', {
            type: 'vector',
            // Use any Mapbox-hosted tileset using its tileset id.
            // Learn more about where to find a tileset id:
            // https://docs.mapbox.com/help/glossary/tileset-id/
            url: 'mapbox://YOUR_TILESET_ID_HERE'
        });
        map.addLayer(
            {
                'id': 'route-data',
                'type': 'line',
                'source': 'septa-routes',
                'source-layer': 'route_shapes-aa4x18',
                'paint': {
                    'line-color': '#ff69b4',
                    'line-width': 1
                }
            },
            'road-label-simple' // Add layer below labels
        );
    });
</script>

</body>
</html>
```
 - Add your mapbox default public token to `mapboxgl.accessToken`
   - Find this in Mapbox Studio by clicking the left side navigtion menu and selecting tokens
 - Add the tileset ID for your tileset to `url: 'mapbox://YOUR_TILESET_ID_HERE`
   - The instructions for finding this are in the `Upload and Visualize in Mapbox Studio` section above
   - When you add your tileset ID, please the `mapbox://` portion at the start of the string
 - View the application in a web browser, you can do this with right click on `index.html`, select applicaton, and select Chrome or Firefox


## 3. Github and Git
GitHub is website that provides hosting for software development version control using Git. Git is a free and open source distributed version control system designed to handle everything from small to very large projects with speed and efficiency. GitHub is not only a code sharing and social networking site for developers. It is also a web hosting site.  Below I have outlined how to host spatial data and a web application from GitHub.  This workflow is perfect for small applications. 

### Github pages
For this exercise, we will use Github to create a simple webpage repository. In this repository, we have the HTML, CSS, and JS required for our webpage. A feature of Github is the ability to create a homepage using something called Github pages.

To use Github pages to host a static page, you have to name your repository very specifically.The following steps detail creating a repository and setting up the initial settings.

Working with Github is easy, there are two main ways you can work with Github, via command line, or with a desktop GUI. The instructions below will show you how to get started on the command line.

### 3.1. Sign up a Github account
Sign up for a Github account on the Github site in which you can host projects and maintain repositories. ([Link](https://github.com/join?source=header-home))


### 3.2. Install Git and check if Git is installed on your Machine
Moving back to our local machine, we need to get git and Github setup so we can work with it.

**If you are using Mac**: Using Terminal, we are going to check for Git, and if it is not found, we will download and install necessary files.

**If you are using Windows**: Git does not work easily from the Windows command prompt. To easily use command line to interact with Github, you need to install Git bash for desktop where you can use Git Bash. This is a command line interface that allows you to run commands to create repositories, rectify file differences, and push commits.

[Download Github Bash](https://gitforwindows.org/)

Once downloaded, proceed below, but instead of using Terminal, you use Git Bash.

#### i. Open Terminal/Git Bash
#### ii. Check git installation by entering the following command
`git –-version`
if you have Git installed, you will see the version. If you get an error, or you don’t see the version, you need to install Git. Install Git from the downloads page on the main Git project homepage.

https://git-scm.com/

Download Git for your machine. A wizard will lead you through the installation. You can select the defaults for installation. You might need to restart your machine after installation to get it to take effect.


**For Mac**, type in `git --version` in your terminal and see if your get the git installed
**For Windows**, open your `Git` bash, and type in `git --version`. 

If we have the github account registered and `git` bash configured successfully, let get started and publish our geoviz online. 

**All the folowing commands will be run in Git Bash, NOT Anaconda**


### 3.3. Create a repository
i. Click on the Repositories tab on your main profile page.
On your Github profile page, click on the Repositories tab.

ii. In the upper right corner, select ‘New’.
Create a new repository, let's say you repo is call `bloodlead`. You can use other names as you like.

iii. In the Create a new repository window, set up your repository.
You name your repository as "geoviz" or other names you like. Give the repository a description, make it public. **Don't initialize it with a README.**

iv. Click Create.
You now have an empty repository set up in which you can add files and set up a project.

i. Click on the Repositories tab on your main profile page.
On your Github profile page, click on the Repositories tab.



### 3.4. Synchronize with your github repository
In you terminal, navigate to the directory that is storing your javascript files by using the `cd` command, my folder is called `geoviz`, you need to to use your folder name.
```
cd geoviz
```
Then initiate your folder as a github repository, 
```
git init
```
**MAKE SURE** your html file is named as `index.html`, or you will not be able to see your webpage.


Alright, let start to Synchronize our local folder with Github repository, 
```
git remote add origin https://github.com/xiaojianggis/bloodlead.git
```
You need to replace the last paramter by the link of your repository name. You can find these when your first created the github repository. This command will link your directory on your local machine with the GitHub repository.  You will see this command on GitHub under how to push an existing repository from the command line.

**Note**: if you get error of "fatal: remote origin already exists." Type the following statement to solve it,
```
git remote -v
git remote rm origin
git remote add origin https://github.com/xiaojianggis/bloodlead.git

```

### 3.5. Check out with a branch
Now you need to create a branch called gh-pages from GitHub and switch to this branch. Type in,
```
git checkout -b gh-pages
```
This command with switch to the gh-pages branch in the repository.

### 3.6. Add and commit your files to your repository
Now just commit everything in the folder to your repository by typing in 
```
git add .
git commit -m 'my initial commit, just a memo'
```

### 3.7. Finally push your project up to the branch gh-pages by typing in  
```
git push origin gh-pages 
```

### 3.8. Now your project is up on GitHub.  
In a web browser log into your GitHub account and view the project in the gh-pages branch.  You can also view the web site using your http://<GitHub handle>.github.io/repository name.  My final website can be viewed at https://xiaojianggis.github.io/bloodlead/

Make sure you replace the `xiaojianggis` by your own user name, and `bloodlead` by your own repository name. 



## Reference:
MIT DUSP Geoviz, https://github.com/civic-data-design-lab/16_11.S947/blob/master/week1/Part1_IntroGitAndGithub.ipynb
Web hosting on Github, https://gis.ucar.edu/github-web-hosting


