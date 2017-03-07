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

# list flattening
flatten = lambda l: [item for sublist in l for item in sublist]

class RepositoryCollection(object):

    # list of all repositories
    repositories = []

    def __init__(self):
        pass

    def add_repo(self, repository):
        # check if two repositories have the same URL
        # (if so raise an error)
        for repo in self.repositories:
            if repo.url == repository.url:
                raise Exception("[ergo: epm]: [PackageError] New repository '%s' has existing source '%s'. Aborting." % (repository.url, repo.url)

        self.repositories.append(repository)
        
    def remove_repo(self, repositories):
        try:
            self.repositories.remove(repository)
        except ValueError:
            print("[ergo: epm]: [Warning] Package to be removed ('%s'), but doesn't exist!")

    def update_packages(self):
        for repo in self.repositories:
            repo.update_packages()

    def list_packages():
        return flatten([x.installedPackages for x in self.repositories])

    def list_repositories():
        return [x.name for x in repositories]

                                
class Repository:
    name = ""
    url = ""
    installedPackages = []
    
    def __init__(self, name, url):
        # initialize a new repository
        self.name = name
        self.url = url

    def update_packages(self):
        for package in installedPackage:
            package.update_package()

    def remove_packages(self):


class Package:

def epm(env, args, kwargs):
    if len(args) < 2:
        if args == ["list"]:
            return list(set([x.split(".")[0] for x in os.listdir(os.path.join(os.path.expanduser("~"),".ergo","packages"))]))
        raise Exception("[ergo: ArgumentError]: Not enough arguments passed to `package` command.")
    if args[0] == "install":
        for package in args[1:]:
            try:
                os.chdir(os.path.join(os.path.expanduser("~"), ".ergo", "packages"))
                wget.download("https://raw.githubusercontent.com/ergonomica/package-%s/master/%s.py" % (package, package))
            except Exception:
                raise Exception("[ergo: DownloadError]: Error downloading package `%s`." % package)
    elif args[0] == "uninstall":
        for package in args[1:]:
            shutil.rmtree(os.path.join(os.path.expanduser("~"), ".ergo", "packages", "%s" % package))

verbs = {"epm":epm,
        }
