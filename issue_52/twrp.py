#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
import os.path, subprocess, hashlib, sys, lzma
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../../.."))
import integrationTest as it

def boot_only():
    it.cleanUp()
    it.decompressXZ("src/integrationTest/resources/issue_52/twrp-3.5.0_10-1-coral.img.xz", "boot.img")
    if sys.platform == "win32":
        gradleWrapper = "gradlew.bat"
        shellRun = True
    else:
        gradleWrapper = "./gradlew"
        shellRun = False
    subprocess.check_call(gradleWrapper + " unpack", shell = True)
    subprocess.check_call(gradleWrapper + " clear", shell = True)
    it.cleanUp()

if __name__ == "__main__":
    boot_only()
