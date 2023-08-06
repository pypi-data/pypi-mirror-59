# KeepFresh

A command line interface for polling changes in a directory and either logging or triggering a termination and restart of a provided command.
Watchdogs' utility tool watchmedo should be used as opposed to this. This was created due to lack of Watchdog documentation regarding running the tool in CLI with the polling mode.

This was developed for the usecase of hot-reloading in a Docker container where the host has a volume mount in the container.

Currently the provided directory is searched recursively for all file types, with the ability to ignore certain directories, and to consider either all file types, or specific file types.

## Installation
```
pip install keepfresh
```
Which will install `keepfresh` as a command.

## Usage
```
usage: keepfresh [-h] [-d D] [-e E [E ...]] [-x X [X ...]]
                 {log,auto-restart} ...

optional arguments:
  -h, --help          show this help message and exit
  -d D                Directory (if not specified, defaults to current directory)
  -e E [E ...]        Excluded directories
  -x X [X ...]        File extensions to watch (if not specified, all are watched)

actions:
  {log,auto-restart}
    log               Run the logging monitor
    auto-restart      Run the command auto-restarter
```

## Examples
Usage for logging event changes:
(This example logs any changes in the current directory ('.') at a 1 second polling interval, we haven't specified filetypes or excluded directories, so all are watched)
```
$ keepfresh log -i 1 -d .
```

Usage for auto-restarting a command:
(This example polls the current directory. No directory is specified, so it defaults to the current directory. -c is the command to terminate and restart when changes are detected)
```
$ keepfresh auto-restart -c echo "Hello World"
```

If you only want to consider certain file types, use the `x` parameter
(This example polls every second in the current directory with logging, but only looks at .py and .txt files
```
$ keepfresh log -i 1 -x py txt
```
