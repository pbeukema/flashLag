# flashlag
Adaptative flash lag experimental design for python

Below are instructions for getting flash lag on your computer. These instructions will work for linux and mac, but will need some modifications for use in windows. Note that if you have already installed the stand alone version of psychopy, when you try running this program from a terminal, it may not recognize that version. Use pip install psychopy (2b), and the libraries will import correctly. 
 
1. Install anaconda (http://continuum.io/downloads), [bash Anaconda$version#.sh]

2. Install dependencies if not already:
  
  a. Install pip (conda install pip)

  b. Install psychopy (pip install psychopy) 

  c. Install pyglet (pip install pyglet)

  d. Install wxpython (conda install wxpython)

  e. Install seaborn (pip install seaborn) 
  
3. If you did not clone the repo, then you will need to make a data directory for the output in the same location as flashlag.py (mkdir data).

4. Open a terminal, navigate to the directory containing flashlag.py, write python flashlag.py & press [enter]

5. Output data will be saved in data/

