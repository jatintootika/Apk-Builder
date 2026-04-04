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
version = 0.1

# (section 4) Requirements (Removed Pandas and openpyxl, using vanilla csv)
requirements = python3, kivy, requests, beautifulsoup4, typing_extensions

# (section 5) Orientation and Permissions
orientation = portrait
fullscreen = 0
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (section 6) Android Versions (YE SABSE ZAROORI HAI)
android.api = 33
android.minapi = 21
# android.sdk = 29 (Iske aage # laga rehne dena, Buildozer khud manage karega)
android.ndk = 25b

# (section 7) Storage
android.private_storage = True

# (section 8) Buildozer log level
log_level = 2
warn_on_root = 0