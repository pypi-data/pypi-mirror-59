# KeepFresh

A command line interface for polling changes in a directory and either logging or triggering a termination and restart of a provided command.
Watchdogs' utility tool watchmedo should be used as opposed to this. This was created due to lack of Watchdog documentation regarding running the tool in CLI with the polling mode.

This was developed for the usecase of hot-reloading in a Docker container where the host has a volume mount in the container.

Currently the provided directory is searched recursively for all file types, with the ability to ignore certain directories.

## Installation
```
pip install keepfresh
```
Which will install `keepfresh` as a command.

## Usage
```
usage: keepfresh [-h] [-i I] [-d D] [-e E [E ...]] [-x X [X ...]] [-a]
                 [-c C [C ...]] [-l]

optional arguments:
  -h, --help    show this help message and exit
  -i I          Interval
  -d D          Directory
  -e E [E ...]  Excluded directories
  -x X [X ...]  File extensions to watch
  -a            Auto restart
  -c C [C ...]  Command
  -l            Run the logging monitor
```

## Examples
Usage for logging event changes:
(This example logs any changes in the current directory ('.') at a 1 second polling interval)
```
$ keepfresh -i 1 -d . -l
```

Usage for auto-restarting a command:
(This example polls every second in the current directory. -a means to auto-restart, -c is the command)
```
$ keepfresh -i 1 -d . -a -c echo "Hello World"
```

If you only want to consider certain file types, use the `x` parameter
(This example polls every second in the current directory with logging, but only looks at .py and .txt files
```
$ keepfresh -i 1 -d . -a -x py md -c echo "Hello World"
```
