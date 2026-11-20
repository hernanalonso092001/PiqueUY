# -*- coding: utf-8 -*-
"""
PIQUE UY — Aplicación Móvil Nativa en Python (Kivy OpenGL) para Android APK / AAB
Estética táctica inspirada en FishMan - Fishing Spots (Sonar Obsidian + Chartreuse + Boya Orange).
Incluye manejo blindado de almacenamiento interno de Android (user_data_dir) y protector de errores en pantalla.
"""

import os
import traceback

from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Line, Ellipse, RoundedRectangle

from uruguay_data import OfflineDatabase, FISH_SPECIES
from ai_engine import BaqueanoAIEngine


KV_INTERFACE = """
#:import dp kivy.metrics.dp

<DarkCard@BoxLayout>:
    orientation: "vertical"
    padding: dp(12)
    spacing: dp(6)
    size_hint_y: None
    height: self.minimum_height
    canvas.before:
        Color:
            rgba: 0.063, 0.086, 0.078, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(14)]
        Color:
            rgba: 0.149, 0.200, 0.176, 1
        Line:
            rounded_rectangle: (self.x, self.y, self.width, self.height, dp(14))
            width: 1.1

<TagButton@Button>:
    background_normal: ""
    background_color: (0, 0, 0, 0)
    color: (0.03, 0.05, 0.04, 1) if self.state == "down" else (0.85, 0.90, 0.87, 1)
    font_size: "12sp"
    bold: True
    size_hint_y: None
    height: dp(34)
    canvas.before:
        Color:
            rgba: (0.722, 1.0, 0.173, 1) if self.state == "down" else (0.09, 0.125, 0.11, 1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(10)]
        Color:
            rgba: (0.722, 1.0, 0.173, 1) if self.state == "down" else (0.18, 0.24, 0.21, 1)
        Line:
            rounded_rectangle: (self.x, self.y, self.width, self.height, dp(10))
            width: 1

<NavButton@Button>:
    background_normal: ""
    background_color: (0, 0, 0, 0)
    font_size: "11sp"
    bold: True
    markup: True

<RootLayout>:
    orientation: "vertical"
    canvas.before:
        Color:
            rgba: 0.035, 0.051, 0.043, 1
        Rectangle:
            pos: self.pos
            size: self.size

    # CABECERA TACTICA SUPERIOR
    BoxLayout:
        size_hint_y: None
        height: dp(56)
        padding: [dp(12), dp(8)]
        spacing: dp(8)
        canvas.before:
            Color:
                rgba: 0.055, 0.078, 0.070, 1
            Rectangle:
                pos: self.pos
                size: self.size
            Color:
                rgba: 0.12, 0.16, 0.14, 1
            Line:
                points: [self.x, self.y, self.right, self.y]
                width: 1

        Label:
            text: "PUY"
            bold: True
            font_size: "13sp"
            color: 0.03, 0.05, 0.04, 1
            size_hint: None, None
            size: dp(38), dp(38)
            canvas.before:
                Color:
                    rgba: 0.722, 1.0, 0.173, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [dp(10)]

        BoxLayout:
            orientation: "vertical"
            spacing: dp(1)
            Label:
                text: "PIQUE[color=b8ff2c]UY[/color] [size=10sp][color=ff7a2f]PRO[/color][/size]"
                markup: True
                bold: True
                font_size: "15sp"
                halign: "left"
                valign: "middle"
                text_size: self.size
            Label:
                text: root.current_spot_name
                font_size: "11sp"
                color: 0.58, 0.66, 0.62, 1
                halign: "left"
                valign: "middle"
                text_size: self.size
                shorten: True

        Button:
            text: "CAMBIAR SPOT"
            size_hint: None, None
            size: dp(108), dp(34)
            pos_hint: {"center_y": 0.5}
            background_normal: ""
            background_color: 0, 0, 0, 0
            color: 0.722, 1.0, 0.173, 1
            font_size: "11sp"
            bold: True
            on_release: root.open_spot_selector()
            canvas.before:
                Color:
                    rgba: 0.09, 0.13, 0.11, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [dp(9)]
                Color:
                    rgba: 0.722, 1.0, 0.173, 0.6
                Line:
                    rounded_rectangle: (self.x, self.y, self.width, self.height, dp(9))
                    width: 1

    # GESTOR DE PANTALLAS NATIVAS
    ScreenManager:
        id: sm

        # PANTALLA 1: MAPA SONAR OFFLINE (ESTILO FISHMAN)
        Screen:
            name: "mapa"
            BoxLayout:
                orientation: "vertical"

                UruguayOfflineMapWidget:
                    id: map_widget
                    size_hint_y: 0.52

                ScrollView:
                    size_hint_y: 0.48
                    do_scroll_x: False
                    BoxLayout:
                        orientation: "vertical"
                        padding: dp(12)
                        spacing: dp(8)
                        size_hint_y: None
                        height: self.minimum_height
                        canvas.before:
                            Color:
                                rgba: 0.063, 0.086, 0.078, 1
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [dp(20), dp(20), 0, 0]

                        BoxLayout:
                            size_hint_y: None
                            height: dp(58)
                            spacing: dp(10)

                            BoxLayout:
                                orientation: "vertical"
                                Label:
                                    text: root.current_spot_water + " - " + root.current_spot_dept
                                    font_size: "11sp"
                                    bold: True
                                    color: 0.722, 1.0, 0.173, 1
                                    halign: "left"
                                    text_size: self.size
                                Label:
                                    text: root.current_spot_name
                                    font_size: "15sp"
                                    bold: True
                                    color: 1, 1, 1, 1
                                    halign: "left"
                                    text_size: self.size
                                    shorten: True
                                Label:
                                    text: root.current_spot_coords
                                    font_size: "11sp"
                                    color: 0.55, 0.64, 0.59, 1
                                    halign: "left"
                                    text_size: self.size

                            BoxLayout:
                                orientation: "vertical"
                                size_hint: None, None
                                size: dp(72), dp(54)
                                padding: dp(4)
                                canvas.before:
                                    Color:
                                        rgba: 0.722, 1.0, 0.173, 1
                                    RoundedRectangle:
                                        pos: self.pos
                                        size: self.size
                                        radius: [dp(12)]
                                Label:
                                    text: str(root.current_fish_score)
                                    font_size: "22sp"
                                    bold: True
                                    color: 0.03, 0.05, 0.04, 1
                                Label:
                                    text: "FISH SCORE"
                                    font_size: "9sp"
                                    bold: True
                                    color: 0.03, 0.05, 0.04, 1

                        BoxLayout:
                            size_hint_y: None
                            height: dp(48)
                            spacing: dp(6)

                            DarkCard:
                                size_hint_y: None
                                height: dp(48)
                                padding: dp(6)
                                Label:
                                    text: "[color=889990]VIENTO[/color]\\n[b]" + root.current_wind + "[/b]"
                                    markup: True
                                    font_size: "11sp"
                                    halign: "center"
                            DarkCard:
                                size_hint_y: None
                                height: dp(48)
                                padding: dp(6)
                                Label:
                                    text: "[color=889990]BAROMETRO[/color]\\n[b]" + root.current_pressure + "[/b]"
                                    markup: True
                                    font_size: "11sp"
                                    halign: "center"
                            DarkCard:
                                size_hint_y: None
                                height: dp(48)
                                padding: dp(6)
                                Label:
                                    text: "[color=889990]AGUA[/color]\\n[b]" + root.current_temps + "[/b]"
                                    markup: True
                                    font_size: "11sp"
                                    halign: "center"

                        DarkCard:
                            Label:
                                text: "[color=ff7a2f][b]REPORTE DE COSTA Y VERIL[/b][/color]"
                                markup: True
                                font_size: "11sp"
                                size_hint_y: None
                                height: dp(18)
                                halign: "left"
                                text_size: self.size
                            Label:
                                text: root.current_field_report
                                font_size: "12sp"
                                color: 0.85, 0.90, 0.87, 1
                                size_hint_y: None
                                height: self.texture_size[1] + dp(4)
                                text_size: self.width, None
                            Label:
                                text: "[color=b8ff2c][b]Carnadas Top Hoy:[/b] " + root.current_baits + "[/color]"
                                markup: True
                                font_size: "11sp"
                                size_hint_y: None
                                height: self.texture_size[1] + dp(4)
                                text_size: self.width, None

                        BoxLayout:
                            size_hint_y: None
                            height: dp(38)
                            spacing: dp(8)
                            TagButton:
                                text: root.offline_pack_status
                                on_release: root.download_current_spot_pack()
                            TagButton:
                                text: "+ CLAVAR PIQUE GPS"
                                on_release: root.open_new_catch_modal()

        # PANTALLA 2: CLIMA IDEAL, TABLA SOLUNAR, MAREAS Y REGLA DINARA
        Screen:
            name: "clima"
            ScrollView:
                do_scroll_x: False
                BoxLayout:
                    orientation: "vertical"
                    padding: dp(12)
                    spacing: dp(10)
                    size_hint_y: None
                    height: self.minimum_height

                    DarkCard:
                        Label:
                            text: "[color=b8ff2c][b]PRONOSTICO BIOMETEOROLOGICO Y MAREAS[/b][/color]"
                            markup: True
                            font_size: "12sp"
                            size_hint_y: None
                            height: dp(20)
                            halign: "left"
                            text_size: self.size
                        Label:
                            text: root.current_spot_name + " (" + root.current_score_label + ")"
                            font_size: "15sp"
                            bold: True
                            size_hint_y: None
                            height: dp(24)
                            halign: "left"
                            text_size: self.size
                        Label:
                            text: "Marea / Nivel: " + root.current_tide_state + "\\nProxima Alta: " + root.current_next_high + "  |  Baja: " + root.current_next_low
                            font_size: "12sp"
                            color: 0.82, 0.88, 0.85, 1
                            size_hint_y: None
                            height: self.texture_size[1] + dp(6)
                            text_size: self.width, None

                    DarkCard:
                        Label:
                            text: "[color=ff7a2f][b]TABLA SOLUNAR URUGUAY - HORARIOS DE PIQUE[/b][/color]"
                            markup: True
                            font_size: "12sp"
                            size_hint_y: None
                            height: dp(20)
                            halign: "left"
                            text_size: self.size
                        Label:
                            text: "Fase Lunar: " + root.current_moon_phase + "\\n[color=b8ff2c][b]Periodos Mayores (Pico 2h):[/b][/color] " + root.current_solunar_major + "\\n[color=38bdf8][b]Periodos Menores (1h):[/b][/color] " + root.current_solunar_minor
                            markup: True
                            font_size: "12sp"
                            size_hint_y: None
                            height: self.texture_size[1] + dp(6)
                            text_size: self.width, None

                    DarkCard:
                        Label:
                            text: "[color=b8ff2c][b]REGLA DIGITAL DINARA / CARU - CONTROL DE VEDA[/b][/color]"
                            markup: True
                            font_size: "12sp"
                            size_hint_y: None
                            height: dp(22)
                            halign: "left"
                            text_size: self.size
                        Label:
                            text: "Desliza para medir tu captura en centimetros y verificar si cumple la talla minima legal:"
                            font_size: "11sp"
                            color: 0.65, 0.72, 0.68, 1
                            size_hint_y: None
                            height: self.texture_size[1] + dp(4)
                            text_size: self.width, None
                        Slider:
                            id: cm_slider
                            min: 15
                            max: 105
                            value: 42
                            step: 1
                            size_hint_y: None
                            height: dp(34)
                            on_value: root.update_dinara_ruler(self.value)
                        Label:
                            text: root.dinara_ruler_result
                            markup: True
                            font_size: "12sp"
                            size_hint_y: None
                            height: self.texture_size[1] + dp(8)
                            text_size: self.width, None

                    DarkCard:
                        Label:
                            text: "[color=ff7a2f][b]ESPECIES ACTIVAS EN ESTA ZONA[/b][/color]"
                            markup: True
                            font_size: "12sp"
                            size_hint_y: None
                            height: dp(20)
                            halign: "left"
                            text_size: self.size
                        Label:
                            text: root.current_zone_species_summary
                            markup: True
                            font_size: "12sp"
                            size_hint_y: None
                            height: self.texture_size[1] + dp(6)
                            text_size: self.width, None

        # PANTALLA 3: COACH IA "EL BAQUEANO" + ESCANER VISUAL DE PECES
        Screen:
            name: "ia"
            BoxLayout:
                orientation: "vertical"
                padding: dp(12)
                spacing: dp(8)

                DarkCard:
                    Label:
                        text: "[color=b8ff2c][b]FISH ID SCANNER & COACH TACTICO IA[/b][/color]"
                        markup: True
                        font_size: "12sp"
                        size_hint_y: None
                        height: dp(20)
                        halign: "left"
                        text_size: self.size
                    Label:
                        text: "Toca una especie para escanear su biometria y veda DINARA o preguntale al Baqueano que aparejo usar hoy:"
                        font_size: "11sp"
                        color: 0.7, 0.77, 0.73, 1
                        size_hint_y: None
                        height: self.texture_size[1] + dp(4)
                        text_size: self.width, None

                    BoxLayout:
                        size_hint_y: None
                        height: dp(34)
                        spacing: dp(6)
                        TagButton:
                            text: "Scan: Corvina"
                            on_release: root.scan_species_demo("corvina_rubia")
                        TagButton:
                            text: "Scan: Tornasol"
                            on_release: root.scan_species_demo("tararira_tornasol")
                        TagButton:
                            text: "Scan: Dorado"
                            on_release: root.scan_species_demo("dorado")

                ScrollView:
                    do_scroll_x: False
                    DarkCard:
                        Label:
                            text: root.ai_response_text
                            markup: True
                            font_size: "13sp"
                            color: 0.92, 0.95, 0.93, 1
                            size_hint_y: None
                            height: self.texture_size[1] + dp(10)
                            text_size: self.width, None

                BoxLayout:
                    size_hint_y: None
                    height: dp(34)
                    spacing: dp(6)
                    TagButton:
                        text: "Que linea pongo hoy?"
                        on_release: root.ask_baqueano("Que linea, plomo y carnada uso hoy en este pesquero?")
                    TagButton:
                        text: "Encarne Corvina Negra"
                        on_release: root.ask_baqueano("Como encarno el cangrejo para la Corvina Negra?")

                BoxLayout:
                    size_hint_y: None
                    height: dp(42)
                    spacing: dp(6)
                    TextInput:
                        id: ai_input
                        hint_text: "Preguntale al Baqueano (carnada, plomo, marea)..."
                        multiline: False
                        background_color: 0.09, 0.13, 0.11, 1
                        foreground_color: 1, 1, 1, 1
                        cursor_color: 0.722, 1.0, 0.173, 1
                        font_size: "13sp"
                        padding: [dp(10), dp(10)]
                    Button:
                        text: "ENVIAR"
                        size_hint_x: None
                        width: dp(82)
                        background_normal: ""
                        background_color: 0.722, 1.0, 0.173, 1
                        color: 0.03, 0.05, 0.04, 1
                        bold: True
                        font_size: "12sp"
                        on_release: root.submit_ai_question()

        # PANTALLA 4: ENCICLOPEDIA COMPLETA (AGUA DULCE Y SALADA)
        Screen:
            name: "enciclopedia"
            BoxLayout:
                orientation: "vertical"
                padding: dp(12)
                spacing: dp(8)

                BoxLayout:
                    size_hint_y: None
                    height: dp(36)
                    spacing: dp(6)
                    TagButton:
                        text: "TODOS (14)"
                        on_release: root.filter_species("ALL")
                    TagButton:
                        text: "MAR / PLATA"
                        on_release: root.filter_species("SALADA")
                    TagButton:
                        text: "RIOS / DULCE"
                        on_release: root.filter_species("DULCE")

                ScrollView:
                    do_scroll_x: False
                    BoxLayout:
                        id: encyclopedia_list
                        orientation: "vertical"
                        spacing: dp(8)
                        size_hint_y: None
                        height: self.minimum_height

        # PANTALLA 5: COMUNIDAD URUGUAYA + LIVE FISHING BATTLES
        Screen:
            name: "comunidad"
            BoxLayout:
                orientation: "vertical"
                padding: dp(12)
                spacing: dp(8)

                DarkCard:
                    Label:
                        text: "[color=b8ff2c][b]BATALLA DE PESCA EN VIVO - SALA #UY-884[/b][/color]"
                        markup: True
                        font_size: "12sp"
                        size_hint_y: None
                        height: dp(20)
                        halign: "left"
                        text_size: self.size
                    Label:
                        text: "1. Sebastian C. (Salto) - Dorado 88cm - [color=b8ff2c][b]1420 PTS[/b][/color]\\n2. Lucia F. (Santa Lucia) - Corvina Negra 94cm - [color=b8ff2c][b]1385 PTS[/b][/color]\\n3. Diego & Facu (Rio Negro) - Tornasol 72cm - [color=b8ff2c][b]1190 PTS[/b][/color]"
                        markup: True
                        font_size: "12sp"
                        size_hint_y: None
                        height: self.texture_size[1] + dp(4)
                        text_size: self.width, None

                BoxLayout:
                    size_hint_y: None
                    height: dp(36)
                    Label:
                        text: "[b]PIQUES DE LA COMUNIDAD URUGUAYA[/b]"
                        markup: True
                        font_size: "13sp"
                        halign: "left"
                        text_size: self.size
                    Button:
                        text: "+ PUBLICAR PIQUE"
                        size_hint_x: None
                        width: dp(130)
                        background_normal: ""
                        background_color: 1.0, 0.478, 0.184, 1
                        color: 0.03, 0.05, 0.04, 1
                        bold: True
                        font_size: "11sp"
                        on_release: root.open_new_catch_modal()

                ScrollView:
                    do_scroll_x: False
                    BoxLayout:
                        id: community_list
                        orientation: "vertical"
                        spacing: dp(8)
                        size_hint_y: None
                        height: self.minimum_height

    # BARRA DE NAVEGACION INFERIOR NATIVA DE 5 BOTONES (ESTILO FISHMAN)
    BoxLayout:
        size_hint_y: None
        height: dp(60)
        padding: [dp(6), dp(4)]
        spacing: dp(4)
        canvas.before:
            Color:
                rgba: 0.055, 0.078, 0.070, 1
            Rectangle:
                pos: self.pos
                size: self.size
            Color:
                rgba: 0.14, 0.19, 0.17, 1
            Line:
                points: [self.x, self.top, self.right, self.top]
                width: 1.1

        NavButton:
            text: "[color=b8ff2c]MAPA GPS[/color]" if sm.current == "mapa" else "[color=7f8f86]MAPA GPS[/color]"
            on_release: sm.current = "mapa"

        NavButton:
            text: "[color=b8ff2c]SOLUNAR[/color]" if sm.current == "clima" else "[color=7f8f86]SOLUNAR[/color]"
            on_release: sm.current = "clima"

        Button:
            text: "COACH IA"
            background_normal: ""
            background_color: 0, 0, 0, 0
            color: 0.03, 0.05, 0.04, 1
            bold: True
            font_size: "11sp"
            on_release: sm.current = "ia"
            canvas.before:
                Color:
                    rgba: (0.722, 1.0, 0.173, 1) if sm.current == "ia" else (1.0, 0.478, 0.184, 1)
                RoundedRectangle:
                    pos: self.x + dp(4), self.y + dp(4)
                    size: self.width - dp(8), self.height - dp(8)
                    radius: [dp(14)]

        NavButton:
            text: "[color=b8ff2c]PECES UY[/color]" if sm.current == "enciclopedia" else "[color=7f8f86]PECES UY[/color]"
            on_release: sm.current = "enciclopedia"

        NavButton:
            text: "[color=b8ff2c]CLUB / LOG[/color]" if sm.current == "comunidad" else "[color=7f8f86]CLUB / LOG[/color]"
            on_release: sm.current = "comunidad"
"""


class UruguayOfflineMapWidget(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spots = []
        self.selected_spot_id = "mvd-escollera"
        self.on_spot_selected = None
        self.bind(pos=self.redraw_map, size=self.redraw_map)

    def set_spots(self, spots, selected_id, callback):
        self.spots = spots
        self.selected_spot_id = selected_id
        self.on_spot_selected = callback
        self.redraw_map()

    def redraw_map(self, *args):
        self.canvas.before.clear()
        self.clear_widgets()

        if self.width <= 10 or self.height <= 10:
            return

        with self.canvas.before:
            Color(0.035, 0.075, 0.095, 1)
            RoundedRectangle(pos=self.pos, size=self.size)

            Color(0.10, 0.20, 0.23, 0.45)
            for i in range(1, 6):
                gx = self.x + (self.width / 6.0) * i
                Line(points=[gx, self.y, gx, self.top], width=1)
            for j in range(1, 5):
                gy = self.y + (self.height / 5.0) * j
                Line(points=[self.x, gy, self.right, gy], width=1)

            coast_norm = [
                (0.18, 0.88),
                (0.19, 0.74),
                (0.20, 0.56),
                (0.21, 0.40),
                (0.27, 0.26),
                (0.35, 0.21),
                (0.42, 0.17),
                (0.49, 0.13),
                (0.67, 0.14),
                (0.82, 0.25),
                (0.91, 0.42),
            ]
            pts_coast = []
            for nx, ny in coast_norm:
                pts_coast.extend([self.x + nx * self.width, self.y + ny * self.height])

            Color(0.722, 1.0, 0.173, 0.75)
            Line(points=pts_coast, width=dp(2.2))

            rio_negro_norm = [
                (0.21, 0.40),
                (0.34, 0.45),
                (0.46, 0.50),
                (0.64, 0.58),
            ]
            pts_rn = []
            for nx, ny in rio_negro_norm:
                pts_rn.extend([self.x + nx * self.width, self.y + ny * self.height])

            Color(0.22, 0.74, 0.97, 0.7)
            Line(points=pts_rn, width=dp(1.8))

        coord_positions = {
            "sal-salto-grande": (0.19, 0.73),
            "rne-andresito": (0.46, 0.50),
            "sjo-kiyu": (0.33, 0.23),
            "can-santa-lucia": (0.42, 0.20),
            "mvd-escollera": (0.50, 0.12),
            "mal-la-barra": (0.68, 0.14),
            "roc-la-paloma": (0.83, 0.26),
        }

        for sp in self.spots:
            nx, ny = coord_positions.get(sp["id"], (0.5, 0.5))
            px = self.x + nx * self.width
            py = self.y + ny * self.height
            is_sel = sp["id"] == self.selected_spot_id

            btn = Button(
                text=f"{sp['fish_score']} {sp['department'].split('/')[0].strip()[:6]}",
                size_hint=(None, None),
                size=(dp(88), dp(28)),
                pos=(px - dp(44), py - dp(14)),
                background_normal="",
                background_color=(0.722, 1.0, 0.173, 1) if is_sel else (0.10, 0.15, 0.13, 1),
                color=(0.03, 0.05, 0.04, 1) if is_sel else (0.95, 0.98, 0.96, 1),
                font_size="10sp",
                bold=True,
            )

            spot_ref = sp
            btn.bind(on_release=lambda inst, s=spot_ref: self.on_spot_selected(s) if self.on_spot_selected else None)
            self.add_widget(btn)


class RootLayout(BoxLayout):
    current_spot_name = StringProperty("Escollera Sarandi y Canal Sur")
    current_spot_dept = StringProperty("Montevideo")
    current_spot_water = StringProperty("Estuario Salobre")
    current_spot_coords = StringProperty("GPS -34.9125, -56.2128")
    current_fish_score = NumericProperty(91)
    current_score_label = StringProperty("PIQUE FIRME")
    current_wind = StringProperty("14 km/h SE")
    current_pressure = StringProperty("1018 hPa")
    current_temps = StringProperty("19.5 C")
    current_field_report = StringProperty("")
    current_baits = StringProperty("")
    current_tide_state = StringProperty("")
    current_next_high = StringProperty("")
    current_next_low = StringProperty("")
    current_solunar_major = StringProperty("")
    current_solunar_minor = StringProperty("")
    current_moon_phase = StringProperty("")
    offline_pack_status = StringProperty("CARTA OFFLINE ACTIVA")
    dinara_ruler_result = StringProperty("")
    current_zone_species_summary = StringProperty("")
    ai_response_text = StringProperty("")

    def __init__(self, db_dir=None, **kwargs):
        super().__init__(**kwargs)
        self.db = OfflineDatabase(db_dir=db_dir)
        self.ai = BaqueanoAIEngine()
        self.spots = self.db.get_spots()
        self.selected_spot = self.spots[0]

    def on_kv_post(self, base_widget):
        self.select_spot(self.selected_spot)
        self.update_dinara_ruler(42)
        self.filter_species("ALL")
        self.refresh_community_feed()
        self.ai_response_text = self.ai.ask_tactical_coach("parte tactico", self.selected_spot)

    def select_spot(self, spot_dict):
        self.selected_spot = spot_dict
        self.current_spot_name = spot_dict["name"]
        self.current_spot_dept = spot_dict["department"]
        self.current_spot_water = spot_dict["water_type"]
        self.current_spot_coords = f"GPS {spot_dict['lat']:.4f}S, {abs(spot_dict['lng']):.4f}W | Prof {spot_dict['depth_m']}"
        self.current_fish_score = spot_dict["fish_score"]
        self.current_score_label = spot_dict["score_label"]
        self.current_wind = f"{spot_dict['wind_kmh']} km/h {spot_dict['wind_dir'].split(' ')[0]}"
        self.current_pressure = f"{spot_dict['pressure_hpa']} hPa"
        self.current_temps = f"{spot_dict['temp_water']}C (Aire {spot_dict['temp_air']}C)"
        self.current_field_report = spot_dict["field_report"]
        self.current_baits = spot_dict["top_baits"]
        self.current_tide_state = spot_dict["tide_state"]
        self.current_next_high = spot_dict["next_high"]
        self.current_next_low = spot_dict["next_low"]
        self.current_solunar_major = spot_dict["solunar_major"]
        self.current_solunar_minor = spot_dict["solunar_minor"]
        self.current_moon_phase = spot_dict["moon_phase"]

        if spot_dict["downloaded"]:
            self.offline_pack_status = f"CARTA OFFLINE OK ({spot_dict['offline_pack_mb']} MB)"
        else:
            self.offline_pack_status = f"BAJAR CARTA ({spot_dict['offline_pack_mb']} MB)"

        ids = spot_dict["species_ids"].split(",")
        lines = []
        for sp in FISH_SPECIES:
            if sp["id"] in ids:
                lines.append(
                    f"- [b]{sp['name']}[/b] ({sp['avg_weight']}) - [color=b8ff2c]Min DINARA: {sp['min_cm']} cm[/color]"
                )
        self.current_zone_species_summary = "\n".join(lines)

        if "map_widget" in self.ids:
            self.ids.map_widget.set_spots(self.spots, spot_dict["id"], self.select_spot)

    def download_current_spot_pack(self):
        self.db.mark_spot_downloaded(self.selected_spot["id"])
        self.spots = self.db.get_spots()
        for s in self.spots:
            if s["id"] == self.selected_spot["id"]:
                self.select_spot(s)
                break

    def update_dinara_ruler(self, cm_val):
        cm = int(cm_val)
        corvina_ok = "[color=b8ff2c]LEGAL[/color]" if cm >= 35 else "[color=ff7a2f]JUVENIL (<35cm)[/color]"
        negra_ok = "[color=b8ff2c]LEGAL[/color]" if cm >= 50 else "[color=ff7a2f]JUVENIL (<50cm)[/color]"
        dorado_ok = "[color=b8ff2c]LEGAL[/color]" if cm >= 65 else "[color=ff7a2f]DEVOLVER (<65cm)[/color]"
        lenguado_ok = "[color=b8ff2c]LEGAL[/color]" if cm >= 40 else "[color=ff7a2f]JUVENIL (<40cm)[/color]"
        self.dinara_ruler_result = (
            f"[b]Medida seleccionada: [color=b8ff2c]{cm} cm[/color][/b]\n"
            f"- Corvina Rubia (35cm): {corvina_ok}   |   Lenguado (40cm): {lenguado_ok}\n"
            f"- Corvina Negra (50cm): {negra_ok}   |   Dorado CARU (65cm): {dorado_ok}"
        )

    def scan_species_demo(self, species_id):
        for sp in FISH_SPECIES:
            if sp["id"] == species_id:
                self.ai_response_text = (
                    f"[color=b8ff2c][b]ESCANER BIOMETRICO DINARA - 99.1% PRECISION[/b][/color]\n\n"
                    f"[b]Especie:[/b] {sp['name']} ({sp['scientific']})\n"
                    f"[b]Talla Minima Legal:[/b] [color=ff7a2f]{sp['min_cm']} cm[/color]\n"
                    f"[b]Estado de Veda:[/b] {sp['veda']}\n\n"
                    f"[b]Como identificarlo:[/b] {sp['id_tips']}\n\n"
                    f"[b]Aparejo recomendado:[/b] {sp['gear']}"
                )
                return

    def ask_baqueano(self, prompt_text):
        ans = self.ai.ask_tactical_coach(prompt_text, self.selected_spot)
        self.ai_response_text = f"[color=b8ff2c][b]RESPUESTA DEL BAQUEANO IA:[/b][/color]\n\n{ans}"

    def submit_ai_question(self):
        txt = self.ids.ai_input.text.strip()
        if not txt:
            return
        self.ids.ai_input.text = ""
        self.ask_baqueano(txt)

    def filter_species(self, mode):
        if "encyclopedia_list" not in self.ids:
            return
        container = self.ids.encyclopedia_list
        container.clear_widgets()
        from kivy.factory import Factory

        for sp in FISH_SPECIES:
            if mode == "SALADA" and "Salada" not in sp["water"] and "Salobre" not in sp["water"]:
                continue
            if mode == "DULCE" and "Dulce" not in sp["water"]:
                continue

            card = Factory.DarkCard()
            lbl = Factory.Label(
                text=(
                    f"[color=b8ff2c][b]{sp['name'].upper()}[/b][/color]  [i][size=11sp]({sp['scientific']})[/size][/i]\n"
                    f"[color=ff7a2f]Agua: {sp['water']}  |  Talla Minima DINARA: {sp['min_cm']} cm[/color]\n"
                    f"[b]Peso:[/b] {sp['avg_weight']}\n"
                    f"[b]Carnadas/Senuelos:[/b] {sp['baits']}\n"
                    f"[b]Equipo:[/b] {sp['gear']}\n"
                    f"[b]Pesqueros UY:[/b] {sp['hotspots']}\n"
                    f"[color=889990][b]Veda:[/b] {sp['veda']}[/color]"
                ),
                markup=True,
                font_size="12sp",
                size_hint_y=None,
            )
            lbl.bind(
                width=lambda inst, val: setattr(inst, "text_size", (val, None)),
                texture_size=lambda inst, val: setattr(inst, "height", val[1] + dp(6)),
            )
            card.add_widget(lbl)
            container.add_widget(card)

    def refresh_community_feed(self):
        if "community_list" not in self.ids:
            return
        container = self.ids.community_list
        container.clear_widgets()
        from kivy.factory import Factory

        for c in self.db.get_catches():
            card = Factory.DarkCard()
            rel_tag = "[color=b8ff2c][DEVUELTO AL AGUA][/color]" if c["released"] else "[color=38bdf8][TALLA LEGAL][/color]"
            lbl = Factory.Label(
                text=(
                    f"[b]{c['fisher']}[/b] - [color=889990]{c['time_ago']}[/color] {rel_tag}\n"
                    f"[color=ff7a2f][b]{c['species']} - {c['weight_kg']} kg ({c['length_cm']} cm)[/b][/color]\n"
                    f"Zona: {c['spot_name']}  |  Carnada: {c['bait']}\n"
                    f"\"{c['comment']}\"\n"
                    f"[color=b8ff2c]+ {c['likes']} felicitaciones de la barra[/color]"
                ),
                markup=True,
                font_size="12sp",
                size_hint_y=None,
            )
            lbl.bind(
                width=lambda inst, val: setattr(inst, "text_size", (val, None)),
                texture_size=lambda inst, val: setattr(inst, "height", val[1] + dp(6)),
            )
            card.add_widget(lbl)
            container.add_widget(card)

    def open_spot_selector(self):
        modal = ModalView(size_hint=(0.9, 0.72), background_color=(0, 0, 0, 0.85))
        box = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(8))

        for sp in self.spots:
            btn = Button(
                text=f"[{sp['fish_score']}] {sp['department'].split('/')[0].strip()} - {sp['name']}",
                background_normal="",
                background_color=(0.11, 0.15, 0.13, 1),
                color=(0.722, 1.0, 0.173, 1) if sp["id"] == self.selected_spot["id"] else (1, 1, 1, 1),
                font_size="12sp",
                bold=True,
            )
            btn.bind(on_release=lambda inst, s=sp: (self.select_spot(s), modal.dismiss()))
            box.add_widget(btn)

        modal.add_widget(box)
        modal.open()

    def open_new_catch_modal(self):
        from kivy.uix.textinput import TextInput

        modal = ModalView(size_hint=(0.92, 0.65), background_color=(0, 0, 0, 0.85))
        box = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(8))

        in_fisher = TextInput(hint_text="Tu nombre o apodo (Ej: Mati UY)", multiline=False)
        in_species = TextInput(hint_text="Especie (Ej: Corvina Rubia / Dorado)", text="Corvina Rubia", multiline=False)
        in_weight = TextInput(hint_text="Peso en kg (Ej: 3.6)", text="3.5", multiline=False)
        in_bait = TextInput(hint_text="Carnada o senuelo usado", text="Camaron atado", multiline=False)
        in_comment = TextInput(hint_text="Comentario del pique y distancia...", multiline=False)

        for w in (in_fisher, in_species, in_weight, in_bait, in_comment):
            w.background_color = (0.10, 0.14, 0.12, 1)
            w.foreground_color = (1, 1, 1, 1)
            box.add_widget(w)

        def _save(*args):
            try:
                w_kg = float(in_weight.text.strip() or "3.0")
            except ValueError:
                w_kg = 3.0
            self.db.add_catch(
                fisher=in_fisher.text.strip() or "Pescador Oriental",
                spot_id=self.selected_spot["id"],
                spot_name=self.selected_spot["name"],
                species=in_species.text.strip() or "Corvina Rubia",
                weight_kg=w_kg,
                length_cm=55,
                bait=in_bait.text.strip() or "Camaron",
                comment=in_comment.text.strip() or "Pique registrado desde GPS offline.",
                released=1,
            )
            self.refresh_community_feed()
            modal.dismiss()

        btn_save = Button(
            text="GUARDAR EN BASE OFFLINE Y MAPA",
            background_normal="",
            background_color=(0.722, 1.0, 0.173, 1),
            color=(0.03, 0.05, 0.04, 1),
            bold=True,
        )
        btn_save.bind(on_release=_save)
        box.add_widget(btn_save)
        modal.add_widget(box)
        modal.open()


def build_root(user_data_dir):
    """Construye la interfaz completa. Lo llama main.py dentro de un try/except."""
    Builder.load_string(KV_INTERFACE)
    return RootLayout(db_dir=user_data_dir)
