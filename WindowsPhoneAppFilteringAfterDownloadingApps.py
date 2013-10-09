import fnmatch
import os
import shutil
import sys
import shutil


def move(root_src_dir, root_dst_dir):
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir)
        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.move(src_file, dst_dir)
    shutil.rmtree(root_src_dir)


def main():
    dir= "/Volumes/Data/CodeCorpus/WPApps/"   
    for x in os.listdir(dir):
        if not os.path.isdir(dir+x):
            continue

        isWP= False
        for root, dirnames, filenames in os.walk(dir+x):
            for file in fnmatch.filter(filenames, '*.csproj'):
                csproj = open(os.path.join(root, file))
                temp=False
                isWP= checkWP(csproj)
                
                if isWP:
                    print file
                    break
            if isWP:
                break
        if isWP:
            print x
            src= dir+x
            dst= "/Volumes/Data/WPApps/"+x
            #move(src,dst)

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

def removeNonWPAppsFromList():
    dir= "/Volumes/Data/CodeCorpus/WPApps/"
    c=1
    for line in open("githubapps.txt").readlines():
        name = line.split(",")[0]
        if name != "name":
            if os.path.isdir(dir+name.replace('/','+')):
                temp=line.split(",")
                print temp[0]+","+temp[1]+","+temp[2]+","+temp[3]+","+temp[4]+","+" ".join(temp[5].split()).replace('\n','')
    for line in open("codeplexapps.txt").readlines():
            name = line.split(",")[0]
            if name != "name":
                if os.path.isdir(dir+name.replace('/','+')):
                    temp=line.split(",")
                    print temp[0]+","+temp[1]+","+temp[2]+","+temp[3]+","+temp[4]+","+" ".join(temp[5].split()).replace('\n','')
            
def remove():
    dir= "/Volumes/Data/CodeCorpus/WPApps/"
    c=1
    for line in open("codecorpus.txt").readlines(): 
        name = line.split(",")[0]
        if name != "name":
            if not os.path.isdir(dir+name.replace('/','+')): 
                print c
        c+=1
        
main()
       

    



