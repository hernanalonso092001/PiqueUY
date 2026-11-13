# Base de datos SQLite Offline y modelos de pesca en Uruguay para PiqueUY (Android Python)

import sqlite3
import os

DB_FILENAME = "piqueuy_offline.db"

URUGUAY_SPOTS = [
    {
        "id": "mvd-escollera",
        "name": "Escollera Sarandí y Canal Sur",
        "department": "Montevideo",
        "water_type": "Estuario Salobre",
        "lat": -34.9125,
        "lng": -56.2128,
        "map_x": 0.48,
        "map_y": 0.87,
        "fish_score": 91,
        "score_label": "PIQUE FIRME",
        "temp_air": 22.0,
        "temp_water": 19.5,
        "pressure_hpa": 1018,
        "pressure_trend": "Estable (Óptimo)",
        "wind_kmh": 14,
        "wind_dir": "SE (Viento de Agua)",
        "tide_state": "Creciendo · Media marea",
        "next_high": "14:40 hs (1.65m)",
        "next_low": "21:15 hs (0.42m)",
        "solunar_major": "06:15-08:15 / 18:45-20:45",
        "solunar_minor": "12:30-13:30 / 00:20-01:20",
        "moon_phase": "Cuarto Creciente (64%)",
        "depth_m": "4 a 9 m",
        "bottom": "Piedra y canal de fango/arena",
        "top_baits": "Camarón atado, Almeja amarilla, Cangrejo, Filet de pejerrey",
        "species_ids": "corvina_rubia,corvina_negra,pejerrey,brotola,burriqueta",
        "field_report": "Agua verde clara con SE suave. Salen corvinas rubias de 2.5 a 3.8 kg tirando lejos al canal con plomo destrabe de 120g. A última hora entra la brótola pegada a las piedras.",
        "offline_pack_mb": 18.4,
        "downloaded": 1
    },
    {
        "id": "can-santa-lucia",
        "name": "Pozones del Río Santa Lucía",
        "department": "San José / Montevideo",
        "water_type": "Desembocadura / Estuario",
        "lat": -34.7912,
        "lng": -56.3536,
        "map_x": 0.41,
        "map_y": 0.82,
        "fish_score": 95,
        "score_label": "ÉPICO (CORVINA NEGRA)",
        "temp_air": 23.0,
        "temp_water": 20.4,
        "pressure_hpa": 1017,
        "pressure_trend": "Estable",
        "wind_kmh": 12,
        "wind_dir": "SE",
        "tide_state": "Repunte de creciente",
        "next_high": "15:10 hs (1.72m)",
        "next_low": "21:45 hs (0.38m)",
        "solunar_major": "06:16-08:16 / 18:46-20:46",
        "solunar_minor": "12:31-13:31 / 00:21-01:21",
        "moon_phase": "Cuarto Creciente (64%)",
        "depth_m": "5 a 11 m en pozón",
        "bottom": "Fango profundo, veriles y juncales",
        "top_baits": "Cangrejo caviche vivo, Camarón en racimo",
        "species_ids": "corvina_negra,corvina_rubia,bagre_marino,tararira_comun",
        "field_report": "Temporada plena de Corvina Negra en los pozones del puente y desembocadura. Encarnando con cangrejo vivo sin pinzas y destapado a un lado salieron piezas de 12 a 19 kg.",
        "offline_pack_mb": 14.2,
        "downloaded": 1
    },
    {
        "id": "sjo-kiyu",
        "name": "Barrancas de Kiyú y Arazatí",
        "department": "San José",
        "water_type": "Río de la Plata Oeste",
        "lat": -34.6950,
        "lng": -56.7820,
        "map_x": 0.33,
        "map_y": 0.79,
        "fish_score": 87,
        "score_label": "MUY BUENO",
        "temp_air": 23.0,
        "temp_water": 20.1,
        "pressure_hpa": 1016,
        "pressure_trend": "En leve alza",
        "wind_kmh": 11,
        "wind_dir": "S limpio",
        "tide_state": "Pleamar iniciando bajante",
        "next_high": "15:20 hs (1.50m)",
        "next_low": "22:00 hs (0.35m)",
        "solunar_major": "06:20-08:20 / 18:50-20:50",
        "solunar_minor": "12:35-13:35 / 00:25-01:25",
        "moon_phase": "Cuarto Creciente (64%)",
        "depth_m": "2 a 5 m (Ideal Kayak)",
        "bottom": "Arena firme y tosca",
        "top_baits": "Anchoíta, Camarón, Lombriz de mar",
        "species_ids": "bagre_marino,corvina_rubia,pejerrey,pati",
        "field_report": "A 600 metros de la costa en kayak están saliendo mimosos (bagres de mar) grandes con anchoíta atada y corvinas rubias muy combativas.",
        "offline_pack_mb": 12.8,
        "downloaded": 1
    },
    {
        "id": "mal-la-barra",
        "name": "La Barra y Punta Salinas",
        "department": "Maldonado",
        "water_type": "Océano Atlántico",
        "lat": -34.9167,
        "lng": -54.8685,
        "map_x": 0.67,
        "map_y": 0.86,
        "fish_score": 86,
        "score_label": "MUY BUENO",
        "temp_air": 20.0,
        "temp_water": 18.2,
        "pressure_hpa": 1019,
        "pressure_trend": "Subiendo",
        "wind_kmh": 16,
        "wind_dir": "E oceánico",
        "tide_state": "Creciendo firme",
        "next_high": "13:55 hs (1.40m)",
        "next_low": "20:30 hs (0.30m)",
        "solunar_major": "06:08-08:08 / 18:38-20:38",
        "solunar_minor": "12:23-13:23 / 00:13-01:13",
        "moon_phase": "Cuarto Creciente (64%)",
        "depth_m": "3 a 8 m",
        "bottom": "Piedra oceánica y banco de arena",
        "top_baits": "Mejillón atado, Pejerrey vivo, Camarón",
        "species_ids": "sargo,lenguado,pejerrey,corvina_rubia,brotola",
        "field_report": "En los pozos de espuma de Punta Salinas están saliendo sargos de más de 1.5 kg cebando con mejillón pisado. En la boca del Arroyo Maldonado pica el lenguado con pejerrey vivo.",
        "offline_pack_mb": 21.5,
        "downloaded": 1
    },
    {
        "id": "roc-la-paloma",
        "name": "Escollera La Paloma y Laguna de Rocha",
        "department": "Rocha",
        "water_type": "Mar Abierto / Albúfera",
        "lat": -34.6615,
        "lng": -54.1422,
        "map_x": 0.81,
        "map_y": 0.76,
        "fish_score": 90,
        "score_label": "EXCELENTE",
        "temp_air": 19.5,
        "temp_water": 17.8,
        "pressure_hpa": 1020,
        "pressure_trend": "Alta estable",
        "wind_kmh": 15,
        "wind_dir": "NE suave",
        "tide_state": "Media marea bajante",
        "next_high": "13:30 hs (1.35m)",
        "next_low": "20:05 hs (0.28m)",
        "solunar_major": "06:04-08:04 / 18:34-20:34",
        "solunar_minor": "12:19-13:19 / 00:09-01:09",
        "moon_phase": "Cuarto Creciente (64%)",
        "depth_m": "4 a 12 m",
        "bottom": "Canal profundo y barra de arena",
        "top_baits": "Pejerrey vivo, Lisa en tira, Camarón de Rocha, Tatuíra",
        "species_ids": "lenguado,corvina_rubia,sargo,pejerrey,burriqueta",
        "field_report": "La barra de la Laguna de Rocha está corriendo bárbaro en bajante: lenguados de 4 a 6 kg con línea corrediza y pejerrey vivo.",
        "offline_pack_mb": 24.0,
        "downloaded": 0
    },
    {
        "id": "sal-salto-grande",
        "name": "Salto Grande y Meseta de Artigas",
        "department": "Salto / Paysandú",
        "water_type": "Agua Dulce · Río Uruguay",
        "lat": -31.2740,
        "lng": -57.9310,
        "map_x": 0.19,
        "map_y": 0.24,
        "fish_score": 96,
        "score_label": "ÉPICO (DORADOS)",
        "temp_air": 27.5,
        "temp_water": 23.5,
        "pressure_hpa": 1013,
        "pressure_trend": "Estable cálida",
        "wind_kmh": 9,
        "wind_dir": "NE",
        "tide_state": "Represa turbinando parejo (Cota 34.2m)",
        "next_high": "08:00 hs (Pico caudal)",
        "next_low": "19:00 hs (Estiaje)",
        "solunar_major": "06:28-08:28 / 18:58-20:58",
        "solunar_minor": "12:43-13:43 / 00:33-01:33",
        "moon_phase": "Cuarto Creciente (64%)",
        "depth_m": "3 a 16 m",
        "bottom": "Piedra mora basáltica y correderas",
        "top_baits": "Crankbaits media agua, Morena viva, Maíz fermentado (Boga)",
        "species_ids": "dorado,surubi,boga,pati,tararira_tornasol",
        "field_report": "Actividad furiosa de dorados cazando sábalos contra los veriles de piedra. Señuelos paleta media y morena viva rinden todo el día. Bogas grandes tomando maíz.",
        "offline_pack_mb": 19.6,
        "downloaded": 1
    },
    {
        "id": "rne-andresito",
        "name": "Rincón del Bonete, San Gregorio y Andresito",
        "department": "Tacuarembó / Flores / Durazno",
        "water_type": "Agua Dulce · Río Negro",
        "lat": -32.8330,
        "lng": -56.4210,
        "map_x": 0.45,
        "map_y": 0.52,
        "fish_score": 93,
        "score_label": "EXCELENTE (TORNASOL)",
        "temp_air": 26.0,
        "temp_water": 22.8,
        "pressure_hpa": 1014,
        "pressure_trend": "Estable",
        "wind_kmh": 8,
        "wind_dir": "N calmo",
        "tide_state": "Embalse estable en bahías",
        "next_high": "Estable",
        "next_low": "Estable",
        "solunar_major": "06:22-08:22 / 18:52-20:52",
        "solunar_minor": "12:37-13:37 / 00:27-01:27",
        "moon_phase": "Cuarto Creciente (64%)",
        "depth_m": "0.8 a 6 m",
        "bottom": "Palos sumergidos y bahías vegetadas",
        "top_baits": "Ranas anti-enganche, Paseantes Zara, Hélices de superficie",
        "species_ids": "tararira_tornasol,tararira_comun,pati,pejerrey",
        "field_report": "Con el calor de la tarde las Tarariras Tornasol (Hoplias lacerdae) explotan en superficie entre los troncos secos. Recordá que rige devolución obligatoria por veda DINARA.",
        "offline_pack_mb": 16.8,
        "downloaded": 1
    }
]

FISH_SPECIES = [
    {
        "id": "corvina_rubia",
        "name": "Corvina Rubia",
        "scientific": "Micropogonias furnieri",
        "water": "Salada / Salobre",
        "avg_weight": "1.5 a 4.5 kg (Récords > 6 kg)",
        "min_cm": 35,
        "veda": "Permitida todo el año (Respetar mínimo 35 cm DINARA)",
        "season": "Octubre a Abril (Presente todo el año)",
        "habitat": "Fondos de arena, conchilla y fango del Río de la Plata y Océano Atlántico.",
        "baits": "Camarón crudo atado con hilo elástico, Almeja amarilla, Lombriz de mar, Tira de calamar",
        "gear": "Caña surfcasting 3.60 a 4.20m, plomo 110-140g destrabe, madre 0.50mm, anzuelo 3/0 a 5/0.",
        "hotspots": "Escollera Sarandí, Kiyú, Costa de Oro, Punta del Este, La Paloma",
        "id_tips": "Lomo bronceado/dorado con líneas oblicuas oscuras, boca inferior con barbillas sensoriales."
    },
    {
        "id": "corvina_negra",
        "name": "Corvina Negra (Pogonias)",
        "scientific": "Pogonias courbina",
        "water": "Salobre / Estuario",
        "avg_weight": "6 a 25 kg (Récords > 35 kg)",
        "min_cm": 50,
        "veda": "Permitida con cupo deportivo estricto",
        "season": "Octubre a Enero (Arribazón reproductiva)",
        "habitat": "Pozones fangosos y veriles de desembocaduras (Río Santa Lucía, Arroyo Pando, Solís Grande, Cufré).",
        "baits": "Cangrejo caviche vivo entero (sin pinzas y destapado un lado), Racimo grande de camarones",
        "gear": "Caña pesada 20-40 lb, madre 0.80mm, anzuelo forjado 7/0 a 9/0 capaz de aguantar su mandíbula trituradora.",
        "hotspots": "Puente y Boca del Río Santa Lucía, Boca del Pando, Boca del Solís Grande",
        "id_tips": "Color gris plomo a negro bronceado, grandes escamas nacaradas duras, ronquido característico."
    },
    {
        "id": "dorado",
        "name": "Dorado (Tigre del Río)",
        "scientific": "Salminus brasiliensis",
        "water": "Agua Dulce",
        "avg_weight": "4 a 15 kg (En Salto Grande > 20 kg)",
        "min_cm": 65,
        "veda": "Devolución obligatoria en Reserva Salto Grande / Normativa CARU 65 cm",
        "season": "Septiembre a Abril",
        "habitat": "Correderas de piedra mora, aguas rápidas oxigenadas y veriles del Río Uruguay y Río Negro.",
        "baits": "Señuelos Crankbaits de media agua, Moscas streamers grandes, Morena viva, Sábalo",
        "gear": "Caña baitcasting/spinning 15-30 lb, multifilamento 40 lb y líder de acero de 50 lb obligatorio.",
        "hotspots": "Salto Grande, Meseta de Artigas (Paysandú), Nuevo Berlín, Bella Unión",
        "id_tips": "Escamas amarillo-oro brillantes con punto negro, aleta caudal rojiza con franja central negra."
    },
    {
        "id": "tararira_tornasol",
        "name": "Tararira Tornasol (Azul)",
        "scientific": "Hoplias lacerdae",
        "water": "Agua Dulce",
        "avg_weight": "3 a 8 kg (Trofeos > 10 kg)",
        "min_cm": 45,
        "veda": "VEDA REPRODUCTIVA DINARA (1 Nov al 31 Ene: Solo Pesca y Devolución)",
        "season": "Octubre a Marzo",
        "habitat": "Cuenca del Río Negro (Rincón del Bonete, San Gregorio, Andresito), Río Tacuarembó y Río Uruguay.",
        "baits": "Paseantes de superficie (Walk the Dog), Ranas anti-enganche, Hélices, Crankbaits sub-superficie",
        "gear": "Caña 14-25 lb acción rápida, multifilamento 35 lb, líder fluorocarbono 0.70mm o acero, anzuelos simples sin rebaba.",
        "hotspots": "San Gregorio de Polanco, Andresito, Rincón del Bonete, Río Queguay",
        "id_tips": "Pliegues mandibulares inferiores paralelos en V abierta (sin tocarse) y reflejos azul/verdosos."
    },
    {
        "id": "tararira_comun",
        "name": "Tararira Común (Ñata)",
        "scientific": "Hoplias malabaricus",
        "water": "Agua Dulce",
        "avg_weight": "1 a 3.5 kg",
        "min_cm": 35,
        "veda": "Veda DINARA en aguas interiores (1 Nov al 31 Ene: Devolución)",
        "season": "Primavera y Verano",
        "habitat": "Lagunas, tajamares, arroyos vegetados y bañados de los 19 departamentos.",
        "baits": "Ranas de goma, Poppers, Cucharas anti-enganche, Posta de dientudo",
        "gear": "Equipo liviano spinning o baitcast 10-17 lb con líder corto de acero.",
        "hotspots": "Laguna del Sauce, Laguna Merín, Arroyos de Florida, Rocha y Canelones",
        "id_tips": "Pliegues bajo la mandíbula unidos en forma de Y, cabeza más corta y cuerpo cilíndrico moteado."
    },
    {
        "id": "pejerrey",
        "name": "Pejerrey (Flecha de Plata)",
        "scientific": "Odontesthes bonariensis / O. argentinensis",
        "water": "Dulce y Salada",
        "avg_weight": "0.3 a 1.4 kg (Matungos > 1.6 kg)",
        "min_cm": 25,
        "veda": "Permitida (Respetar talla mínima 25 cm)",
        "season": "Mayo a Septiembre (Invierno)",
        "habitat": "Costas rocosas y playas de Montevideo, Maldonado y Rocha; Río Uruguay, Río Negro y lagunas.",
        "baits": "Mojarra viva o salada, Camarón en tiritas, Filet de pejerrey teñido de amarillo/rojo",
        "gear": "Caña 4.00 a 4.50m, multifilamento 0.12mm flotante, aparejo de 3 boyas cometa o chupetona + puntero y ceba con aceite.",
        "hotspots": "Punta Fría (Piriápolis), Escollera Sarandí, Villa Soriano, Laguna del Sauce",
        "id_tips": "Cuerpo plateado esbelto con una inconfundible banda lateral plateada brillante en cada flanco."
    },
    {
        "id": "lenguado",
        "name": "Lenguado Costero",
        "scientific": "Paralichthys orbignyanus",
        "water": "Salada / Albúfera",
        "avg_weight": "2 a 7 kg (Trofeos en Rocha > 10 kg)",
        "min_cm": 40,
        "veda": "Permitida (Talla mínima 40 cm DINARA)",
        "season": "Noviembre a Abril",
        "habitat": "Bocas de lagunas costeras y arroyos salobres donde caza al acecho enterrado en la arena.",
        "baits": "Pejerrey vivo encarnado del labio, Lisa viva chica, Vinilos tipo Shad y Minnows",
        "gear": "Caña spinning 2.40-2.70m, plomo pasante liviano y línea con anzuelo simple + triple robador; esperar 10 segundos antes de clavar.",
        "hotspots": "Boca de Laguna de Rocha, Laguna José Ignacio, La Barra (Maldonado), Valizas",
        "id_tips": "Pez plano asimétrico con ambos ojos del lado superior marrón mimético y vientre blanco."
    },
    {
        "id": "surubi",
        "name": "Surubí Pintado y Atigrado",
        "scientific": "Pseudoplatystoma corruscans",
        "water": "Agua Dulce",
        "avg_weight": "8 a 30 kg (Gigantes > 45 kg)",
        "min_cm": 85,
        "veda": "Regulado por CARU (Talla mínima 85 cm Pintado)",
        "season": "Octubre a Abril (Especialmente de noche)",
        "habitat": "Pozones profundos y veriles de canal del Río Uruguay y bajo Río Negro.",
        "baits": "Morena viva grande, Anguila viva, Cascarudo, Señuelos de paleta larga para trolling profundo",
        "gear": "Caña pesada 30-60 lb, multifilamento 50-65 lb, anzuelo 9/0 a 10/0 con líder de acero largo.",
        "hotspots": "Paysandú, Salto, Nuevo Berlín, Fray Bentos",
        "id_tips": "Gran bagre de piel sin escamas con manchas negras circulares (Pintado) o rayas tipo cebra (Atigrado)."
    },
    {
        "id": "sargo",
        "name": "Sargo Oceánico",
        "scientific": "Diplodus argenteus",
        "water": "Agua Salada",
        "avg_weight": "0.6 a 2.2 kg",
        "min_cm": 24,
        "veda": "Permitida",
        "season": "Diciembre a Mayo",
        "habitat": "Puntas de piedra con espuma blanca y rompiente en Maldonado y Rocha.",
        "baits": "Mejillón atado con hilo elástico, Camarón, Cangrejo blando de piedra",
        "gear": "Caña de piedra 3.60m, línea de flote para espuma o plomo perdido liviano, anzuelo fuerte N° 1 o 1/0.",
        "hotspots": "Punta Salinas (Punta del Este), Punta Colorada, Cabo Polonio, Cerro Verde",
        "id_tips": "Cuerpo alto plateado comprimido, dientes incisivos frontales y mancha negra en la base de la cola."
    },
    {
        "id": "boga",
        "name": "Boga del Río Uruguay",
        "scientific": "Megaleporinus obtusidens",
        "water": "Agua Dulce",
        "avg_weight": "2 a 5 kg",
        "min_cm": 42,
        "veda": "Permitida respetando mínimo 42 cm CARU",
        "season": "Noviembre a Abril",
        "habitat": "Veriles con corriente sobre piedra o conchilla en el Río Uruguay, Río Negro y Colonia.",
        "baits": "Maíz fermentado con vainilla, Daditos de salamín o corazón vacuno, Masa dulce",
        "gear": "Caña boguera de puntera sensible 2.10m, plomo corredizo 40-60g y anzuelos chicos forjados Maruseigo 1/0.",
        "hotspots": "Salto, Paysandú, Nuevo Berlín, Carmelo y Nueva Palmira",
        "id_tips": "Cuerpo fusiforme plateado con tres manchas oscuras laterales y boca pequeña con dientes fuertes."
    },
    {
        "id": "brotola",
        "name": "Brótola",
        "scientific": "Urophycis brasiliensis",
        "water": "Salada / Salobre",
        "avg_weight": "1 a 3 kg",
        "min_cm": 30,
        "veda": "Permitida (Mínimo 30 cm)",
        "season": "Abril a Octubre (Pique nocturno)",
        "habitat": "Fondos de piedra y barro cercanos a escolleras y pozones costeros.",
        "baits": "Camarón fresco, Filet de pejerrey o anchoíta, Calamar",
        "gear": "Línea de fondo con anzuelo de pata larga 2/0 o 3/0 porque traga a fondo.",
        "hotspots": "Escollera Sarandí, Piriápolis, Punta del Este, La Paloma",
        "id_tips": "Dos largos filamentos bifurcados debajo de la garganta que usa para tantear el fondo."
    },
    {
        "id": "burriqueta",
        "name": "Burriqueta (Pescadilla de Costa)",
        "scientific": "Menticirrhus americanus",
        "water": "Salada / Salobre",
        "avg_weight": "0.5 a 1.8 kg",
        "min_cm": 25,
        "veda": "Permitida",
        "season": "Octubre a Abril",
        "habitat": "Primera y segunda canaleta de playas de arena de toda la costa uruguaya.",
        "baits": "Camarón atado, Almeja, Lombriz de mar (Nereis), Tatuíra",
        "gear": "Equipo liviano de playa, línea de 2 anzuelos N° 1 con perlita roja o amarilla flotante.",
        "hotspots": "Costa de Oro (Atlántida, San Luis, Cuchilla Alta), Playa Pascual, Maldonado",
        "id_tips": "Cuerpo alargado gris violáceo con una sola barbilla corta y rígida en la punta del mentón."
    },
    {
        "id": "pati",
        "name": "Patí",
        "scientific": "Luciopimelodus pati",
        "water": "Agua Dulce / Estuario",
        "avg_weight": "3 a 12 kg (En canales > 16 kg)",
        "min_cm": 45,
        "veda": "Permitida",
        "season": "Todo el año (Noche)",
        "habitat": "Canales profundos del Río Uruguay, Río Negro, Río Santa Lucía y Río de la Plata Oeste.",
        "baits": "Anguila viva o en posta, Sábalo en trozos, Racimo de lombrices",
        "gear": "Equipo de fondo medio-pesado, plomo corredizo 80-120g y anzuelo 5/0 a 7/0.",
        "hotspots": "Colonia, Juan Lacaze, Fray Bentos, Paysandú, Arazatí",
        "id_tips": "Color gris azulado con lunares oscuros, aleta adiposa muy larga y sin chuzas punzantes."
    },
    {
        "id": "bagre_marino",
        "name": "Bagre de Mar (Mimoso)",
        "scientific": "Genidens barbus",
        "water": "Salada / Estuario",
        "avg_weight": "2.5 a 8 kg",
        "min_cm": 40,
        "veda": "Cuidar desove e incubación bucal en primavera",
        "season": "Septiembre a Diciembre",
        "habitat": "Canales costeros de San José, Montevideo, Colonia y desembocadura del Santa Lucía.",
        "baits": "Anchoíta entera atada, Calamar, Trozo de pejerrey, Camarón",
        "gear": "Equipo firme de costa o kayak, anzuelo 5/0 a 6/0; precaución extrema con sus 3 chuzas aserradas.",
        "hotspots": "Kiyú y Arazatí, Canal de Punta Carretas, Río Santa Lucía",
        "id_tips": "Lomo gris oscuro metalizado, vientre blanco y tres espinas óseas aserradas muy peligrosas."
    }
]

INITIAL_COMMUNITY_CATCHES = [
    {
        "fisher": "Martín 'El Ruso' Pereira",
        "spot_id": "mvd-escollera",
        "spot_name": "Escollera Sarandí (Extremo Sur)",
        "species": "Corvina Rubia",
        "weight_kg": 3.8,
        "length_cm": 58,
        "bait": "Camarón fresco con hilo elástico",
        "comment": "Entró el cardumen firme pasando el faro hacia el canal. Plomo destrabe de 120g. Salieron 4 entre 2.5 y 3.8 kg.",
        "released": 0,
        "likes": 42,
        "time_ago": "Hace 45 min"
    },
    {
        "fisher": "Lucía Fernández (Kayak UY)",
        "spot_id": "can-santa-lucia",
        "spot_name": "Pozón del Puente Santa Lucía",
        "species": "Corvina Negra (Pogonias)",
        "weight_kg": 16.4,
        "length_cm": 94,
        "bait": "Cangrejo caviche vivo entero",
        "comment": "Tremendo tren en el pozón de 9 metros. 25 minutos de pelea desde el kayak y devuelta sana al agua.",
        "released": 1,
        "likes": 91,
        "time_ago": "Hace 2 h"
    },
    {
        "fisher": "Sebastián Correa",
        "spot_id": "sal-salto-grande",
        "spot_name": "Piedras de Salto Grande",
        "species": "Dorado (Tigre del Río)",
        "weight_kg": 11.2,
        "length_cm": 88,
        "bait": "Crankbait paleta media color Cardenal",
        "comment": "Los dorados están cazando sábalos contra la piedra mora. Cinco saltos limpios y devuelto al Río Uruguay.",
        "released": 1,
        "likes": 118,
        "time_ago": "Hace 3 h"
    },
    {
        "fisher": "Gonzalo Techera",
        "spot_id": "roc-la-paloma",
        "spot_name": "Boca de Laguna de Rocha",
        "species": "Lenguado Costero",
        "weight_kg": 5.1,
        "length_cm": 71,
        "bait": "Pejerrey vivo con línea corrediza",
        "comment": "En plena bajante. Llevó la línea, esperé 12 segundos a que tragara el pejerrey y clavada firme.",
        "released": 0,
        "likes": 67,
        "time_ago": "Hace 5 h"
    },
    {
        "fisher": "Diego & Facu (Hopliomaníacos)",
        "spot_id": "rne-andresito",
        "spot_name": "Bahía de los Palos — Andresito",
        "species": "Tararira Tornasol (Azul)",
        "weight_kg": 5.6,
        "length_cm": 72,
        "bait": "Paseante de superficie blanco/cabeza roja",
        "comment": "Explosión violenta en 80 cm de agua al lado de un palo seco. Anzuelos simples sin rebaba y devolución inmediata.",
        "released": 1,
        "likes": 104,
        "time_ago": "Ayer"
    }
]


class OfflineDatabase:
    def __init__(self, db_dir=None):
        self.mem_conn = None
        if db_dir is None:
            try:
                from kivy.app import App
                app = App.get_running_app()
                if app and getattr(app, "user_data_dir", None):
                    db_dir = app.user_data_dir
            except Exception:
                pass

        if not db_dir:
            db_dir = os.path.dirname(os.path.abspath(__file__))

        try:
            os.makedirs(db_dir, exist_ok=True)
            self.db_path = os.path.join(db_dir, DB_FILENAME)
            test_conn = sqlite3.connect(self.db_path)
            test_conn.close()
        except Exception:
            self.db_path = ":memory:"
            self.mem_conn = sqlite3.connect(":memory:")
            self.mem_conn.row_factory = sqlite3.Row

        self._init_db()

    def _connect(self):
        if self.mem_conn is not None:
            return self.mem_conn
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS spots (
                id TEXT PRIMARY KEY,
                name TEXT,
                department TEXT,
                water_type TEXT,
                lat REAL,
                lng REAL,
                map_x REAL,
                map_y REAL,
                fish_score INTEGER,
                score_label TEXT,
                temp_air REAL,
                temp_water REAL,
                pressure_hpa INTEGER,
                pressure_trend TEXT,
                wind_kmh INTEGER,
                wind_dir TEXT,
                tide_state TEXT,
                next_high TEXT,
                next_low TEXT,
                solunar_major TEXT,
                solunar_minor TEXT,
                moon_phase TEXT,
                depth_m TEXT,
                bottom TEXT,
                top_baits TEXT,
                species_ids TEXT,
                field_report TEXT,
                offline_pack_mb REAL,
                downloaded INTEGER
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS catches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fisher TEXT,
                spot_id TEXT,
                spot_name TEXT,
                species TEXT,
                weight_kg REAL,
                length_cm INTEGER,
                bait TEXT,
                comment TEXT,
                released INTEGER,
                likes INTEGER,
                time_ago TEXT
            )
        """)

        cur.execute("SELECT COUNT(*) as c FROM spots")
        if cur.fetchone()["c"] == 0:
            for s in URUGUAY_SPOTS:
                cur.execute("""
                    INSERT INTO spots VALUES (
                        :id, :name, :department, :water_type, :lat, :lng, :map_x, :map_y,
                        :fish_score, :score_label, :temp_air, :temp_water, :pressure_hpa,
                        :pressure_trend, :wind_kmh, :wind_dir, :tide_state, :next_high,
                        :next_low, :solunar_major, :solunar_minor, :moon_phase, :depth_m,
                        :bottom, :top_baits, :species_ids, :field_report, :offline_pack_mb, :downloaded
                    )
                """, s)

        cur.execute("SELECT COUNT(*) as c FROM catches")
        if cur.fetchone()["c"] == 0:
            for c in INITIAL_COMMUNITY_CATCHES:
                cur.execute("""
                    INSERT INTO catches (
                        fisher, spot_id, spot_name, species, weight_kg, length_cm,
                        bait, comment, released, likes, time_ago
                    ) VALUES (
                        :fisher, :spot_id, :spot_name, :species, :weight_kg, :length_cm,
                        :bait, :comment, :released, :likes, :time_ago
                    )
                """, c)
        conn.commit()
        if self.mem_conn is None:
            conn.close()

    def get_spots(self):
        conn = self._connect()
        rows = conn.execute("SELECT * FROM spots").fetchall()
        res = [dict(r) for r in rows]
        if self.mem_conn is None:
            conn.close()
        return res

    def mark_spot_downloaded(self, spot_id):
        conn = self._connect()
        conn.execute("UPDATE spots SET downloaded = 1 WHERE id = ?", (spot_id,))
        conn.commit()
        if self.mem_conn is None:
            conn.close()

    def get_catches(self):
        conn = self._connect()
        rows = conn.execute("SELECT * FROM catches ORDER BY id DESC").fetchall()
        res = [dict(r) for r in rows]
        if self.mem_conn is None:
            conn.close()
        return res

    def add_catch(self, fisher, spot_id, spot_name, species, weight_kg, length_cm, bait, comment, released=1):
        conn = self._connect()
        conn.execute("""
            INSERT INTO catches (
                fisher, spot_id, spot_name, species, weight_kg, length_cm,
                bait, comment, released, likes, time_ago
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 'Recién')
        """, (fisher, spot_id, spot_name, species, weight_kg, length_cm, bait, comment, released))
        conn.commit()
        if self.mem_conn is None:
            conn.close()
