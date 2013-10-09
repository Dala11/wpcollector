import zipfile
import os.path
import fnmatch
import os
import shutil
import sys
import shutil


def copyfolder(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

def upgradeVisualStudioApps():
    dir= "/Volumes/Data/CodeCorpus/WPApps/"
    analyze=False
    for x in os.listdir(dir):
        if not os.path.isdir(dir+x):
            continue
        isThereAnySln= False
        if analyze:
            for root, dirnames, filenames in os.walk(dir+x):
                for file in fnmatch.filter(filenames, '*.sln'):
                    isThereAnySln= True
                    path= os.path.join(root,file)
                    print path
                    os.system('devenv "'+ path +'" /upgrade')
            if not isThereAnySln:
                for root, dirnames, filenames in os.walk(dir+x):
                    for file in fnmatch.filter(filenames, '*.csproj'):
                        isThereAnySln= True
                        path= os.path.join(root,file)
                        print path
                        os.system('devenv "'+ path +'" /upgrade')

def RemoveUpgradeRelics():
    dir= "/Volumes/Data/CodeCorpus/WPApps/"   
    for x in os.listdir(dir):
        if not os.path.isdir(dir+x):
            continue
        deleted=False
        a=0
        for root, dirnames, filenames in os.walk(dir+x):
            for file in fnmatch.filter(dirnames, '_UpgradeReport_Files'):
                for x in os.listdir(root):
                        if x.startswith('Backup'):
                            print root+'/'+x
                            shutil.rmtree(root+'/'+x)
                            deleted=True

def findReleases():
    dir= "/Volumes/Data/CodeCorpus/WPApps/"   
    for x in os.listdir(dir):
        if not os.path.isdir(dir+x):
            continue
        found=False
        a=0

        for root, dirnames, filenames in os.walk(dir+x):
            for dirname in fnmatch.filter(dirnames, 'Release'):
                if not('Bin' in root) and not('obj' in root) and not('bin' in root):

                    for root2, dirnames2, filenames2 in os.walk(root+"/"+dirname):
                        for file in fnmatch.filter(filenames2, '*.sln'):
                            found=True
                    if found:
                        print root+"/"+dirname
                

def unzipAllDownloadedApps():
    dir= "/Volumes/Data/CodeCorpus/"
    for x in os.listdir(dir):
        f= dir+x+"/archive.zip"
        if os.path.isfile(f):
            print x
            a=1
            zfile = zipfile.ZipFile(f)
            zfile.extractall(dir+x)
            zfile.close()
            os.remove(f)


def checkWP(csproj):
    isWP=False
    for line in csproj.readlines():
        if "TargetFrameworkIdentifier" in line and "WindowsPhone" in line:
            isWP=True
        if "TargetFrameworkProfile" in line and "WindowsPhone" in line:
            isWP=True
        if "XnaPlatform" in line and "Windows Phone" in line:
            isWP=True
    return isWP



def NugetPackageRestore():
    dir= "/Volumes/Data/CodeCorpus/Refactoring/"   
    for x in os.listdir(dir):
        if not os.path.isdir(dir+x):
            continue
        for root, dirnames, filenames in os.walk(dir+x):
            for file in fnmatch.filter(filenames, '*.csproj'):
                csproj = open(os.path.join(root, file))
                csProjName= os.path.join(root, file).rsplit('/',1)[1];
                if checkWP(csproj):                
                    if os.path.isfile(root+"/packages.config"):
                        packageConfigPath= root + "/packages.config"
                        
                        
                        isSolutionFound= False;
                        for root2, dirnames2, filenames2 in os.walk(dir+x):
                            for file2 in fnmatch.filter(filenames2, '*.sln'):
                                for line in open(os.path.join(root2, file2)).readlines():
                                    if csProjName in line:
                                        isSolutionFound = True
                                        packagesFolder= root2
                                        
                        if not isSolutionFound:
                            packagesFolder = root
                        
                        print packagesFolder
                        

