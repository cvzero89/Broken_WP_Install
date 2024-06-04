# Broken_WP_Install
Installs WordPress with fixed parameters and then "breaks" the install with common issues for training purposes.

## Usage:
```
$ python3 wordpress_exercise.py -h
usage: Broken WP Install [-h] --mode {install,run,reset}

Sets up a broken WordPress instance to be used for debug/training.

optional arguments:
  -h, --help            show this help message and exit
  --mode {install,run,reset}

What are you looking at? I am a short help article.
```
  ### To start:

```
  git clone https://github.com/cvzero89/Broken_WP_Install.git
  cd Broken_WP_Install
  python3 wordpress_exercise.py --mode install && source ~/.bashrc

  or:

  python3 wordpress_exercise.py --mode run && source ~/.bashrc
```
