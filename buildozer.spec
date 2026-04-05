[app]
title = Itachi Tool V2
package.name = itachiv2
package.domain = org.itachi
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# REQUIREMENTS (Double check these)
requirements = python3, kivy==2.2.1, requests, beautifulsoup4, certifi, urllib3, idna, charset-normalizer

version = 1.2
orientation = portrait

# PERMISSIONS (Android 11+ ke liye zaroori)
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.private_storage = True

[buildozer]
log_level = 2
