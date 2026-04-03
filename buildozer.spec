[app]
# (section 1) Title and Package
title = AntiGravityBot
package.name = antigravity
package.domain = org.jatin

# (section 2) Source files
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# (section 3) Versioning
version = 0.1

# (section 4) Requirements (BS4 aur Requests add kar diye hain)
requirements = python3, kivy, pyjnius, requests, beautifulsoup4

# (section 5) Orientation and Permissions
orientation = portrait
fullscreen = 0
android.permissions = INTERNET, BIND_ACCESSIBILITY_SERVICE, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (section 6) Android Versions (YE SABSE ZAROORI HAI)
android.api = 33
android.minapi = 21
# android.sdk = 29 (Iske aage # laga rehne dena, Buildozer khud manage karega)
android.ndk = 25b

# (section 7) Storage and Services
android.private_storage = True
android.services = MyBotService:service.py

# (section 8) Buildozer log level
log_level = 2
warn_on_root = 0