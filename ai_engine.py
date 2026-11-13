# Motor de Inteligencia Artificial y Escáner Biométrico DINARA en Python puro
# Usa urllib.request nativo para ser 100% compatible con compilación Android APK (Buildozer / Flet)

import json
import urllib.request
import urllib.error


class BaqueanoAIEngine:
    def __init__(self, api_key=""):
        self.api_key = api_key.strip()

    def set_api_key(self, key: str):
        self.api_key = key.strip()

    def ask_tactical_coach(self, question: str, spot: dict) -> str:
        q = question.lower().strip()

        # Si el usuario cargó una clave de Gemini API, consulta en vivo vía HTTPS nativo
        if self.api_key:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.api_key}"
                prompt = (
                    f"Eres 'El Baqueano', guía profesional de pesca en Uruguay en la app Android PiqueUY.\n"
                    f"Spot actual: {spot['name']} ({spot['department']}).\n"
                    f"Fish Score: {spot['fish_score']}/100 ({spot['score_label']}).\n"
                    f"Clima: Aire {spot['temp_air']}°C, Agua {spot['temp_water']}°C, "
                    f"Presión {spot['pressure_hpa']} hPa ({spot['pressure_trend']}), "
                    f"Viento {spot['wind_dir']} a {spot['wind_kmh']} km/h.\n"
                    f"Marea/Río: {spot['tide_state']}.\n"
                    f"Responde en máximo 5 puntos concretos con medidas de nylon/multifilamento, anzuelos, plomo y carnada.\n"
                    f"Pregunta del pescador: {question}"
                )
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}]
                }
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=8) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts and "text" in parts[0]:
                            return parts[0]["text"]
            except Exception:
                pass  # Si no hay internet en el río, cae automáticamente al motor experto offline

        # MOTOR EXPERTO OFFLINE (Funciona en el medio del Río Negro o costa sin señal 4G)
        if "corvina negra" in q or "cangrejo" in q or "santa luc" in q:
            return (
                f"TÁCTICA CORVINA NEGRA — {spot['name'].upper()}\n"
                f"• Pozo y Marea: Buscá los veriles de 6 a 10m en el repunte de pleamar ({spot['next_high']}).\n"
                f"• Línea: Madre 0.80mm, brazolada corta 45cm en 0.70mm, anzuelo forjado 8/0 o 9/0.\n"
                f"• Encarne: Cangrejo caviche vivo sin pinzas; levantale apenas un lateral del caparazón para que largue olor y atalo firme con hilo elástico.\n"
                f"• Talla Mínima DINARA: 50 cm."
            )

        if "tararira" in q or "tornasol" in q or "rana" in q:
            return (
                f"TÁCTICA TARARIRA TORNASOL — {spot['name'].upper()}\n"
                f"• Alerta DINARA: Del 1° Nov al 31 Ene rige Veda Reproductiva (solo Captura y Devolución).\n"
                f"• Señuelos Hoy: Con agua a {spot['temp_water']}°C usá paseantes (Walk the Dog) y ranas de goma anti-enganche rozando los palos sumergidos.\n"
                f"• Equipo: Caña rápida 14-25 lb, multifilamento 35 lb, líder fluorocarbono 0.70mm o cable de acero y anzuelos simples sin rebaba."
            )

        if "dorado" in q or "salto" in q or "morena" in q:
            return (
                f"TÁCTICA DORADO — RÍO URUGUAY\n"
                f"• Condición: Agua en {spot['temp_water']}°C y represa moviendo caudal.\n"
                f"• Artificiales: Crankbaits de media agua color cardenal o amarillo/negro golpeando la piedra mora.\n"
                f"• Carnada: Morena viva con anzuelo circular 8/0 y líder de acero de 50 lb al garete controlado.\n"
                f"• Regla CARU: Devolución obligatoria en zona de seguridad; mínimo 65 cm fuera de reserva."
            )

        if "pejerrey" in q or "boya" in q:
            return (
                f"TÁCTICA PEJERREY — FLECHA DE PLATA\n"
                f"• Aparejo: 3 boyas cometa o chupetona con puntero cargado; brazoladas de 25, 40 y 55 cm en fluorocarbono 0.24mm.\n"
                f"• Anzuelo y Carnada: Akita Kitsune 2/0 encarnado con mojarra o filet del propio pejerrey teñido de amarillo.\n"
                f"• Secreto: Armá calle de ceba con aceite de pescado y pan rallado."
            )

        return (
            f"PARTE TÁCTICO OFFLINE — {spot['name'].upper()}\n"
            f"• Fish Score Actual: {spot['fish_score']}/100 ({spot['score_label']})\n"
            f"• Barómetro y Viento: {spot['pressure_hpa']} hPa ({spot['pressure_trend']}) · {spot['wind_dir']} {spot['wind_kmh']} km/h\n"
            f"• Carnadas N°1 Hoy: {spot['top_baits']}\n"
            f"• Ventana Solunar Mayor: {spot['solunar_major']}\n"
            f"• Reporte de costa: {spot['field_report']}"
        )
