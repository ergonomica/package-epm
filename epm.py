"""
[epm.py]

The Ergonomica package manager.
"""

import os
import shutil
import pickle

# thanks to http://stackoverflow.com/users/578907/uwe-kleine-k%C3%B6nig
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

try:
    import semver
except ImportError:
    raise Exception("[ergo: PackageError]: Please pip install `semver` to use package `epm`.")

# path to Ergonomica local package store
PATH_TO_LOCALSTORE = os.path.join(os.path.expanduser("~"), ".ergo", ".epm")

# path to Ergonomica package directory
PATH_TO_PACKAGES = os.path.join(os.path.expanduser("~"), ".ergo", "packages")

def download(path, url):
    open(path, "wb").write(urlopen(url).read())

# list flattening (for package lists)
flatten = lambda l: [item for sublist in l for item in sublist]

class RepositoryCollection(object):

    # list of all repositories
    repositories = []

    def __init__(self, store=None):
        self.store = store
        pass

    def update_store(self):
        if self.store: # if the package repository is stored in a file
            pickle.dump(self, open(store, "wb"))
            
    def add_repo(self, repository):
        # check if two repositories have the same URL
        # (if so raise an error)
        for repo in self.repositories:
            if repo.url == repository.url:
                raise Exception("[ergo: epm]: [PackageError] New repository '%s' has existing source '%s'. Aborting." % (repository.url, repo.url))

        self.repositories.append(repository)
        self.update_store()
        
    def remove_repo(self, repositories):
        try:
            self.repositories.remove(repository)
        except ValueError:
            print("[ergo: epm]: [Warning] Package to be removed ('%s'), but doesn't exist!")

        self.update_store()

    #def remove_package(self):
    #    for repository in self.repositories:
    #   

    def update(self):
        for repo in self.repositories:
            repo.update()
    
    def update_packages(self):
        for repo in self.repositories:
            repo.update_packages()

    def list_packages():
        return flatten([x.installedPackages for x in self.repositories])

    def list_repositories():
        return [x.name for x in repositories]

    def install_package(packagename):
        for repository in self.repositories:
            if repository.install_package(packagename):
                print("[ergo: epm]: Package `%s` successfully installed." % packagename)
                return
                                
        print("[ergo: epm]: [PackageError]: [Warning] No package `%s` found." % (packagename))
                                
class Repository:
    name = ""
    url = ""
    remotePackages = []
    installedPackages = []
    
    def __init__(self, name, url):
        # initialize a new repository
        self.name = name
        self.url = url

    def update(self):
        new_packages = str(urlopen(self.url).read()).split("\\n\\n")
        
    def update_packages(self):
        for package in installedPackage:
            package.update_package()

            
    def remove_packages(self):
        #
        pass
        
class Package:
    name = ""
    url = ""
    version = ""
    description = ""

    def __init__(self, name, description, url):
        self.name = name
        self.description = description
        self.url = url

    def install(self):
        """Install the latest version of a package."""

        try:
            download(PATH_TO_PACKAGES, self.url)
        except Exception, e:
            print("[ergo: epm] [Error] Could not download package `%s`." % (self.name))
        
    def doctor(self):
        if self.name == "":
            print("[ergo: epm]: [Warning] A package has an empty name!")


    def equals(self, new_package):

    def is_later_version(self, new_package)

def package_from_listing(string):
    """Generate a Package() object from a MANIFEST listing."""
    split_listing = string.split("\\n")
    return Package()

# NOTE: this does not need to be continuously updated as the instantiated RepositoryStore object
# automatically updates itself on any changes
try:
    localStore = pickle.load(open(PATH_TO_LOCALSTORE, "rb"))
except FileNotFoundError: # there is no package store
    print("[ergo: epm] [Info] No epm store found!")
    print("[ergo: epm] [Info] Initializing package store at %s.." % (PATH_TO_LOCALSTORE))

    # initialize the localstore as a RepositoryCollection
    localStore = RepositoryCollection(PATH_TO_LOCALSTORE)

def epm(env, args, kwargs):

    # info commands (list packages, list repos)
    if len(args) < 2:
        if args == ["packages"]:
            return localStore.list_packages()

        elif args == ["repos"]:
            return localStore.list_repositories()

        else:
            raise Exception("[ergo: ArgumentError]: Not enough arguments passed to `package` command.")

    if args[0] == "add-source":
        map(localStore.add_repository, map(Repository, args[1:]))

    elif args[0] == "install-pkg":
        map(localStore.install_package, args[1:])

    elif args[0] == "uninstall-pkg":
        map(localStore.uninstall_package, args[1:])

verbs = {"epm":epm,
        }
 
