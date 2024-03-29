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
    shutil.copyfile("src/integrationTest/resources/10.0.0_coral-qq1d.200205.002/vbmeta.img", "vbmeta.img")
    subprocess.check_call(gradleWrapper + " unpack", shell = True)
    subprocess.check_call(gradleWrapper + " pack", shell = True)
    unittest.TestCase().assertEqual("7d46447d06bf98e91900e303525fae70", hashFile("vbmeta.img"))
    unittest.TestCase().assertEqual("865c673b258030d97ed2ff1c3d32fa5e", hashFile("vbmeta.img.signed"))
    cleanUp()

def vbmeta_only():
    cleanUp()
    decompressXZ("src/integrationTest/resources/10.0.0_coral-qq1d.200205.002/boot.img.xz", "boot.img")
    subprocess.check_call(gradleWrapper + " unpack", shell = True)
    subprocess.check_call(gradleWrapper + " pack", shell = True)
    unittest.TestCase().assertEqual("a619ad39e982c83b76a407f08e82a5e1", hashFile("boot.img.google"))
    unittest.TestCase().assertEqual("078cef4c9debb2a1abfcc596e8291477", hashFile("boot.img.signed"))
    unittest.TestCase().assertEqual("078cef4c9debb2a1abfcc596e8291477", hashFile("boot.img.signed2"))

def boot_vbmeta():
    cleanUp()
    shutil.copyfile("src/integrationTest/resources/10.0.0_coral-qq1d.200205.002/vbmeta.img", "vbmeta.img")
    decompressXZ("src/integrationTest/resources/10.0.0_coral-qq1d.200205.002/boot.img.xz", "boot.img")
    subprocess.check_call(gradleWrapper + " unpack", shell = True)
    subprocess.check_call(gradleWrapper + " pack", shell = True)
    unittest.TestCase().assertEqual("078cef4c9debb2a1abfcc596e8291477", hashFile("boot.img.signed"))
    unittest.TestCase().assertEqual("5d07532769fec2003c1e4475a094e30c", hashFile("vbmeta.img.signed"))
    cleanUp()

def boot_change_algorithm():
    cleanUp()
    decompressXZ("src/integrationTest/resources/10.0.0_coral-qq1d.200205.002/boot.img.xz", "boot.img")
    subprocess.check_call(gradleWrapper + " unpack", shell = True)
    # algorithm_type = 1
    subprocess.check_call(["vim", "-u", "NONE", "-N",
        "build/unzip_boot/boot.avb.json",
        "-c", '%s/algorithm_type"\s*:\s\+\d/algorithm_type" : 1/g',
        "-c", ":wq"], shell = shellRun)
    subprocess.check_call(gradleWrapper + " pack", shell = True)
    unittest.TestCase().assertEqual("43e2e04dc59bcde1c172b0ab5c815016", hashFile("boot.img.signed"))
    # algorithm_type = 2
    subprocess.check_call(["vim", "-u", "NONE", "-N",
        "build/unzip_boot/boot.avb.json",
        "-c", '%s/algorithm_type"\s*:\s\+\d/algorithm_type" : 2/g',
        "-c", ':wq'], shell = shellRun)
    subprocess.check_call(gradleWrapper + " pack", shell = True)
    unittest.TestCase().assertEqual("e188f2865e683988e51a7d057738d04a", hashFile("boot.img.signed"))
    # algorithm_type = 3
    subprocess.check_call(["vim", "-u", "NONE", "-N",
        "build/unzip_boot/boot.avb.json",
        "-c", '%s/algorithm_type"\s*:\s\+\d/algorithm_type" : 3/g',
        "-c", ':wq'], shell = shellRun)
    subprocess.check_call(gradleWrapper + " pack", shell = True)
    unittest.TestCase().assertEqual("c2b2a9b2e587b81ced78e836b0dfaced", hashFile("boot.img.signed"))
    # algorithm_type = 4
    subprocess.check_call(["vim", "-u", "NONE", "-N",
        "build/unzip_boot/boot.avb.json",
        "-c", '%s/algorithm_type"\s*:\s\+\d/algorithm_type" : 4/g',
        "-c", ':wq'], shell = shellRun)
    subprocess.check_call(gradleWrapper + " pack", shell = True)
    unittest.TestCase().assertEqual("a392c4368e6a5e94d1b7b32483ba3914", hashFile("boot.img.signed"))
    # algorithm_type = 5
    subprocess.check_call(["vim", "-u", "NONE", "-N",
        "build/unzip_boot/boot.avb.json",
        "-c", '%s/algorithm_type"\s*:\s\+\d/algorithm_type" : 5/g',
        "-c", ':wq'], shell = shellRun)
    subprocess.check_call(gradleWrapper + " pack", shell = True)
    unittest.TestCase().assertEqual("832f12556acb4979fcf8ea556064d95e", hashFile("boot.img.signed"))
    # algorithm_type = 6
    subprocess.check_call(["vim", "-u", "NONE", "-N",
        "build/unzip_boot/boot.avb.json",
        "-c", '%s/algorithm_type"\s*:\s\+\d/algorithm_type" : 6/g',
        "-c", ':wq'], shell = shellRun)
    subprocess.check_call(gradleWrapper + " pack", shell = True)
    unittest.TestCase().assertEqual("e17f440c19b52a072328f7da09a2b5c4", hashFile("boot.img.signed"))
    unittest.TestCase().assertEqual("e17f440c19b52a072328f7da09a2b5c4", hashFile("boot.img.signed2"))

def boot_change_footer_hash_algorithm():
    cleanUp()
    decompressXZ("src/integrationTest/resources/10.0.0_coral-qq1d.200205.002/boot.img.xz", "boot.img")
    subprocess.check_call(gradleWrapper + " unpack", shell = True)
    subprocess.check_call(["vim", "-u", "NONE", "-N",
        "build/unzip_boot/boot.avb.json",
        "-c", '%s/hash_algorithm.*"/hash_algorithm" : "sha512"/g',
        "-c", ":wq"], shell = shellRun)
    subprocess.check_call(gradleWrapper + " pack", shell = True)
    unittest.TestCase().assertEqual("13fe1ffe8f13dc94eda387d1d65099e9", hashFile("boot.img.signed"))
    unittest.TestCase().assertEqual("13fe1ffe8f13dc94eda387d1d65099e9", hashFile("boot.img.signed2"))

if __name__ == "__main__":
    boot_only()
    vbmeta_only()
    boot_vbmeta()
    boot_change_algorithm()
    boot_change_footer_hash_algorithm()
