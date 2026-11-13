[app]

title = PiqueUY Pesca Uruguay
package.name = piqueuy
package.domain = com.uy
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db,json,ttf
version = 1.0.0

# Fijamos Python 3.11.5 y Kivy 2.3.0 para que no use Python 3.14 experimental
requirements = hostpython3==3.11.5,python3==3.11.5,kivy==2.3.0,sqlite3,openssl,certifi

orientation = portrait
fullscreen = 0
presplash.color = #090D0B

android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,CAMERA

android.api = 34
android.minapi = 24
android.ndk = 25b
android.ndk_api = 24
android.accept_sdk_license = True
android.archs = arm64-v8a
android.allow_backup = True

# Rama estable probada de python-for-android (no usa Python 3.14)
p4a.branch = release-2024.01.21

[buildozer]
log_level = 1
warn_on_root = 0
