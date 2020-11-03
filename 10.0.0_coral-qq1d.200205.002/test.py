#!/usr/bin/env python3

import shutil, os.path, json, subprocess, hashlib, glob
import unittest, logging, sys, lzma

log = logging.getLogger('coral')
log.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'))
log.addHandler(consoleHandler)

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
    subprocess.check_call("./gradlew unpack", shell = True)
    subprocess.check_call("./gradlew pack", shell = True)
    unittest.TestCase().assertEqual("7d46447d06bf98e91900e303525fae70", hashFile("vbmeta.img"))
    unittest.TestCase().assertEqual("865c673b258030d97ed2ff1c3d32fa5e", hashFile("vbmeta.img.signed"))
    cleanUp()

def vbmeta_only():
    cleanUp()
    decompressXZ("src/integrationTest/resources/10.0.0_coral-qq1d.200205.002/boot.img.xz", "boot.img")
    subprocess.check_call("./gradlew unpack", shell = True)
    subprocess.check_call("./gradlew pack", shell = True)
    unittest.TestCase().assertEqual("aaf8d027cb0c165de7c66bf32f8341c1", hashFile("boot.img.google"))
    unittest.TestCase().assertEqual("0fed36e951788e49c2bcd23b95011878", hashFile("boot.img.signed"))
    unittest.TestCase().assertEqual("0fed36e951788e49c2bcd23b95011878", hashFile("boot.img.signed2"))

def boot_vbmeta():
    cleanUp()
    shutil.copyfile("src/integrationTest/resources/10.0.0_coral-qq1d.200205.002/vbmeta.img", "vbmeta.img")
    decompressXZ("src/integrationTest/resources/10.0.0_coral-qq1d.200205.002/boot.img.xz", "boot.img")
    subprocess.check_call("./gradlew unpack", shell = True)
    subprocess.check_call("./gradlew pack", shell = True)
    unittest.TestCase().assertEqual("0fed36e951788e49c2bcd23b95011878", hashFile("boot.img.signed"))
    unittest.TestCase().assertEqual("70689c8e0e576ea6cc0b4301931304ab", hashFile("vbmeta.img.signed"))
    cleanUp()

def boot_change_algorithm():
    cleanUp()
    decompressXZ("src/integrationTest/resources/10.0.0_coral-qq1d.200205.002/boot.img.xz", "boot.img")
    subprocess.check_call("./gradlew unpack", shell = True)
    # algorithm_type = 1
    subprocess.check_call(
"""
vim -u NONE build/unzip_boot/boot.avb.json -c '%s/algorithm_type"\s*:\s\+\d/algorithm_type" : 1/g' -c ':wq'
""".strip(), shell = True)
    subprocess.check_call("./gradlew pack", shell = True)
    unittest.TestCase().assertEqual("2adfd5d17b12a49b14e49a14504ab5eb", hashFile("boot.img.signed"))
    # algorithm_type = 2
    subprocess.check_call(
"""
vim -u NONE build/unzip_boot/boot.avb.json -c '%s/algorithm_type"\s*:\s\+\d/algorithm_type" : 2/g' -c ':wq'
""".strip(), shell = True)
    subprocess.check_call("./gradlew pack", shell = True)
    unittest.TestCase().assertEqual("4ecb4d4493dea6480f93502fbd5491e3", hashFile("boot.img.signed"))
    # algorithm_type = 3
    subprocess.check_call(
"""
vim -u NONE build/unzip_boot/boot.avb.json -c '%s/algorithm_type"\s*:\s\+\d/algorithm_type" : 3/g' -c ':wq'
""".strip(), shell = True)
    subprocess.check_call("./gradlew pack", shell = True)
    unittest.TestCase().assertEqual("7971607e61c7f55fa1c59c7ccbf042ac", hashFile("boot.img.signed"))
    # algorithm_type = 4
    subprocess.check_call(
"""
vim -u NONE build/unzip_boot/boot.avb.json -c '%s/algorithm_type"\s*:\s\+\d/algorithm_type" : 4/g' -c ':wq'
""".strip(), shell = True)
    subprocess.check_call("./gradlew pack", shell = True)
    unittest.TestCase().assertEqual("8e2e28b4bd69b1887ddc664ad75b99ed", hashFile("boot.img.signed"))
    # algorithm_type = 5
    subprocess.check_call(
"""
vim -u NONE build/unzip_boot/boot.avb.json -c '%s/algorithm_type"\s*:\s\+\d/algorithm_type" : 5/g' -c ':wq'
""".strip(), shell = True)
    subprocess.check_call("./gradlew pack", shell = True)
    unittest.TestCase().assertEqual("b8bdacb1131e013404996ba7ace89ad3", hashFile("boot.img.signed"))
    # algorithm_type = 6
    subprocess.check_call(
"""
vim -u NONE build/unzip_boot/boot.avb.json -c '%s/algorithm_type"\s*:\s\+\d/algorithm_type" : 6/g' -c ':wq'
""".strip(), shell = True)
    subprocess.check_call("./gradlew pack", shell = True)
    unittest.TestCase().assertEqual("c7488be18b6acaf1bd4f3191a0bbcb95", hashFile("boot.img.signed"))
    unittest.TestCase().assertEqual("c7488be18b6acaf1bd4f3191a0bbcb95", hashFile("boot.img.signed2"))

def boot_change_footer_hash_algorithm():
    cleanUp()
    decompressXZ("src/integrationTest/resources/10.0.0_coral-qq1d.200205.002/boot.img.xz", "boot.img")
    subprocess.check_call("./gradlew unpack", shell = True)
    subprocess.check_call(
"""
vim -u NONE build/unzip_boot/boot.avb.json -c '%s/hash_algorithm.*"/hash_algorithm" : "sha512"/g' -c ':wq'
""".strip(), shell = True)
    subprocess.check_call("./gradlew pack", shell = True)
    unittest.TestCase().assertEqual("5e23cf961963916b106799e2534c49fb", hashFile("boot.img.signed"))
    unittest.TestCase().assertEqual("5e23cf961963916b106799e2534c49fb", hashFile("boot.img.signed2"))

if __name__ == "__main__":
    boot_only()
    vbmeta_only()
    boot_vbmeta()
    boot_change_algorithm()
    boot_change_footer_hash_algorithm()
