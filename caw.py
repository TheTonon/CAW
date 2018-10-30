# -*- coding: utf-8 -*-
import optparse
import os
from urllib import urlretrieve
import urllib
from bs4 import BeautifulSoup
from tempfile import mktemp
from zipfile import ZipFile
import time
import shutil
import sys
import requests

tTime = 0

def main():
    p = optparse.OptionParser()
    p.add_option('--install', '-i', default="elvui")
    options, arguments = p.parse_args()

    global tTime
    tTime = time.time()

    if options.install == 'elvui':
        print("Installing ElvUI from official git repositories")
        elvUIURL = 'http://git.tukui.org/Elv/elvui/repository/archive.zip'
        print("Repository that's being used: http://git.tukui.org/Elv/elvui/repository/archive.zip.")
        downloadAndInstall(elvUIURL, "elvui")
    else:
        addonName = options.install
        #try:
        #    addonURL = parseAddonURL(addonName, "https://www.wowace.com")
        #else:
        #    addonURL = parseAddonURL(addonName, "https://wow.curseforge.com")
        addonURL = parseCurseURL(addonName)
        print("Downloading addon %(addonName)s") % locals()
        print(addonURL)
        downloadAndInstall(addonURL, addonName)

def downloadAndInstall(url, addon):
    print("Creating temporary directories and files")
    filename = mktemp('.zip')
    destDir = checkForWoWInstallation()
    print("Downloading addon.")
    name, hdrs = urlretrieve(url, filename, reporthook=dProgress)
    addon = ZipFile(filename)
    print("\nExtracting files.")
    start_time = time.time()
    addon.extractall(destDir)
    print("Extraction done in %s seconds." % (time.time() - start_time))
    start_time = time.time()
    try:
        print("Excluding old files")
        if addon == "elvui":
            shutil.rmtree(destDir+'/ElvUI/')
            shutil.rmtree(destDir+'/ElvUI_Config/')
        else:
            shutil.rmtree(destDir+addon+'/')
    except:
        pass

    print("Exclusion done in %s seconds." % (time.time() - start_time))
    start_time = time.time()
    try:
        print "Copiando arquivos novos e retirando o lixo."
        if addon == "elvui":
            shutil.move(destDir+'/elvui.git/ElvUI/', destDir)
            shutil.move(destDir+'/elvui.git/ElvUI_Config/', destDir)
            shutil.rmtree(destDir+'/elvui.git/')
    except:
        pass

    print("Done in %s seconds." % (time.time() - start_time))
    addon.close()
    print("Installation completed.")
    print("Total running time: %s seconds." % (time.time() - tTime))

def checkForWoWInstallation():
    print "Conferindo qual a sua instalação."

    isdir = os.path.isdir

    windir86 = "c:/Program Files (x86)/World of Warcraft/"
    windir64 = "c:/Program Files/World of Warcraft/"
    osxdir = "/Applications/World of Warcraft/"
    addons = "Interface/AddOns"

    if isdir(windir86):
        print "WoW 32-bits no Windows encontrado."
        if isdir(windir86+addons):
            print "Diretório de AddOns ok."
            return windir86+addons

    elif isdir(windir64):
        print "WoW 64 bits no Windows encontrado."
        if isdir(windir64+addons):
            print "Diretório de AddOns ok."
            return windir64+addons

    elif isdir(osxdir):
        print "WoW no OSX encontrado."
        if isdir(osxdir+addons):
            print "Diretório de AddOns ok."
            return osxdir+addons

def parseAddonURL(addonName, base):
    start_time = time.time()
    linkToGo = ""
    toSearch = addonName.lower()
    urlT = urllib.urlopen("https://www.wowace.com/addons/%(toSearch)s/" % locals())
    soup = BeautifulSoup(urlT)
    countLink = 0
    for link in soup.findAll("a"):
        linkParseado = link.get("href")
        if linkParseado.startswith("/addons/%(toSearch)s/files/" % locals()):
            countLink = countLink + 1
            if countLink == 2:
                linkToGo = linkParseado
                print ("Link encontrado em %s segundos." % (time.time() - start_time))
                break

    realLink = base+linkToGo
    print realLink
    urlR = urllib.urlopen(realLink)
    soup2 = BeautifulSoup(urlR)
    for link in soup2.findAll("a"):
        linkP = link.get("href")
        if linkP.startswith("https://www.wowace.com/media/files"):
            print ("Mandou de volta em %s segundos." % (time.time() - start_time))
            return linkP
            break
    if realLink == None:
        return Exception

def parseCurseURL(addonName):
    with requests.session() as s:
        s.headers['user-agent'] = 'Mozilla/5.0'
        addon = addonName.lower()
        r = s.get('https://mods.curse.com/addons/wow/%(addon)s/download' % locals())
        soup = BeautifulSoup(r.text, 'html.parser')

        url  = soup.find('a', 'download-link')['data-href']

        return url

def dlProgress(count, blockSize, totalSize):
      percent = int(count*blockSize*100/totalSize)
      sys.stdout.write("%2d%%" % percent)
      sys.stdout.write("\b\b\b")
      sys.stdout.flush()

def dProgress(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d segundos se passaram." %
                    (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()

main()
