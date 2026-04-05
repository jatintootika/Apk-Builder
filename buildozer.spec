[app]
# (section 1) Title and Package
title = Itachi FB Tool
package.name = itachifbtool
package.domain = org.jatin
presplash.filename = %(source.dir)s/itachi_logo.png
icon.filename = %(source.dir)s/itachi_logo.png
presplash.color = #111111

# (section 2) Source files
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# (section 3) Versioning
version = 1.0

# (section 4) Requirements (SSL aur Certification add kiya hai)
requirements = python3, kivy==2.2.1, requests, beautifulsoup4, typing_extensions, certifi, urllib3, idna, charset-normalizer

# (section 5) Orientation and Permissions
orientation = portrait
fullscreen = 0
# Android 11+ ke liye extra permission
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# (section 6) Android Versions
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

# (section 7) Architecture (Sabse Zaroori)
android.archs = arm64-v8a, armeabi-v7a

# (section 8) Storage & Misc
android.private_storage = True
p4a.branch = master

# (section 9) Buildozer log level
log_level = 2
warn_on_root = 0

[buildozer]
log_level = 2
warn_on_root = 0
