[app]

# (section 1) Basic Info
title = Itachi FB Tool
package.name = itachifbtool
package.domain = org.jatin
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# (section 2) Requirements (Isse Crash Nahi Hoga)
requirements = python3, kivy==2.2.1, requests, beautifulsoup4, certifi, urllib3, idna, charset-normalizer, typing_extensions

version = 1.2
orientation = portrait

# (section 3) Permissions (Storage Fix)
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# (section 4) Android Settings
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.private_storage = True

# (section 5) Architecture
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 0
