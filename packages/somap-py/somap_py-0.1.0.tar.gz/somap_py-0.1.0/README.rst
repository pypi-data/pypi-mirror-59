# somap_py | A Self Organizing Map Utility
Implements a Self Organizing Map algorithm based on the [R Kohonen SOM](https://cran.r-project.org/web/packages/kohonen/kohonen.pdf)
in Python. 


## Run the Self Organizing Map
The SOM can be run by calling the graphical user interface script (GUI):

`>> python som_selector_gui.py`

The SOM can also be run from a python script :

* Examples/SOM-Driver-Example.py
    * A simple example of how to make calls to run an SOM in a script


## Requirements for Windows
* Python 3+
* Numpy 
* Scipy 
* Matplotlib 
* Pandas 
* PyQt4
* Rtree 
* Scikit-Learn 
* Scikit-Image

If developing on Windows and unample to `>> pip install package` , pre-built solutions can be 
found at (https://www.lfd.uci.edu/~gohlke/pythonlibs/) where links can 
be downloaded from that site, making sure you select the correct download 
depending on your version of Python. These downloads are pre-compiled and 
made for easy Windows install. Once downloaded they can be installed from a 
command line like follows:

`>> pip install GDAl-2.3.2-cp37-cp37m-win_amd64.whl`
If you don't have __pip__ it will give you a message and tell you how to get it.

* Microsoft Visuall C++ Build Tools (https://www.microsoft.com/en-us/download/confirmation.aspx?id=48159)
    * Download and click through setup helper
