[app]

title = PiqueUY Pesca Uruguay
package.name = piqueuy
package.domain = com.uy
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db,json,ttf
source.exclude_dirs = .venv,.github,bin,.buildozer,__pycache__
version = 1.0.0

# Dependencias nativas probadas con python-for-android 2024.01.21
requirements = python3,kivy==2.3.0,sqlite3,openssl,certifi

orientation = portrait
fullscreen = 0
presplash.color = #090D0B

android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,CAMERA

# Configuración blindada para GitHub Actions + Google Play Store (API 34)
android.api = 34
android.minapi = 24
android.ndk = 25b
android.ndk_api = 24
android.accept_sdk_license = True
android.archs = arm64-v8a
android.allow_backup = True

# Fijar versión estable de python-for-android
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 0
