#!/usr/bin/env python3

import shutil, os.path, json, subprocess, hashlib, glob
import unittest, logging, sys, lzma

log = logging.getLogger('coral')
log.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'))
log.addHandler(consoleHandler)
if sys.platform == "win32":
    gradleWrapper = "gradlew.bat"
    shellRun = True
else:
    gradleWrapper = "./gradlew"
    shellRun = False

def decompressXZ(inFile, outFile):
    with lzma.open(inFile) as f:
        file_content = f.read()
        with open(outFile, "wb") as f2:
            f2.write(file_content)

def deleteIfExists(inFile):
    if os.path.isfile(inFile):
        os.remove(inFile)

def cleanUp():
    log.info("clean up ...")
    shutil.rmtree("build", ignore_errors = True)
    deleteIfExists("boot.img")
    deleteIfExists("boot.img.clear")
    deleteIfExists("boot.img.google")
    deleteIfExists("boot.img.signed")
    deleteIfExists("boot.img.signed2")
    deleteIfExists("recovery.img")
    deleteIfExists("recovery.img.clear")
    deleteIfExists("recovery.img.google")
    deleteIfExists("recovery.img.signed")
    deleteIfExists("recovery.img.signed2")
    deleteIfExists("vbmeta.img")
    deleteIfExists("vbmeta.img.signed")

def hashFile(fileName):
    hasher = hashlib.md5()
    with open(fileName, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    return hasher.hexdigest()

def boot_only():
    cleanUp()
    decompressXZ("src/integrationTest/resources/issue_52/twrp-3.5.0_10-1-coral.img.xz", "boot.img")
    subprocess.check_call(gradleWrapper + " unpack", shell = True)
    cleanUp()

if __name__ == "__main__":
    boot_only()
