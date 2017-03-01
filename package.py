"""
[package.py]

The Ergonomica package manager.
"""

import os

try:
    import wget
except ImportError:
    raise Exception("[ergo: PackageError]: Please pip install `wget` to use package `package`.")

def package(env, args, kwargs):
    if len(args) < 2:
        raise Exception("[ergo: ArgumentError]: Not enough arguments passed to `package` command.")
    if args[0] == "install":
        for package in args[1:]:
            try:
                os.chdir(os.path.expanduser("~/.ergo/packages"))
                wget.download("https://raw.githubusercontent.com/ergonomica/package-%s/master/%s.py" % (package, package)
            except:
                raise Exception("[ergo: DownloadError]: Error downloading package `%s`." % package)
