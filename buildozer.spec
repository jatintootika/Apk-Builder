[app]

# (section 1) Title and Package
title = Itachi FB Tool
package.name = itachifbtool
package.domain = org.jatin

# (section 2) Source files
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# (section 3) Versioning
version = 2.1

# (section 4) Requirements (Anti-Crash & HTTPS Fix)
requirements = python3, kivy==2.2.1, requests, beautifulsoup4, certifi, urllib3, idna, charset-normalizer, typing_extensions, openssl

# (section 5) Orientation and Permissions
orientation = portrait
fullscreen = 0

# Android 11+ ke liye MANAGE_EXTERNAL_STORAGE zaroori hai taaki CSV save ho sake
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# (section 6) Android Versions
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

# (section 7) Private Storage
android.private_storage = True

# (section 8) Architecture (Sabse Zaroori)
android.archs = arm64-v8a, armeabi-v7a

# (section 9) Python for Android settings
p4a.branch = master

# (section 10) Buildozer log level
log_level = 2
warn_on_root = 0

[buildozer]
# Build directory settings
build_dir = ./.buildozer
bin_dir = ./bin
