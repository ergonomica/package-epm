"""
[epm.py]

The Ergonomica package manager.
"""

import os
import shutil

try:
    import wget
except ImportError:
    raise Exception("[ergo: PackageError]: Please pip install `wget` to use package `package`.")

def epm(env, args, kwargs):
    if len(args) < 2:
        if args == ["list"]:
            return list(set([x.split(".")[0] for x in os.listdir(os.path.expanduser("~/.ergo/packages"))]))
        raise Exception("[ergo: ArgumentError]: Not enough arguments passed to `package` command.")
    if args[0] == "install":
        for package in args[1:]:
            try:
                os.chdir(os.path.expanduser("~/.ergo/packages"))
                wget.download("https://raw.githubusercontent.com/ergonomica/package-%s/master/%s.py" % (package, package))
            except Exception:
                raise Exception("[ergo: DownloadError]: Error downloading package `%s`." % package)
    elif args[0] == "uninstall":
        for package in args[1:]:
            shutil.rmtree(os.path.expanduser("~/.ergo/packages/%s" % package))

verbs = {"epm":epm,
        }
