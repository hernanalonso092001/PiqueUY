[app]

# Nombre de la aplicación en el teléfono Android y en Google Play Store
title = PiqueUY Pesca Uruguay

# Nombre corto del paquete Android
package.name = piqueuy

# Dominio inverso único para Google Play Console (com.uy.piqueuy)
package.domain = com.uy

# Directorio del código fuente Python (. = raíz del proyecto)
source.dir = .

# Extensiones incluidas dentro del APK/AAB (incluye SQLite pre-cargado)
source.include_exts = py,png,jpg,kv,atlas,db,json,ttf

# Versión de la aplicación (incrementar al subir nuevas versiones a Play Store)
version = 1.0.0

# Dependencias Python que se empaquetan nativamente con python-for-android
requirements = python3,kivy==2.3.1,sqlite3,openssl,certifi

# Orientación vertical nativa (como FishMan)
orientation = portrait

# Pantalla completa en Android (sin barras de navegador)
fullscreen = 0

# Color de la pantalla de carga en Android (Sonar Obsidian)
presplash.color = #090D0B

# Permisos de Android requeridos (GPS Offline, Internet para sincronizar piques y Cámara para Escáner de Peces)
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,CAMERA

# API de Android requerida por Google Play Store (Android 14 / API 34)
android.api = 34

# Mínima versión de Android soportada (Android 7.0+)
android.minapi = 24

# Versión del NDK estable para Kivy 2.3.1
android.ndk = 25b

# Aceptar licencias del SDK de Android automáticamente durante la compilación del APK
android.accept_sdk_license = True

# Arquitecturas de procesadores móviles modernas (64-bit y 32-bit exigidas por Google Play Store)
android.archs = arm64-v8a, armeabi-v7a

# Permitir copia de seguridad de la base SQLite de bitácora del usuario
android.allow_backup = True

# Formato de salida cuando se compila en modo release (aab para Google Play Console, apk para instalar directo)
android.release_artifact = aab

[buildozer]
# Nivel de registro (2 = detallado para ver el progreso de compilación del APK)
log_level = 2
warn_on_root = 1
