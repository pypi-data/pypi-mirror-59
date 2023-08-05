"""deploy.py"""

HELPTEXT = """
                  ----- Umpire -----

Umpire reads a properly formatted JSON deployment file to deploy files.
Examples can be found on GitHub: https://github.com/Signiant/umpire

Usage:  umpire <deployment_file>

Options:
--clear-cache, -c:   Clears the default Umpire cache of all packages
--help, -h:          Displays this help text
--repair-cache, -r:  Removes lock files from the cache
--version:           Displays the current version of Umpire

"""

# Define WindowError if we're on Linux
try:
    WindowsError
except NameError:
    WindowsError = None


import sys, os, json, time, traceback, shutil
from distutils import dir_util
from maestro.core import module
from maestro.tools import path

#Local modules
from . import fetch, cache
# from cache import CacheError

CACHE_ROOT_KEYS = ["c", "with-cache"]
HELP_KEYS = ["h", "help"]

## The following code


## The following code backports an islink solution for windows in python 2.7.x
## It gets assigned to a function called "islink"
def islink_windows(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            FILE_ATTRIBUTE_REPARSE_POINT = 0x0400
            attributes = ctypes.windll.kernel32.GetFileAttributesW(unicode(path))
            return (attributes & FILE_ATTRIBUTE_REPARSE_POINT) > 0
        else:
            command = ['dir', path]
            try:
                with open(os.devnull, 'w') as NULL_FILE:
                    o0 = check_output(command, stderr=NULL_FILE, shell=True)
            except CalledProcessError as e:
                print (e.output)
                return False
            o1 = [s.strip() for s in o0.split('\n')]
            if len(o1) < 6:
                return False
            else:
                return 'SYMLINK' in o1[5]
    else:
        return False

islink = os.path.islink
if os.name == "nt":
    import ctypes
    from subprocess import CalledProcessError, check_output
    islink = islink_windows

class DeploymentError(Exception):
    pass

class DeploymentModule(module.AsyncModule):
    # Required ID of this module
    id = "deploy"

    #Cache Root
    cache_root = None

    #Deployment File
    deployment_file = None

    #Set to true to view tracebacks for exceptions
    DEBUG = False

    def help(self):
        print(self.help_text)
        exit(0)

    def run(self,kwargs):
        try:
            with open(self.deployment_file) as f:
                data = json.load(f)
        except TypeError:
            print(HELPTEXT)
            sys.exit(1)
        except IOError as e:
            if not self.DEBUG:
                print("Unable to locate file: " + self.deployment_file)
            else:
                raise e
            sys.exit(1)

        fetchers = list()

        for repo in data:
            repo_url = repo["url"]
            for item in repo["items"]:

                #Required parameters
                name = item["name"]
                version = item["version"]
                platform = item["platform"]
                destination = os.path.expandvars(item["destination"])

                #Optional parameters
                link = True
                try:
                    link = item["link"]
                except KeyError:
                    #Debugging logging
                    pass
                unpack = True
                try:
                    unpack = item["unpack"]
                except KeyError:
                    #Debugging logging
                    pass
                keep_updated = False
                try:
                    keep_updated = item["keep_updated"]
                except KeyError:
                    pass

                #Configure a Fetch module for each entry
                fetcher = fetch.FetchModule(None)
                fetcher.dependency_name = name
                fetcher.dependency_version = version
                fetcher.dependency_platform = platform
                fetcher.dependency_repo = repo_url
                fetcher.dependency_is_link = link
                fetcher.dependency_unpack = unpack
                fetcher.cache_root = self.cache_root
                fetcher.keep_updated = keep_updated
                fetcher.DEBUG = self.DEBUG
                #TODO: Figure out how to move this out of deploy
                try:
                    cache_dir =  os.path.join(fetcher.cache_root, fetcher.get_cache_name())
                    cache.create_local_cache(cache_dir, repo_url)
                except cache.CacheError:
                    pass #Cache already exists
                fetcher.start()
                fetchers.append((fetcher,destination))

        done_count = 0
        exit_code = 0
        while done_count < len(fetchers):
            done_count = 0
            for fetcher, destination in fetchers:
                if fetcher.status == module.PROCESSED:
                    done_count += 1
                    continue
                if not os.path.exists(destination):
                    try:
                        os.makedirs(destination)
                    except OSError as e:
                        if(self.DEBUG):
                            traceback.print_exc()
                        raise DeploymentError(fetcher.format_entry_name() + ": Error attempting to create destination directories.")

                if fetcher.status == module.DONE and fetcher.exception is not None:
                    if self.DEBUG:
                        print (fetcher.exception.traceback)
                    else:
                        print (fetcher.format_entry_name() + ": ERROR -- " + str(fetcher.exception))
                    exit_code = 1
                    fetcher.status = module.PROCESSED
                if fetcher.status == module.DONE and fetcher.exception is None:
                    files = fetcher.result[0]
                    state = fetcher.result[1]
                    for entry in files:
                        destination_file = os.path.join(destination,os.path.split(entry)[1])

                        # If the file exists, and points to the same target as the entry
                        if (os.path.exists(destination_file) and islink(destination_file) and state == fetch.EntryState.CACHE and os.path.realpath(entry) == os.path.realpath(destination_file)):
                            print (fetcher.format_entry_name() + ": Already deployed.")
                            fetcher.status = module.PROCESSED
                            break

                        # If the file exists, but something changed between the entry and the destination_file
                        elif (os.path.exists(destination_file) and (state == fetch.EntryState.UPDATED or state == fetch.EntryState.CACHE or state == fetch.EntryState.DOWNLOADED)):
                            print (fetcher.format_entry_name() + ": Updating " + destination_file)
                            self.__remove_and_deploy_to_destination__(fetcher, entry, destination_file)

                        # Wasn't in the cache, or updated.
                        else:
                            print (fetcher.format_entry_name() + ": Deploying " + destination_file)
                            self.__remove_and_deploy_to_destination__(fetcher, entry, destination_file)
                        #TODO: Kinda hacky, no significance other than to make it not DONE
                        fetcher.status = module.PROCESSED

                if fetcher.status == module.PROCESSED:
                    done_count += 1
            time.sleep(0.1)
        return exit_code

    def __remove_and_deploy_to_destination__(self, fetcher, entry, destination_file):
        if os.path.exists(destination_file):
            try:
                if os.path.isdir(destination_file) and not islink(destination_file):
                    try:
                        os.rmdir(destination_file)
                    except OSError as e:
                        shutil.rmtree(destination_file)
                else:
                    os.unlink(destination_file)
            except OSError as e:
                if(self.DEBUG):
                    traceback.print_exc()
                    raise DeploymentError(fetcher.format_entry_name() + ": Unable to remove previously deployed file: " + str(destination_file))
        try:
            if fetcher.dependency_is_link:
                path.symlink(entry, destination_file)
            elif os.path.isdir(entry):
                dir_util.copy_tree(entry, destination_file)
            else:
                shutil.copyfile(entry, destination_file)
        except WindowsError as e:
            if(self.DEBUG):
                traceback.print_exc()
                raise DeploymentError(fetcher.format_entry_name() + ": Unable to create symlink. Ensure you are running Umpire as an administrator or otherwise enabled your user to create symlinks. Contact your system administrator if this problem persists.")
        except OSError as e:
            if(self.DEBUG):
                traceback.print_exc()
                raise DeploymentError(fetcher.format_entry_name() + ": Unable to create symlink: " + str(e))

