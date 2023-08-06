# git-multi-branch
Clone all branches of a git repository

## Install
```
$ pip install git-multi-branch
```

## Usage
```
$ git-multi-branch --help

Usage: gitmb.py [OPTIONS] URL

  Clones all the branches of a git repository using the given url. It uses
  the local ssh key of the current user to authenticate while running git
  commands.

Options:
  -d, --target-dir TEXT  Target directory to run the command from  [default:
                         ./repos]
  -c, --cache-dir TEXT   Cache directory  [default: ./.cache]
  --help                 Show this message and exit.
```

Examples:
```
# (Default) Clones all the branches related to the git-url
$ git-multi-branch <git-url>

```