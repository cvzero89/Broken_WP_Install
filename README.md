# Broken_WP_Install
Installs WordPress with fixed parameters and then "breaks" the install with common issues for training purposes.

## Usage:
```
$ python3 wordpress_exercise.py -h
usage: wordpress_exercise.py [-h] [--installer] [--reset]

Setting up WP for training exercises.

optional arguments:
  -h, --help   show this help message and exit
  --installer  Installs and sets up WP.
  --reset      Resets the environment.
```
  ### To start:

```
  git clone https://github.com/cvzero89/Broken_WP_Install.git
  cd Broken_WP_Install
  python3 wordpress_exercise.py --installer && source ~/.bashrc
```
