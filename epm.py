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
    open(path, "wb").write(urlopen(url).read().decode("utf-8"))

# list flattening (for package lists)
flatten = lambda l: [item for sublist in l for item in sublist]

class Package:
    name = ""
    url = ""
    version = ""
    description = ""

    def __init__(self, name, version, description, url):
        self.name = name
        self.description = description
        self.url = url

    def install(self):
        """Install the latest version of a package."""

        try:
            download(os.path.join(PATH_TO_PACKAGES, "ergo_" + self.name + ".py"), self.url)
        except Exception as e:
            print("[ergo: epm]: [Error] Could not download package `%s`." % (self.name))

    def uninstall(self):
        """Uninstall self."""
        os.remove(os.path.join(PATH_TO_PACKAGES, self.name))
        print("[ergo: epm]: Removed package `%s`." % self.name)
        
    def doctor(self):
        if self.name == "":
            print("[ergo: epm]: [Warning] A package has an empty name!")


    def equals(self, new_package):
        #TODO
        pass
        
    def is_later_version(self, new_package):
        #TODO
        pass


def package_from_listing(string):
    """Generate a Package() object from a MANIFEST listing."""
    [pacinfo, description, url] = string.strip().split("\n")
    [name, version] = pacinfo.split("(")
    version = version[:-1]
    return Package(name, version, description, url)

                               
class Repository:
    name = ""
    url = ""
    remotePackages = []
    installedPackages = []
    
    def __init__(self, name, url):
        # initialize a new repository
        self.name = name
        self.url = url

    def install_package(self, packagename):
        for remotePackage in self.remotePackages:
            if remotePackage.name == packagename:
                remotePackage.install()
                self.installedPackages.append(remotePackage)
                return True
        return False
        
    def update(self):

        new_packages = urlopen(self.url).read().decode("utf-8").split("\n\n")
        try:
            new_packages.remove("'")
        except ValueError:
            pass

        self.remotePackages = [package_from_listing(pkg) for pkg in new_packages]
        
    def update_packages(self):
        #self.remotePackages = map(package_from_
        
        #for package in installedPackage:
        #    package.update_package()
        pass
        
            
    def remove_packages(self, packagename):
        for installedPackage in self.installedPackages:
            installedPackages.remove(package)
        pass
 


class RepositoryCollection(object):

    def __init__(self, store=None):
        self.store = store
        self.repositories = []
        
    def load_from_store(self):
        if self.store:
            self.__dict__.update(pickle.load(open(self.store, 'rb')))
        else:
            raise Exception("Can't load from store if not set!")
        
    def update_store(self):
        if self.store: # if the package repository is stored in a file
            pickle.dump(self.__dict__, open(self.store, "wb"))

    def update(self):
        [repository.update() for repository in self.repositories]
        self.update_store()
        
    def add_repo(self, repository):
        print("[ergo: epm]: Adding repository '%s' at '%s' to store..." % (repository.name, repository.url))
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

    def list_packages(self):
        return flatten([x.installedPackages for x in self.repositories])

    def list_repositories(self):
        return [x.name for x in self.repositories]

    def list_remotes(self):
        return ["%s: %s" % (y.name, y.description) for y in flatten([x.remotePackages for x in self.repositories])]
    
    def install_package(self, packagename):
        for repository in self.repositories:
            if repository.install_package(packagename):
                return ["[ergo: epm]: Package `%s` successfully installed." % packagename]
                                
        print("[ergo: epm]: [PackageError]: [Warning] No package `%s` found." % (packagename))
         

localStore = RepositoryCollection(PATH_TO_LOCALSTORE)

try:
    localStore.load_from_store()

except IOError:
    
    # NOTE: this does not need to be continuously updated as the instantiated RepositoryStore object
    # automatically updates itself on any changes
	 
    print("[ergo: epm]: [Info] No epm store found!")
    print("[ergo: epm]: [Info] Initializing package store at %s.." % (PATH_TO_LOCALSTORE))

    
    # add main Ergonomica repository
    localStore.add_repo(Repository("Ergonomica Main", "https://raw.githubusercontent.com/ergonomica/packages/master/MANIFEST"))


def main(argc):
    """epm: Ergonomica's package manager.

    Usage:
        epm install PACKAGES...
        epm uninstall PACKAGES...
        epm packages (local|remote)
        epm repos
        epm update
        epm add-source NAME URL
    """

    if argc.args['repos']:
        return localStore.list_repositories()

    elif argc.args['packages']:
        if argc.args['local']:
            return localStore.list_packages()
        
        elif argc.args['remote']:
            return localStore.list_remotes()
        
    elif argc.args['update']:
        localStore.update()
        return

    elif argc.args['add-source']:
        localStore.add_repository(Repository(argc.args['NAME'],
                                             argc.args['URL']))

    elif argc.args['install']:
        map(localStore.install_package, argc.args['PACKAGES'])

    elif argc.args['uninstall']:
        map(localStore.uninstall_package, argc.args['PACKAGES'])

 
