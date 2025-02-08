## Configure Python environment through Anaconda
Python is an increasingly popular high-level programming language. It emphasizes legibility over highly complex structure. Python innately provides simple data structures allowing for easy data manipulation. Python provides a simple approach to object-oriented programming, which in turn allows for intuitive programming, and has resulted in a large user community that has created numerous libraries that extend the basic capacities of the language.

The Anaconda makes configuring Python programing environment super easy. The Anaconda is cross-platform and it is very easy to install different libraries in the virtual environment. The following tutorial will walk you through the tutorial for installing Anaconda and required Python modules.

## 1. Install Anaconda
1. **Download the Anaconda**. Go to the [website](https://www.anaconda.com/products/individual) to download Anaconda for different OSs. Select the right Anaconda for your computer.

 <img src="images/download-anaconda.png" title="A cute kitten" height="300" /> 



2. **Locate you installer and install**. Locate you downloaded Anaconda installer and then double click it to install. For Windows and MacOS, the installing is the same, just keep following the instructions by default.

<img src="images/wind-install.png" title="A cute kitten" height="300" />

3. **Check your installation**. When you installation is done, you can then check if you have the Anaconda installed successfully. For Windows, press windows button and see if you have `Anaconda Prompt`. For Mac, go to your terminal and type in `conda`. 


## 2.Be familiar with Anaconda
When you have the Anaconda installed successfully, then you can open your Anaconda terminal (command line) and create virtual environment for Python programming. 

1. Open the Anaconda. 
 - For Windows, open the `Anaconda Prompt` 
<img src="images/win-terminal.png" title="A cute kitten" height="300" />. 

- For Mac, go to the `terminal`  
<img src="images/mac-terminal.png" title="A cute kitten" height="300" />

- For Linux (Command Line) run `conda activate` or `source ./anaconda3/bin/activate`

2. Type in `conda info -e` in your terminal, you should see the `base` environment. The `base` is the default Python environment. We usually don't install Python modules in the `base`. 


## 3. Add the Conda-Forge Channel
The packaging team from Anaconda, Inc., packages a multitude of packages and provides them to all users free of charge in their defaults channel. But what if a package you are looking for is not in the defaults channel? `conda-forge` is a community effort that provides conda packages for a wide range of software.

 - see channels `conda config --show channels`
 - add conda-forge `conda config --append channels conda-forge`

## 4. Create a Customized Virtual Environment
1. Create a customized virutal environment called `geospatial`, `conda create --name geospatial -c conda-forge numpy shapely matplotlib rasterio fiona pandas ipython pyproj gdal rtree jupyter geopandas`. Using this command, you can install most needed modules in this class. It is pretty straightforward to install the modules you need in Anaconda. In most cases just type in `conda install name_module`.

## 5. Start Jupyter Notebook and write Python code
Now we have the required environment ready. Let's start the `Jupyter Notebook` and then write your Python code. 

1. Go to your terminal. Make sure the `geospatial` is activated. **Note**: If you still see the `base`, you need to activate it first by typing `conda activate geospatial` in the terminal. If you want to go back to base, you can also deactivate it, `conda deactivate`. In this way, you can swich between different virtual environment, which can be created for different purposes. 

2. Start the Jupyter Notebook by typing `jupyter notebook` in the terminal. Then you web browser will start automatically and guide you to the notebook. You can then write Python code over there. 

3. Turn off the environment by typing `conda deactivate`, delete the environment by typing `conda env remove -n <environment-name> --all`.



## What Next
Go to open the test Jupyter Notebook file [link](../01_basics_python_spatial_data.ipynb). You can open the `ipynb` file directly or copy the statment to you newly created notebook.

## Troubleshooting
You may find you are unable to import libraries into a jupyter notebook that you have installed in your Anaconda environment. You will see messages like `rasterio not found`. It may be the case that ipython and jupyter-notebook do not have the same sys.path as python. To verify, in your jupyter notebook run the following:

```
import sys
print(sys.executable)
print(sys.version)
```
And from a terminal running your Anaconda environment run the following:

```
python --version
which python
```
They should be identical. If they are not you can install the Python kernel for Jupyter to point to your current Anaconda environment.
```
conda install ipykernel
```
Then add the environment to Jupyter's list of available kernels. `geospatial` is the name of your Anaconda environment. The --display-name is how it will appear in the Jupyter interface.
```
python -m ipykernel install --user --name=geospatial --display-name "Python (geospatisl)"
```
After this, restart Jupyter Notebook and select the correct kernel (e.g., "Python (myenv)") from the "Kernel" > "Change Kernel" menu.

#### Reference
1. Jupyter notebook for beginners, https://realpython.com/jupyter-notebook-introduction/
2. Notebook Basics, https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Notebook%20Basics.html
