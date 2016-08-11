# -*- coding: utf-8 -*-
import optparse
import os
from urllib import urlretrieve
from tempfile import mktemp
from zipfile import ZipFile
import time
import shutil
import sys

tTime = 0

def main():
    p = optparse.OptionParser()
    p.add_option('--install', '-i', default="elvui")
    options, arguments = p.parse_args()

    if options.install == 'elvui':
        print "Instalando ElvUI a partir do Git Oficial."
        global tTime
        tTime = time.time()
        elvUIURL = 'http://git.tukui.org/Elv/elvui/repository/archive.zip'
        print "Diretório da ElvUI Utilizado: http://git.tukui.org/Elv/elvui/repository/archive.zip."
        downloadAndInstall(elvUIURL)

def downloadAndInstall(url):
    print "Criando diretórios e arquivos temporários."
    filename = mktemp('.zip')
    destDir = checkForWoWInstallation()
    print "Baixando o addon."
    name, hdrs = urlretrieve(url, filename, reporthook=dProgress)
    addon = ZipFile(filename)
    print "\nExtraindo arquivos."
    start_time = time.time()
    addon.extractall(destDir)
    print ("Extração concluída em %s segundos." % (time.time() - start_time))
    start_time = time.time()
    try:
        print "Excluindo arquivos antigos."
        shutil.rmtree(destDir+'/ElvUI/')
        shutil.rmtree(destDir+'/ElvUI_Config/')
    except:
        pass

    print ("Exclusão concluída em %s segundos." % (time.time() - start_time))
    start_time = time.time()
    try:
        print "Copiando arquivos novos e retirando o lixo."
        shutil.move(destDir+'/elvui.git/ElvUI/', destDir)
        shutil.move(destDir+'/elvui.git/ElvUI_Config/', destDir)
        shutil.rmtree(destDir+'/elvui.git/')
    except:
        pass

    print ("Tudo pronto em %s segundos." % (time.time() - start_time))
    addon.close()
    print "Instalação feita com sucesso."
    print ("Tempo total da instalação: %s segundos." % (time.time() - tTime))

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
