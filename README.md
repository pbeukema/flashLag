# flashlag
This is experimental code for testing dynamic speed vision or how well you can discriminate the location of a moving object relative to a fixed object. The inspiration for this test is a visual illusion called the flashlag effect which you can read about [here](https://en.wikipedia.org/wiki/Flash_lag_illusion). For reference, the best professional athletes I have tested score around 4 degrees, average performance among non-professionals I have tested is about 4 times worse.  

Below are instructions for getting flash lag to run. 

* Download/Install [anaconda](http://continuum.io/downloads)
```bash
bash Anaconda$version#.sh
```
* Install dependencies:
  * Install pip (conda install pip)
  * Install psychopy (pip install psychopy) 
  * Install pyglet (pip install pyglet)
  * Install wxpython (conda install wxpython)
  * Install seaborn (pip install seaborn) 
  
Note that Python 3 is currently incompatible with psychopy. Therefore if you are running python 3, the solution is to create a virtual environment with python 2. Conda makes that extremely simple. First install anaconda following step 1 below then come back here. 

```bash
conda create -n $newenvname python=2.XX anaconda 
```
This will download python 2.XX if you haven't already done so. Next activate your newly created environment with

```bash
source activate pyflash
```
  
* If you did not clone the repo, then you will need to make a data directory for the output in the same location as flashlag.py (mkdir data).

* Open a terminal, navigate to the directory containing flashlag.py, write python flashlag.py & press [enter]

* Output data will be saved in data/

