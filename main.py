# -*- coding: utf-8 -*-
"""
PiqueUY - Lanzador seguro para Android.
Este archivo es minimo a proposito: NO importa nada pesado al inicio, asi que si cualquier
parte de la app falla (import, KV, base de datos), el error se MUESTRA EN PANTALLA y se guarda
en un archivo de texto, en lugar de cerrar la app sin explicacion.
"""

import os
import sys
import traceback

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView


def _write_crash_log(app, text):
    """Guarda el error en el almacenamiento interno de la app (y en Descargas si se puede)."""
    paths = []
    try:
        paths.append(os.path.join(app.user_data_dir, "crash_log.txt"))
    except Exception:
        pass
    for p in paths:
        try:
            with open(p, "w", encoding="utf-8") as f:
                f.write(text)
        except Exception:
            pass


def _error_screen(text):
    sv = ScrollView()
    lbl = Label(
        text=text,
        font_size="12sp",
        color=(1, 0.45, 0.3, 1),
        size_hint_y=None,
        padding=(dp(12), dp(24)),
    )
    lbl.bind(
        width=lambda i, v: setattr(i, "text_size", (v, None)),
        texture_size=lambda i, v: setattr(i, "height", v[1] + dp(60)),
    )
    sv.add_widget(lbl)
    return sv


class PiqueUYMobileApp(App):
    title = "PiqueUY - Pesca & Sonar Uruguay"

    def build(self):
        try:
            from app_core import build_root
            return build_root(self.user_data_dir)
        except Exception:
            err = (
                "PIQUEUY - ERROR DE ARRANQUE (sacale captura a esta pantalla)\n\n"
                "Python: %s\n\n%s" % (sys.version.split()[0], traceback.format_exc())
            )
            _write_crash_log(self, err)
            return _error_screen(err)


if __name__ == "__main__":
    try:
        PiqueUYMobileApp().run()
    except Exception:
        # Ultimo recurso: imprime el error en logcat para poder verlo con adb
        print("PIQUEUY FATAL:\n" + traceback.format_exc())
        raise
