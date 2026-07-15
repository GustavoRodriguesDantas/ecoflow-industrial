"""
EcoFlow Industrial - Simulador de Linha de Produção
Matéria: Lógica de Programação
Tema: Sustentabilidade
Inspiração: N8N
"""

import pygame
import sys
import math
import random

pygame.init()

# ─── Tela ─────────────────────────────────────────────────────────────────────
W, H   = 1360, 840
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("EcoFlow Industrial - Linha de Produção Sustentavel")

SIDEBAR_W  = 300
HEADER_H   = 62
METRICS_H  = 122
BTN_AREA_H = 130  
FPS        = 60
OX, OY     = SIDEBAR_W, HEADER_H
PORT_R     = 9

# ─── Paleta ───────────────────────────────────────────────────────────────────
C = {
    "hdr"     : (14,  42,  76),
    "side"    : (18,  38,  64),
    "canvas"  : (208, 222, 238),
    "dot"     : (178, 196, 218),
    "cborder" : (148, 174, 208),
    "hline"   : (40,  86,  148),
    "sline"   : (36,  76,  132),
    "blue"    : (48,  116, 208),   "blue_d"   : (26,  82,  160),
    "orange"  : (226, 152,  24),   "orange_d" : (170, 110,   8),
    "green"   : (48,  166,  78),   "green_d"  : (26,  126,  52),
    "red"     : (210,  72,  26),   "red_d"    : (158,  48,  12),
    "yellow"  : (220, 188,  18),   "yellow_d" : (166, 136,   6),
    "teal"    : (28,  154, 148),   "teal_d"   : (14,  112, 108),
    "purple"  : (130,  60, 200),   "purple_d" : (90,   30, 150),
    "brown"   : (140,  90,  40),   "brown_d"  : (100,  60,  20),
    "port_in" : (55,  205, 100),
    "port_out": (255, 152,  38),
    "port_yes": (55,  205, 100),
    "port_no" : (215,  70,  28),
    "port_hl" : (255, 255, 100),
    "conn"    : (34,   66, 114),
    "conn_pre": (80,  160, 255),
    "anim_dot": (255, 218,  42),
    "yes"     : (48,  166,  78),
    "no"      : (210,  72,  26),
    "white"   : (255, 255, 255),
    "tdark"   : (14,   26,  46),
    "lgray"   : (188, 208, 230),
    "shadow"  : (84,  106, 138),
    "run"     : (38,  158,  58),  "run_h" : (30, 130, 48),  "run_a": (24, 106, 38),
    "rst"     : (60,   80, 110),  "rst_h" : (48,  66, 96),
    "kpi_oee" : (48,  166,  78),
    "kpi_co2" : (48,  116, 208),
    "kpi_reus": (28,  154, 148),
    "kpi_cust": (220, 188,  18),
    "mbg"     : (228, 238, 252),
    "mcard"   : (246, 250, 255),
    "mtrack"  : (185, 202, 228),
    "fb_ok"   : (38,  158,  58),
    "fb_info" : (48,  116, 208),
    "cat_bg"  : (12,  28,  52),
}

# ─── Fontes ───────────────────────────────────────────────────────────────────
def _font(size, bold=True):
    for name in ["Segoe UI", "Helvetica Neue", "Arial", "DejaVu Sans"]:
        try:
            return pygame.font.SysFont(name, size, bold=bold)
        except Exception:
            pass
    return pygame.font.Font(None, size)

F = {k: _font(s) for k, s in
     [("title",23),("h2",18),("body",15),("small",13),("tiny",11)]}

# ─── Helpers ──────────────────────────────────────────────────────────────────
def rrect(surf, col, rect, r=10, border=None, bw=2):
    if not isinstance(rect, pygame.Rect):
        rect = pygame.Rect(*rect)
    pygame.draw.rect(surf, col, rect, border_radius=r)
    if border:
        pygame.draw.rect(surf, border, rect, bw, border_radius=r)

def draw_text(surf, s, font, col, pos, anchor="topleft"):
    t = font.render(str(s), True, col)
    r = t.get_rect(**{anchor: pos})
    surf.blit(t, r)
    return t.get_size()

def circ(surf, col, pos, r, border=None, bw=2):
    pygame.draw.circle(surf, col, (int(pos[0]), int(pos[1])), r)
    if border:
        pygame.draw.circle(surf, border, (int(pos[0]), int(pos[1])), r, bw)

def dist(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

def bezier(p0, p1, p2, p3, steps=32):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = (1-t)**3*p0[0]+3*(1-t)**2*t*p1[0]+3*(1-t)*t**2*p2[0]+t**3*p3[0]
        y = (1-t)**3*p0[1]+3*(1-t)**2*t*p1[1]+3*(1-t)*t**2*p2[1]+t**3*p3[1]
        pts.append((int(x), int(y)))
    return pts

def draw_arrowhead(surf, tip, prev, col, size=11):
    dx, dy = tip[0]-prev[0], tip[1]-prev[1]
    d = math.hypot(dx, dy) or 1
    dx, dy = dx/d, dy/d
    px, py = -dy, dx
    p1 = (tip[0]-dx*size+px*size*0.45, tip[1]-dy*size+py*size*0.45)
    p2 = (tip[0]-dx*size-px*size*0.45, tip[1]-dy*size-py*size*0.45)
    pygame.draw.polygon(surf, col, [tip, p1, p2])

# ─── Icones desenhados via pygame (sem dependencia de fonte emoji) ─────────────
# Cada funcao recebe (surf, cx, cy, size, col) e desenha o icone centrado em cx,cy

def icon_mine(surf, cx, cy, s, col):        # picareta - Coletar Materia
    pygame.draw.line(surf, col, (cx-s,cy+s//2),(cx+s,cy-s//2), max(2,s//4))
    pygame.draw.circle(surf, col, (cx-s+s//3, cy+s//2-s//3), s//3)

def icon_sun(surf, cx, cy, s, col):         # sol - Energia Solar
    pygame.draw.circle(surf, col, (cx,cy), s//2, max(2,s//5))
    for a in range(0,360,45):
        r = math.radians(a)
        x1,y1 = cx+int((s//2+2)*math.cos(r)), cy+int((s//2+2)*math.sin(r))
        x2,y2 = cx+int((s-1)*math.cos(r)),    cy+int((s-1)*math.sin(r))
        pygame.draw.line(surf, col, (x1,y1),(x2,y2), max(1,s//6))

def icon_gear(surf, cx, cy, s, col):        # engrenagem - Processar
    pygame.draw.circle(surf, col, (cx,cy), s//2)
    pygame.draw.circle(surf, C["side"], (cx,cy), s//4)
    for a in range(0,360,60):
        r = math.radians(a)
        tx = cx+int((s//2)*math.cos(r)); ty = cy+int((s//2)*math.sin(r))
        pygame.draw.rect(surf, col, (tx-s//6, ty-s//6, s//3, s//3))

def icon_lens(surf, cx, cy, s, col):        # lupa - Verificar Qualidade
    pygame.draw.circle(surf, col, (cx-s//5, cy-s//5), s//2, max(2,s//5))
    pygame.draw.line(surf, col, (cx+s//6,cy+s//6),(cx+s//2,cy+s//2), max(2,s//4))

def icon_bolt(surf, cx, cy, s, col):        # raio - Verificar Desperdicio
    pts = [(cx,cy-s),(cx-s//3,cy),(cx,cy-s//6),(cx,cy+s),(cx+s//3,cy),(cx,cy+s//6)]
    pygame.draw.polygon(surf, col, pts)

def icon_recycle(surf, cx, cy, s, col):     # setas circulares - Reciclar/Reuso
    for i,a in enumerate([30,150,270]):
        r = math.radians(a)
        r2= math.radians(a+80)
        x1,y1 = cx+int(s*0.8*math.cos(r)),  cy+int(s*0.8*math.sin(r))
        x2,y2 = cx+int(s*0.8*math.cos(r2)), cy+int(s*0.8*math.sin(r2))
        pygame.draw.line(surf, col, (x1,y1),(x2,y2), max(2,s//4))

def icon_drop(surf, cx, cy, s, col):        # gota - Efluente
    pts = [(cx,cy-s),(cx+s//2,cy),(cx,cy+s//2),(cx-s//2,cy)]
    pygame.draw.polygon(surf, col, pts)

def icon_box(surf, cx, cy, s, col):         # caixa - Embalar
    r = pygame.Rect(cx-s//2, cy-s//2, s, s)
    pygame.draw.rect(surf, col, r, max(2,s//5))
    pygame.draw.line(surf, col, (cx-s//2,cy-s//6),(cx+s//2,cy-s//6), max(1,s//6))

def icon_truck(surf, cx, cy, s, col):       # caminhao - Distribuir
    pygame.draw.rect(surf, col, (cx-s,cy-s//3,int(s*1.4),s//2))
    pygame.draw.rect(surf, col, (cx+s//3,cy-s//2,s//2,s//3))
    circ(surf, col, (cx-s//2,cy+s//5), s//4)
    circ(surf, col, (cx+s//3,cy+s//5), s//4)

def icon_trash(surf, cx, cy, s, col):       # lixeira - Descartar
    pygame.draw.rect(surf, col, (cx-s//2,cy-s//3,s,int(s*0.8)))
    pygame.draw.rect(surf, col, (cx-s//3,cy-s//2,int(s*0.66),s//6))
    for ox in (-s//5,0,s//5):
        pygame.draw.line(surf, C["side"],(cx+ox,cy-s//4),(cx+ox,cy+s//3),max(1,s//7))

def icon_factory(surf, cx, cy, s, col):     # fabrica - Armazenar
    pygame.draw.rect(surf, col, (cx-s//2,cy,s,s//2))
    pts = [(cx-s//2,cy),(cx,cy-s//2),(cx+s//2,cy)]
    pygame.draw.polygon(surf, col, pts)
    pygame.draw.rect(surf, C["side"], (cx-s//6,cy+s//6,s//3,s//3))

def icon_leaf(surf, cx, cy, s, col):        # folha - Bioplastico/Compostagem
    pts = [(cx,cy-s),(cx+s,cy),(cx,cy+s//3),(cx-s,cy)]
    pygame.draw.polygon(surf, col, pts)
    pygame.draw.line(surf, C["side"],(cx,cy-s//2),(cx,cy+s//3),max(1,s//7))

def icon_bamboo(surf, cx, cy, s, col):      # bambu
    for ox in (-s//3, s//3):
        pygame.draw.line(surf, col,(cx+ox,cy-s),(cx+ox,cy+s),max(2,s//4))
    for oy in (-s//3,0,s//3):
        pygame.draw.line(surf, col,(cx-s//3,cy+oy),(cx+s//3,cy+oy),max(1,s//6))

def icon_pellet(surf, cx, cy, s, col):      # pellets - Plastico Reciclado
    for ox,oy in [(-s//3,-s//3),(s//3,-s//3),(0,0),(-s//3,s//3),(s//3,s//3)]:
        pygame.draw.circle(surf, col,(cx+ox,cy+oy),s//4)

def icon_mushroom(surf, cx, cy, s, col):    # cogumelo - Mycelium
    pygame.draw.ellipse(surf, col,(cx-s//2,cy-s//2,s,s//2))
    pygame.draw.rect(surf, col,(cx-s//6,cy,s//3,s//2))

def icon_flame(surf, cx, cy, s, col):       # chama - Pirolise
    pts = [(cx,cy-s),(cx+s//2,cy),(cx+s//4,cy-s//3),
           (cx+s//3,cy+s//2),(cx,cy+s//4),(cx-s//3,cy+s//2),
           (cx-s//4,cy-s//3),(cx-s//2,cy)]
    pygame.draw.polygon(surf, col, pts)

def icon_compost(surf, cx, cy, s, col):     # folhas empilhadas - Compostagem
    for oy in (-s//3,0,s//3):
        pygame.draw.ellipse(surf, col,(cx-s//2,cy+oy-s//5,s,s//3))

def icon_arrow_back(surf, cx, cy, s, col):  # seta volta - Logistica Reversa
    pygame.draw.arc(surf, col, (cx-s//2,cy-s//2,s,s), math.pi*0.2, math.pi*1.8, max(2,s//4))
    ax,ay = cx-s//4, cy-s//2
    pygame.draw.polygon(surf, col,[(ax,ay-s//4),(ax-s//4,ay+s//8),(ax+s//4,ay+s//8)])

def icon_wind(surf, cx, cy, s, col):        # vento - Eolica
    for oy in (-s//3,0,s//3):
        pygame.draw.arc(surf, col,(cx-s,cy+oy-s//5,s,s//3), 0, math.pi, max(2,s//5))

def icon_battery(surf, cx, cy, s, col):     # bateria - Biogas
    pygame.draw.rect(surf, col,(cx-s//2,cy-s//3,int(s*0.8),int(s*0.66)),max(2,s//5))
    pygame.draw.rect(surf, col,(cx+s//3,cy-s//6,s//6,s//3))
    pygame.draw.rect(surf, col,(cx-s//3,cy-s//5,s//3,int(s*0.4)))

def icon_cogen(surf, cx, cy, s, col):       # ondas calor - Cogeracao
    for i,oy in enumerate([-s//3,0,s//3]):
        pygame.draw.arc(surf, col,(cx-s//2,cy+oy-s//5,s,s//3),
                        math.pi*0.1,math.pi*0.9, max(2,s//5))

def icon_flask(surf, cx, cy, s, col):       # frasco - Verif. Material
    pygame.draw.rect(surf, col,(cx-s//6,cy-s//2,s//3,s//3))
    pts=[(cx-s//6,cy-s//6),(cx-s//2,cy+s//2),(cx+s//2,cy+s//2),(cx+s//6,cy-s//6)]
    pygame.draw.polygon(surf, col, pts)
    pygame.draw.rect(surf, C["side"],(cx-s//3,cy+s//6,int(s*0.66),s//4))

def icon_biohazard(surf, cx, cy, s, col):   # contaminacao
    pygame.draw.circle(surf, col,(cx,cy),s//4)
    for a in (0,120,240):
        r=math.radians(a); x=cx+int(s//2*math.cos(r)); y=cy+int(s//2*math.sin(r))
        pygame.draw.circle(surf, col,(x,y),s//3,max(2,s//5))

def icon_bottle(surf, cx, cy, s, col):      # garrafa PET
    pygame.draw.rect(surf, col,(cx-s//4,cy-s//2,s//2,s))
    pygame.draw.rect(surf, col,(cx-s//6,cy-int(s*0.6),s//3,s//8))

def icon_can(surf, cx, cy, s, col):         # lata aluminio
    pygame.draw.ellipse(surf, col,(cx-s//2,cy-s//2,s,s//3))
    pygame.draw.rect(surf, col,(cx-s//2,cy-s//3,s,int(s*0.66)))
    pygame.draw.ellipse(surf, col,(cx-s//2,cy+s//3,s,s//3))

def icon_glass(surf, cx, cy, s, col):       # vidro
    pts=[(cx-s//3,cy-s//2),(cx+s//3,cy-s//2),(cx+s//2,cy+s//2),(cx-s//2,cy+s//2)]
    pygame.draw.polygon(surf, col,pts,max(2,s//5))
    pygame.draw.line(surf,col,(cx-s//4,cy-s//4),(cx+s//4,cy-s//4),max(1,s//7))

def icon_paper(surf, cx, cy, s, col):       # papel
    pygame.draw.rect(surf, col,(cx-s//2,cy-s//2,s,s),max(2,s//5))
    for oy in (-s//4,0,s//4):
        pygame.draw.line(surf,col,(cx-s//3,cy+oy),(cx+s//3,cy+oy),max(1,s//8))

def icon_organic(surf, cx, cy, s, col):     # materia organica
    pygame.draw.ellipse(surf, col,(cx-s//2,cy-s//3,s,int(s*0.66)))
    pygame.draw.line(surf,col,(cx,cy-s//3),(cx+s//3,cy-int(s*0.6)),max(1,s//6))

def icon_chemical(surf, cx, cy, s, col):    # quimico / solvente
    pygame.draw.ellipse(surf, col,(cx-s//2,cy,s,s//2))
    pygame.draw.rect(surf, col,(cx-s//4,cy-s//2,s//2,s//2))
    pygame.draw.rect(surf, col,(cx-s//6,cy-int(s*0.6),s//3,s//8))
    pygame.draw.line(surf,col,(cx+s//4,cy-s//3),(cx+s//2,cy-s//2),max(1,s//6))

def icon_metal(surf, cx, cy, s, col):       # metal / sucata
    for ox in (-s//3,0,s//3):
        pygame.draw.rect(surf, col,(cx+ox-s//8,cy-s//2,s//4,s))
    pygame.draw.rect(surf, col,(cx-s//2,cy-s//5,s,s//3))

def icon_rubber(surf, cx, cy, s, col):      # borracha / pneu
    pygame.draw.circle(surf, col,(cx,cy),s//2,max(3,s//3))
    pygame.draw.circle(surf, col,(cx,cy),s//4)

# Mapa de ID → funcao de icone
ICON_FN = {
    "coletar"    : icon_mine,
    "solar"      : icon_sun,
    "processar"  : icon_gear,
    "qualidade"  : icon_lens,
    "desperd"    : icon_bolt,
    "reuso"      : icon_recycle,
    "reciclar"   : icon_recycle,
    "efluente"   : icon_drop,
    "embalar"    : icon_box,
    "distribuir" : icon_truck,
    "descartar"  : icon_trash,
    "armazenar"  : icon_factory,
    "bioplastico": icon_leaf,
    "papel_kraft": icon_paper,
    "bambu"      : icon_bamboo,
    "plastico_rec":icon_pellet,
    "mycelium"   : icon_mushroom,
    "pirolise"   : icon_flame,
    "compostagem": icon_compost,
    "logrev"     : icon_arrow_back,
    "eolica"     : icon_wind,
    "biogas"     : icon_battery,
    "cogeracao"  : icon_cogen,
    "verif_mat"  : icon_flask,
    "verif_cont" : icon_biohazard,
    # novos materiais coletaveis
    "col_pet"    : icon_bottle,
    "col_alumin" : icon_can,
    "col_vidro"  : icon_glass,
    "col_papel"  : icon_paper,
    "col_organic": icon_organic,
    "col_quim"   : icon_chemical,
    "col_metal"  : icon_metal,
    "col_borr"   : icon_rubber,
}

def draw_icon(surf, block_id, cx, cy, size, col):
    fn = ICON_FN.get(block_id)
    if fn:
        fn(surf, cx, cy, size, col)
    else:
        # fallback: quadrado colorido com inicial
        pygame.draw.rect(surf, col, (cx-size//2, cy-size//2, size, size), border_radius=4)
        draw_text(surf, block_id[0].upper(), F["small"], C["white"], (cx,cy), "center")

# ─── Definicao dos Blocos ─────────────────────────────────────────────────────
BLOCK_DEFS = [
    # ── Coleta de Materiais (novos tipos) ─────────────────────────────────────
    {"id":"coletar",     "label":"Coletar Materia",    "color":"blue",   "is_if":False,
     "co2":+6,  "custo":+40,  "oee":  0, "reuso":  0,
     "desc":"Coleta materia-prima bruta",              "categoria":"Coleta"},
    {"id":"col_pet",     "label":"Coletar PET",         "color":"blue",   "is_if":False,
     "co2":+3,  "custo":+20,  "oee":  0, "reuso": +5,
     "desc":"Garrafa PET pos-consumo",                "categoria":"Coleta"},
    {"id":"col_alumin",  "label":"Coletar Aluminio",    "color":"blue",   "is_if":False,
     "co2":+4,  "custo":+25,  "oee":  0, "reuso": +8,
     "desc":"Latas e chapas de aluminio",              "categoria":"Coleta"},
    {"id":"col_vidro",   "label":"Coletar Vidro",       "color":"teal",   "is_if":False,
     "co2":+3,  "custo":+18,  "oee":  0, "reuso": +6,
     "desc":"Cacos e embalagens de vidro",             "categoria":"Coleta"},
    {"id":"col_papel",   "label":"Coletar Papel/Papel", "color":"brown",  "is_if":False,
     "co2":+2,  "custo":+15,  "oee":  0, "reuso": +4,
     "desc":"Papelao e papel descartado",              "categoria":"Coleta"},
    {"id":"col_organic", "label":"Coletar Organicos",   "color":"green",  "is_if":False,
     "co2":+2,  "custo":+12,  "oee":  0, "reuso": +3,
     "desc":"Residuos alimentares e vegetais",         "categoria":"Coleta"},
    {"id":"col_quim",    "label":"Coletar Quimicos",    "color":"purple", "is_if":False,
     "co2":+8,  "custo":+55,  "oee":  0, "reuso":  0,
     "desc":"Solventes e residuos quimicos perigosos", "categoria":"Coleta"},
    {"id":"col_metal",   "label":"Coletar Metal/Sucata","color":"brown",  "is_if":False,
     "co2":+5,  "custo":+30,  "oee":  0, "reuso": +6,
     "desc":"Sucata ferrosa e metalica",               "categoria":"Coleta"},
    {"id":"col_borr",    "label":"Coletar Borracha",    "color":"red",    "is_if":False,
     "co2":+6,  "custo":+22,  "oee":  0, "reuso": +4,
     "desc":"Pneus e residuos de borracha",            "categoria":"Coleta"},
    # ── Verificacoes (IF) ─────────────────────────────────────────────────────
    {"id":"qualidade",   "label":"Verif. Qualidade",    "color":"orange", "is_if":True,
     "co2":  0, "custo":+15,  "oee": +8, "reuso":  0,
     "desc":"qualidade >= 80%?",                       "categoria":"Verificacao"},
    {"id":"desperd",     "label":"Verif. Desperdicio",  "color":"orange", "is_if":True,
     "co2":  0, "custo":+10,  "oee":+10, "reuso":  0,
     "desc":"desperdicio < 10%?",                      "categoria":"Verificacao"},
    {"id":"verif_mat",   "label":"Verif. Material",     "color":"orange", "is_if":True,
     "co2":  0, "custo":+12,  "oee": +6, "reuso":  0,
     "desc":"material e reciclavel?",                  "categoria":"Verificacao"},
    {"id":"verif_cont",  "label":"Verif. Contaminacao", "color":"orange", "is_if":True,
     "co2":  0, "custo":+18,  "oee": +5, "reuso":  0,
     "desc":"contaminacao < 5%?",                      "categoria":"Verificacao"},
    # ── Processos base ────────────────────────────────────────────────────────
    {"id":"processar",   "label":"Processar",           "color":"blue",   "is_if":False,
     "co2": +8, "custo":+60,  "oee": +6, "reuso":  0,
     "desc":"Transforma a materia-prima",              "categoria":"Processo"},
    {"id":"embalar",     "label":"Embalar",             "color":"blue",   "is_if":False,
     "co2": +4, "custo":+30,  "oee": +4, "reuso":  0,
     "desc":"Empacota o produto final",                "categoria":"Processo"},
    {"id":"distribuir",  "label":"Distribuir",          "color":"blue",   "is_if":False,
     "co2": +8, "custo":+50,  "oee": +6, "reuso":  0,
     "desc":"Entrega o produto ao cliente",            "categoria":"Processo"},
    {"id":"armazenar",   "label":"Armazenar",           "color":"blue",   "is_if":False,
     "co2": +2, "custo":+15,  "oee": +2, "reuso":  0,
     "desc":"Buffer intermediario de estoque",         "categoria":"Processo"},
    {"id":"descartar",   "label":"Descartar",           "color":"red",    "is_if":False,
     "co2":+20, "custo": +8,  "oee":-12, "reuso": -8,
     "desc":"Descarte em aterro sanitario",            "categoria":"Processo"},
    # ── Materiais alternativos ────────────────────────────────────────────────
    {"id":"bioplastico", "label":"Bioplastico",         "color":"green",  "is_if":False,
     "co2":-14, "custo":+25,  "oee": +3, "reuso":+10,
     "desc":"Plastico de origem vegetal (PLA)",        "categoria":"Mat. Alternativo"},
    {"id":"papel_kraft", "label":"Papel Kraft",         "color":"green",  "is_if":False,
     "co2":-10, "custo": -5,  "oee": +2, "reuso":+15,
     "desc":"Substitui embalagem plastica",            "categoria":"Mat. Alternativo"},
    {"id":"bambu",       "label":"Fibra de Bambu",      "color":"green",  "is_if":False,
     "co2":-16, "custo":+20,  "oee": +2, "reuso":+12,
     "desc":"Material renovavel de rapido crescimento","categoria":"Mat. Alternativo"},
    {"id":"plastico_rec","label":"Plast. Reciclado",    "color":"teal",   "is_if":False,
     "co2":-12, "custo":-10,  "oee": +4, "reuso":+20,
     "desc":"Usa pellets de plastico pos-consumo",     "categoria":"Mat. Alternativo"},
    {"id":"mycelium",    "label":"Mycelium Pack",       "color":"green",  "is_if":False,
     "co2":-18, "custo":+30,  "oee": +1, "reuso": +8,
     "desc":"Embalagem biodegradavel de fungo",        "categoria":"Mat. Alternativo"},
    # ── Tratamento ────────────────────────────────────────────────────────────
    {"id":"reciclar",    "label":"Reciclar",            "color":"green",  "is_if":False,
     "co2":-15, "custo":-15,  "oee": +3, "reuso":+22,
     "desc":"Recicla residuos gerados",                "categoria":"Tratamento"},
    {"id":"reuso",       "label":"Redir. Reuso",        "color":"green",  "is_if":False,
     "co2":-12, "custo":-25,  "oee": +5, "reuso":+18,
     "desc":"Reutiliza subprodutos no processo",       "categoria":"Tratamento"},
    {"id":"efluente",    "label":"Tratar Efluente",     "color":"teal",   "is_if":False,
     "co2": -6, "custo":+20,  "oee": +3, "reuso": +8,
     "desc":"Trata e reutiliza agua residual",         "categoria":"Tratamento"},
    {"id":"pirolise",    "label":"Pirolise",            "color":"teal",   "is_if":False,
     "co2": -8, "custo":+35,  "oee": +4, "reuso":+16,
     "desc":"Converte plastico em combustivel",        "categoria":"Tratamento"},
    {"id":"compostagem", "label":"Compostagem",         "color":"green",  "is_if":False,
     "co2":-10, "custo": +5,  "oee": +2, "reuso":+14,
     "desc":"Biodegradacao de materiais organicos",    "categoria":"Tratamento"},
    {"id":"logrev",      "label":"Logist. Reversa",     "color":"teal",   "is_if":False,
     "co2": -5, "custo":+22,  "oee": +3, "reuso":+12,
     "desc":"Retorna embalagens para reprocesso",      "categoria":"Tratamento"},
    # ── Energia limpa ─────────────────────────────────────────────────────────
    {"id":"solar",       "label":"Energia Solar",       "color":"yellow", "is_if":False,
     "co2":-18, "custo":-35,  "oee": +4, "reuso":  0,
     "desc":"Substitui energia da rede eletrica",      "categoria":"Energia"},
    {"id":"eolica",      "label":"Energia Eolica",      "color":"yellow", "is_if":False,
     "co2":-16, "custo":-28,  "oee": +3, "reuso":  0,
     "desc":"Geracao por turbinas eolicas",            "categoria":"Energia"},
    {"id":"biogas",      "label":"Biogas",              "color":"yellow", "is_if":False,
     "co2":-12, "custo":-20,  "oee": +3, "reuso": +5,
     "desc":"Energia do gas de residuos organicos",    "categoria":"Energia"},
    {"id":"cogeracao",   "label":"Cogeracao",           "color":"yellow", "is_if":False,
     "co2":-10, "custo":-18,  "oee": +5, "reuso":  0,
     "desc":"Reaproveitamento de calor industrial",    "categoria":"Energia"},
]
BLOCK_BY_ID = {b["id"]: b for b in BLOCK_DEFS}

# ─── No ───────────────────────────────────────────────────────────────────────
_uid_counter = 0

class Node:
    W_STD, H_STD = 178, 58
    W_IF,  H_IF  = 196, 76

    def __init__(self, x, y, bdef):
        global _uid_counter
        _uid_counter += 1
        self.uid       = _uid_counter
        self.x, self.y = float(x), float(y)
        self.bdef      = bdef
        self.is_if     = bdef["is_if"]
        self.w         = self.W_IF  if self.is_if else self.W_STD
        self.h         = self.H_IF  if self.is_if else self.H_STD
        self._dragging = False
        self._doff     = (0.0, 0.0)
        self.pulse     = 0.0
        self.lit       = False

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def p_in(self):
        return (int(self.x),          int(self.y + self.h // 2))
    def p_out(self):
        return (int(self.x + self.w), int(self.y + self.h // 2))
    def p_yes(self):
        return (int(self.x + self.w // 2), int(self.y + self.h))
    def p_no(self):
        return (int(self.x + self.w),      int(self.y + self.h // 2))

    def near_port(self, pos, port_pos, tol=PORT_R + 5):
        return dist(pos, port_pos) < tol

    def handle_drag(self, event, ox, oy):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            ax, ay = event.pos[0] - ox, event.pos[1] - oy
            if self.rect.collidepoint(ax, ay):
                self._dragging = True
                self._doff = (ax - self.x, ay - self.y)
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self._dragging = False
        elif event.type == pygame.MOUSEMOTION and self._dragging:
            ax, ay = event.pos[0] - ox, event.pos[1] - oy
            self.x = ax - self._doff[0]
            self.y = ay - self._doff[1]
        return False

    def draw(self, surf, mx, my):
        col  = C[self.bdef["color"]]
        dark = C[self.bdef["color"] + "_d"]
        hov  = self.rect.collidepoint(mx, my)
        shade = tuple(min(255, v + 20) for v in col) if hov else col

        if self.lit:
            a = int(150 * abs(math.sin(self.pulse)))
            gs = pygame.Surface((self.w + 20, self.h + 20), pygame.SRCALPHA)
            pygame.draw.rect(gs, (*col, a), (0, 0, self.w+20, self.h+20), border_radius=16)
            surf.blit(gs, (int(self.x) - 10, int(self.y) - 10))

        rrect(surf, C["shadow"], (int(self.x)+4, int(self.y)+4, self.w, self.h), 12)
        rrect(surf, shade, self.rect, 12, dark, 2)

        if self.is_if:
            self._draw_if_body(surf, dark)
        else:
            self._draw_std_body(surf, dark)

        pi = self.p_in()
        near_i = self.near_port((mx, my), pi)
        circ(surf, C["port_hl"] if near_i else C["port_in"], pi, PORT_R, C["green_d"], 2)

        if self.is_if:
            py_ = self.p_yes(); pn_ = self.p_no()
            near_y = self.near_port((mx, my), py_)
            near_n = self.near_port((mx, my), pn_)
            circ(surf, C["port_hl"] if near_y else C["port_yes"], py_, PORT_R, C["green_d"], 2)
            circ(surf, C["port_hl"] if near_n else C["port_no"],  pn_, PORT_R, C["red_d"],   2)
            draw_text(surf, "Y", F["tiny"], C["white"], py_, "center")
            draw_text(surf, "N", F["tiny"], C["white"], pn_, "center")
        else:
            po = self.p_out()
            near_o = self.near_port((mx, my), po)
            circ(surf, C["port_hl"] if near_o else C["port_out"], po, PORT_R, C["orange_d"], 2)

    def _draw_std_body(self, surf, dark):
        cx = int(self.x) + 26
        cy = int(self.y) + self.h // 2
        pygame.draw.circle(surf, dark, (cx, cy), 18)
        draw_icon(surf, self.bdef["id"], cx, cy, 11, C["white"])
        draw_text(surf, self.bdef["label"], F["body"], C["white"],
                  (int(self.x) + 50, cy), "midleft")

    def _draw_if_body(self, surf, dark):
        cx, cy = int(self.x) + 22, int(self.y) + 22
        r = 15
        pts = [(cx + r*math.cos(math.radians(a-90)),
                cy + r*math.sin(math.radians(a-90))) for a in range(0, 360, 60)]
        pygame.draw.polygon(surf, dark, pts)
        draw_text(surf, "IF", F["tiny"], C["white"], (cx, cy), "center")
        draw_text(surf, self.bdef["label"], F["small"], C["white"],
                  (int(self.x) + 44, int(self.y) + 8))
        draw_text(surf, "IF " + self.bdef["desc"], F["tiny"], C["lgray"],
                  (int(self.x) + 44, int(self.y) + 26))
        yr = pygame.Rect(int(self.x) + 12, int(self.y) + 54, 78, 16)
        nr = pygame.Rect(int(self.x) + 98, int(self.y) + 54, 78, 16)
        rrect(surf, C["yes"], yr, 5)
        rrect(surf, C["no"],  nr, 5)
        draw_text(surf, "YES ->", F["tiny"], C["white"], yr.center, "center")
        draw_text(surf, "NO  ->", F["tiny"], C["white"], nr.center, "center")

# ─── Conexao ──────────────────────────────────────────────────────────────────
class Connection:
    def __init__(self, src, dst, from_yes=True):
        self.src      = src
        self.dst      = dst
        self.from_yes = from_yes
        self.anim_t   = 0.0
        self.active   = False

    def _start(self):
        if self.src.is_if:
            return self.src.p_yes() if self.from_yes else self.src.p_no()
        return self.src.p_out()

    def _end(self):
        return self.dst.p_in()

    def _pts(self):
        s, e = self._start(), self._end()
        mx   = (s[0] + e[0]) / 2
        return bezier(s, (mx, s[1]), (mx, e[1]), e)

    def draw(self, surf):
        pts = self._pts()
        if len(pts) < 2:
            return
        pygame.draw.lines(surf, C["conn"], False, pts, 3)
        draw_arrowhead(surf, pts[-1], pts[-2], C["conn"])

        if self.active and 0 < self.anim_t < 1:
            t    = self.anim_t
            s    = self._start(); e = self._end()
            mx_b = (s[0] + e[0]) / 2
            x = (1-t)**3*s[0]+3*(1-t)**2*t*mx_b+3*(1-t)*t**2*mx_b+t**3*e[0]
            y = (1-t)**3*s[1]+3*(1-t)**2*t*s[1] +3*(1-t)*t**2*e[1] +t**3*e[1]
            pygame.draw.circle(surf, C["anim_dot"], (int(x), int(y)), 8)
            pygame.draw.circle(surf, C["white"],    (int(x), int(y)), 4)

    def hit(self, px, py, tol=9):
        return any(dist(p, (px, py)) < tol for p in self._pts())

# ─── Simulacao (BFS) ──────────────────────────────────────────────────────────
def simulate(nodes, conns, base_metrics):
    dst_set = {c.dst.uid for c in conns}
    sources = [n for n in nodes if n.uid not in dst_set]
    visited = set(); queue = list(sources); order = []
    while queue:
        node = queue.pop(0)
        if node.uid in visited: continue
        visited.add(node.uid); order.append(node)
        for c in conns:
            if c.src.uid == node.uid and c.dst.uid not in visited:
                queue.append(c.dst)
    d_co2 = d_custo = d_oee = d_reuso = 0
    for n in order:
        d_co2   += n.bdef["co2"];  d_custo += n.bdef["custo"]
        d_oee   += n.bdef["oee"];  d_reuso += n.bdef["reuso"]
    def clamp(v, lo, hi): return max(lo, min(hi, v))
    return {
        "co2"  : clamp(base_metrics["co2"]  + d_co2,   0, 999),
        "custo": clamp(base_metrics["custo"] + d_custo, 0, 9999),
        "oee"  : clamp(base_metrics["oee"]  + d_oee,   0, 100),
        "reuso": clamp(base_metrics["reuso"] + d_reuso, 0, 100),
    }, order

# ─── Fluxo padrao ─────────────────────────────────────────────────────────────
def build_default():
    n_pet  = Node( 44,  30, BLOCK_BY_ID["col_pet"])
    n_alu  = Node( 44, 160, BLOCK_BY_ID["col_alumin"])
    n_sol  = Node( 44, 290, BLOCK_BY_ID["solar"])
    n_vmat = Node(268,  30, BLOCK_BY_ID["verif_mat"])
    n_prc  = Node(268, 180, BLOCK_BY_ID["processar"])
    n_prec = Node(492,  10, BLOCK_BY_ID["plastico_rec"])
    n_bio  = Node(492, 120, BLOCK_BY_ID["bioplastico"])
    n_qlt  = Node(492, 260, BLOCK_BY_ID["qualidade"])
    n_emb  = Node(720,  10, BLOCK_BY_ID["embalar"])
    n_dst  = Node(940,  10, BLOCK_BY_ID["distribuir"])
    n_rec  = Node(720, 190, BLOCK_BY_ID["reciclar"])
    n_pir  = Node(720, 320, BLOCK_BY_ID["pirolise"])

    nodes = [n_pet,n_alu,n_sol,n_vmat,n_prc,n_prec,n_bio,n_qlt,n_emb,n_dst,n_rec,n_pir]
    conns = [
        Connection(n_pet,  n_vmat),
        Connection(n_alu,  n_prc),
        Connection(n_sol,  n_prc),
        Connection(n_vmat, n_prec, from_yes=True),
        Connection(n_vmat, n_bio,  from_yes=False),
        Connection(n_prec, n_qlt),
        Connection(n_bio,  n_qlt),
        Connection(n_prc,  n_qlt),
        Connection(n_qlt,  n_emb, from_yes=True),
        Connection(n_qlt,  n_rec, from_yes=False),
        Connection(n_emb,  n_dst),
        Connection(n_rec,  n_pir),
    ]
    return nodes, conns

# ─── Sidebar: estado de scroll ────────────────────────────────────────────────
_sidebar_scroll = 0

def sidebar_scroll_delta(dy):
    global _sidebar_scroll
    _sidebar_scroll = max(0, _sidebar_scroll - dy * 28)

_ITEM_H = 46
_CAT_H  = 22

def _sidebar_layout():
    items = []; y = 0; last_cat = None
    for bd in BLOCK_DEFS:
        cat = bd.get("categoria", "")
        if cat != last_cat:
            items.append(("cat", y, cat)); y += _CAT_H + 2; last_cat = cat
        items.append(("block", y, bd));    y += _ITEM_H + 4
    return items, y

# ─── Desenho: Sidebar ─────────────────────────────────────────────────────────
def draw_sidebar(surf, mouse):
    global _sidebar_scroll
    mx, my = mouse

    pygame.draw.rect(surf, C["side"], (0, 0, SIDEBAR_W, H))
    pygame.draw.line(surf, C["sline"], (SIDEBAR_W-1, 0), (SIDEBAR_W-1, H), 2)

    # Titulo
    draw_text(surf, "EcoFlow", F["h2"], C["white"], (14, 10))
    draw_text(surf, "Blocos disponíveis", F["tiny"], C["lgray"], (14, 32))
    pygame.draw.line(surf, C["sline"], (0, HEADER_H-4), (SIDEBAR_W, HEADER_H-4), 1)

    # Zona da lista
    list_top    = HEADER_H
    list_bottom = H - BTN_AREA_H
    list_h      = list_bottom - list_top

    items, total_h = _sidebar_layout()
    _sidebar_scroll = max(0, min(_sidebar_scroll, max(0, total_h - list_h)))

    # Surface clipada para a lista de blocos
    clip = pygame.Surface((SIDEBAR_W, list_h), pygame.SRCALPHA)
    clip.fill((18, 38, 64, 255))

    rects_local = []
    for kind, y_rel, data in items:
        y_draw = y_rel - _sidebar_scroll
        item_h = _ITEM_H if kind == "block" else _CAT_H
        if y_draw + item_h < 0 or y_draw > list_h:
            continue

        if kind == "cat":
            pygame.draw.rect(clip, C["cat_bg"], (0, y_draw, SIDEBAR_W, _CAT_H))
            draw_text(clip, data.upper(), F["tiny"], C["lgray"], (10, y_draw + 5))

        elif kind == "block":
            bd  = data
            col = C[bd["color"]]
            drk = C[bd["color"] + "_d"]
            br  = pygame.Rect(6, y_draw, SIDEBAR_W - 12, _ITEM_H)
            mx_c = mx; my_c = my - list_top
            hov  = br.collidepoint(mx_c, my_c) and 0 <= my_c <= list_h
            shade = tuple(min(255, v + 22) for v in col) if hov else col

            rrect(clip, C["shadow"], (br.x+2, br.y+2, br.w, br.h), 7)
            rrect(clip, shade, br, 7, drk, 2)

            # icone desenhado (sem emoji)
            icon_cx = br.x + 20; icon_cy = br.centery
            pygame.draw.circle(clip, drk, (icon_cx, icon_cy), 15)
            draw_icon(clip, bd["id"], icon_cx, icon_cy, 9, C["white"])

            draw_text(clip, bd["label"], F["small"], C["white"],
                      (br.x + 40, br.centery - 9))
            co2_col = C["green"] if bd["co2"] <= 0 else C["red"]
            oee_col = C["green"] if bd["oee"] >= 0 else C["red"]
            draw_text(clip, f"CO2:{bd['co2']:+}", F["tiny"], co2_col,
                      (br.x + 40, br.centery + 4))
            draw_text(clip, f"OEE:{bd['oee']:+}%", F["tiny"], oee_col,
                      (br.x + 40 + 84, br.centery + 4))

            screen_rect = pygame.Rect(br.x, br.y + list_top, br.w, br.h)
            rects_local.append((screen_rect, bd))

    surf.blit(clip, (0, list_top))

    # Scrollbar
    if total_h > list_h:
        sb_w = 4; sb_x = SIDEBAR_W - sb_w - 2
        ratio = list_h / total_h
        sb_h  = max(24, int(list_h * ratio))
        sb_y  = list_top + int((_sidebar_scroll / max(1, total_h)) * list_h)
        pygame.draw.rect(surf, C["lgray"], (sb_x, sb_y, sb_w, sb_h), border_radius=2)

    # ── Zona de botoes (fixada no fundo da sidebar) ────────────────────────────
    btn_y0 = H - BTN_AREA_H
    pygame.draw.rect(surf, C["side"], (0, btn_y0, SIDEBAR_W, BTN_AREA_H))
    pygame.draw.line(surf, C["sline"], (0, btn_y0), (SIDEBAR_W, btn_y0), 1)

    return rects_local

# ─── Desenho: Botoes de acao (agora retornam so os rects, desenho esta na sidebar) ──
def draw_action_buttons(surf, run_active, mouse):
    mx, my = mouse
    btn_y0 = H - BTN_AREA_H
    pad = 8; bw = SIDEBAR_W - pad*2

    # Botao Reset (acima)
    rstb = pygame.Rect(pad, btn_y0 + 8, bw, 40)
    hov_s = rstb.collidepoint(mx, my)
    rrect(surf, C["shadow"], (rstb.x+2, rstb.y+2, rstb.w, rstb.h), 9)
    rrect(surf, C["rst_h"] if hov_s else C["rst"], rstb, 9, (20, 40, 70), 2)
    draw_text(surf, "Reset KPIs", F["body"], C["white"], rstb.center, "center")

    # Botao Run (abaixo)
    rb = pygame.Rect(pad, btn_y0 + 56, bw, 54)
    hov_r = rb.collidepoint(mx, my)
    rc = C["run_a"] if run_active else (C["run_h"] if hov_r else C["run"])
    rrect(surf, C["shadow"], (rb.x+2, rb.y+2, rb.w, rb.h), 10)
    rrect(surf, rc, rb, 10, C["green_d"], 2)

    if run_active:
        spin = (pygame.time.get_ticks() // 7) % 360
        for a in range(0, 360, 45):
            ax = rb.centerx + 14*math.cos(math.radians(a + spin)) - 36
            ay = rb.centery +  6*math.sin(math.radians(a + spin))
            pygame.draw.circle(surf, C["white"], (int(ax), int(ay)), 3)
        draw_text(surf, "  Simulando...", F["h2"], C["white"], rb.center, "center")
    else:
        draw_text(surf, "> Run Flow", F["h2"], C["white"], rb.center, "center")

    return rb, rstb

# ─── Desenho: KPIs ────────────────────────────────────────────────────────────
def draw_metrics(surf, mt):
    mr = pygame.Rect(SIDEBAR_W, H - METRICS_H, W - SIDEBAR_W, METRICS_H)
    pygame.draw.rect(surf, C["mbg"], mr)
    pygame.draw.line(surf, C["cborder"], (mr.x, mr.y), (mr.right, mr.y), 2)
    draw_text(surf, "KPIs - Indicadores de Desempenho",
              F["h2"], C["tdark"], (mr.x + 18, mr.y + 10))

    kpis = [
        ("OEE",    f"{mt['oee']:.0f}%",     mt['oee'],
         "kpi_oee", "Eficiencia Global"),
        ("CO2",    f"{mt['co2']:.0f} kg",
         max(0, 100 - mt['co2'] * 0.20),
         "kpi_co2", "Emissao de carbono"),
        ("Reuso",  f"{mt['reuso']:.0f}%",   mt['reuso'],
         "kpi_reus","Reaproveitamento"),
        ("Custo",  f"R${mt['custo']:.0f}",
         max(0, 100 - mt['custo'] * 0.025),
         "kpi_cust","Custo de producao"),
    ]

    cw = (mr.width - 44) // 4
    for i, (name, val_s, fill_pct, ckey, desc) in enumerate(kpis):
        cx_ = mr.x + 14 + i * (cw + 5)
        cy_ = mr.y + 34
        card = pygame.Rect(cx_, cy_, cw, 76)
        rrect(surf, C["mcard"], card, 8, C["cborder"], 1)
        draw_text(surf, name,  F["body"], C[ckey], (cx_+10, cy_+7))
        draw_text(surf, val_s, F["h2"],  C[ckey], (card.right-10, cy_+5), "topright")
        draw_text(surf, desc,  F["tiny"],C["tdark"],(cx_+10, cy_+30))
        track = pygame.Rect(cx_+10, cy_+52, cw-20, 14)
        rrect(surf, C["mtrack"], track, 7)
        fw = max(6, int((cw-20) * max(0, min(100, fill_pct)) / 100))
        rrect(surf, C[ckey], (cx_+10, cy_+52, fw, 14), 7)

# ─── Desenho: Canvas ──────────────────────────────────────────────────────────
def draw_canvas(nodes, conns, mx_c, my_c,
                connecting, conn_src, conn_from_yes, conn_drag):
    cw = W - SIDEBAR_W
    ch = H - HEADER_H - METRICS_H
    surf = pygame.Surface((cw, ch))
    surf.fill(C["canvas"])

    for gx in range(0, cw, 24):
        for gy in range(0, ch, 24):
            pygame.draw.circle(surf, C["dot"], (gx, gy), 1)

    for c in conns:
        c.draw(surf)

    if connecting and conn_src:
        start = (conn_src.p_yes() if conn_from_yes else conn_src.p_no()) \
                if conn_src.is_if else conn_src.p_out()
        mx_p = (start[0] + conn_drag[0]) // 2
        pts  = bezier(start, (mx_p, start[1]), (mx_p, conn_drag[1]), conn_drag)
        if len(pts) >= 2:
            pygame.draw.lines(surf, C["conn_pre"], False, pts, 2)
        pygame.draw.circle(surf, C["anim_dot"], conn_drag, 7)
        pygame.draw.circle(surf, C["white"],    conn_drag, 4)

    for node in nodes:
        node.draw(surf, mx_c, my_c)

    # Legenda
    lx, ly = cw - 190, ch - 52
    draw_text(surf, "Portas:", F["tiny"], C["tdark"], (lx, ly))
    circ(surf, C["port_in"],  (lx+60, ly+5),  7, C["green_d"],  1)
    draw_text(surf, "Entrada", F["tiny"], C["tdark"],  (lx+72, ly+1))
    circ(surf, C["port_out"], (lx+60, ly+20), 7, C["orange_d"], 1)
    draw_text(surf, "Saida",   F["tiny"], C["tdark"],  (lx+72, ly+16))
    circ(surf, C["port_yes"], (lx+128,ly+5),  7, C["green_d"],  1)
    draw_text(surf, "YES",     F["tiny"], C["yes"],    (lx+140,ly+1))
    circ(surf, C["port_no"],  (lx+128,ly+20), 7, C["red_d"],    1)
    draw_text(surf, "NO",      F["tiny"], C["no"],     (lx+140,ly+16))
    return surf

# ─── Main ─────────────────────────────────────────────────────────────────────
METRICS_BASE = {"co2": 80, "custo": 500, "oee": 55, "reuso": 10}

def main():
    clock = pygame.time.Clock()
    nodes, conns = build_default()
    metrics      = dict(METRICS_BASE)

    run_active    = False
    anim_t        = 0.0
    connecting    = False
    conn_src      = None
    conn_from_yes = True
    conn_drag     = (0, 0)
    fb_msg = ""; fb_col = C["fb_ok"]; fb_t = 0.0

    run_btn_r = pygame.Rect(0,0,0,0)
    rst_btn_r = pygame.Rect(0,0,0,0)
    sidebar_r = []

    canvas_rect = pygame.Rect(OX, OY, W - SIDEBAR_W, H - HEADER_H - METRICS_H)

    def set_feedback(msg, col=None):
        nonlocal fb_msg, fb_col, fb_t
        fb_msg = msg; fb_col = col or C["fb_ok"]; fb_t = 4000.0

    while True:
        dt = clock.tick(FPS)
        mx, my     = pygame.mouse.get_pos()
        mx_c, my_c = mx - OX, my - OY

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                connecting = False; conn_src = None

            if event.type == pygame.MOUSEWHEEL and mx < SIDEBAR_W:
                sidebar_scroll_delta(event.y)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if canvas_rect.collidepoint(mx, my):
                    deleted = False
                    for n in nodes[:]:
                        if n.rect.collidepoint(mx_c, my_c):
                            conns = [c for c in conns
                                     if c.src.uid != n.uid and c.dst.uid != n.uid]
                            nodes.remove(n); deleted = True
                            set_feedback("No removido."); break
                    if not deleted:
                        for c in conns[:]:
                            if c.hit(mx_c, my_c):
                                conns.remove(c)
                                set_feedback("Conexao removida."); break

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if canvas_rect.collidepoint(mx, my):
                    consumed = False
                    for node in reversed(nodes):
                        p_in = node.p_in()
                        if connecting and conn_src and node.uid != conn_src.uid:
                            if dist((mx_c, my_c), p_in) < PORT_R + 6:
                                dup = any(c.src.uid == conn_src.uid and
                                          c.dst.uid == node.uid and
                                          c.from_yes == conn_from_yes for c in conns)
                                if not dup:
                                    conns.append(Connection(conn_src, node, conn_from_yes))
                                    set_feedback("Conexao criada!")
                                connecting = False; conn_src = None
                                consumed = True; break
                        if not connecting:
                            if node.is_if and dist((mx_c,my_c),node.p_yes()) < PORT_R+6:
                                connecting=True; conn_src=node; conn_from_yes=True
                                consumed=True; break
                            if node.is_if and dist((mx_c,my_c),node.p_no()) < PORT_R+6:
                                connecting=True; conn_src=node; conn_from_yes=False
                                consumed=True; break
                            if not node.is_if and dist((mx_c,my_c),node.p_out()) < PORT_R+6:
                                connecting=True; conn_src=node; conn_from_yes=True
                                consumed=True; break
                    if not consumed and connecting:
                        connecting=False; conn_src=None
                    if not consumed:
                        for node in reversed(nodes):
                            if node.handle_drag(event, OX, OY):
                                nodes.remove(node); nodes.append(node); break
                else:
                    # Clique na sidebar: adicionar bloco
                    for br, bd in sidebar_r:
                        if br.collidepoint(mx, my):
                            nx = random.randint(30, canvas_rect.width  - 210)
                            ny = random.randint(30, canvas_rect.height - 130)
                            nodes.append(Node(nx, ny, bd))
                            set_feedback(f"'{bd['label']}' adicionado.", C["fb_info"])
                            break
                    # Botao Run
                    if run_btn_r.collidepoint(mx, my) and not run_active:
                        if not conns:
                            set_feedback("Conecte os nos antes de executar!", C["red"])
                        else:
                            run_active = True; anim_t = 0.0
                            for c in conns: c.active=True; c.anim_t=0.0
                            for n in nodes: n.lit=True;   n.pulse=0.0
                    # Botao Reset
                    if rst_btn_r.collidepoint(mx, my) and not run_active:
                        metrics = dict(METRICS_BASE)
                        for n in nodes: n.lit = False
                        set_feedback("KPIs restaurados.", C["fb_info"])

            if event.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                for node in nodes:
                    node.handle_drag(event, OX, OY)

        conn_drag = (mx_c, my_c)

        # Animacao Run
        if run_active:
            anim_t += dt
            speed = 0.0013
            for i, c in enumerate(conns):
                c.anim_t = max(0.0, min(1.0, anim_t * speed - i * 0.15))
            for n in nodes:
                n.pulse += dt * 0.005
            if all(c.anim_t >= 1.0 for c in conns):
                new_mt, order = simulate(nodes, conns, metrics)
                metrics = new_mt; run_active = False
                for c in conns: c.active = False
                for n in nodes: n.lit    = False
                set_feedback("Simulacao concluida! KPIs atualizados.")

        if fb_t > 0:
            fb_t -= dt

        # ── Render ────────────────────────────────────────────────────────────
        screen.fill(C["hdr"])

        # Header
        pygame.draw.rect(screen, C["hdr"], (0, 0, W, HEADER_H))
        pygame.draw.line(screen, C["hline"], (SIDEBAR_W, HEADER_H-1), (W, HEADER_H-1), 2)
        draw_text(screen, "EcoFlow Industrial", F["title"], C["white"], (SIDEBAR_W+18, 14))
        draw_text(screen, "Simulador de Linha de Producao Sustentavel - Plastico & Embalagens",
                  F["small"], C["lgray"], (SIDEBAR_W+18, 38), "topleft")
        hint = "ESC cancela conexao  |  Btn direito deleta  |  Arraste para mover  |  Scroll na sidebar"
        draw_text(screen, hint, F["tiny"], C["lgray"], (W - 14, HEADER_H//2), "midright")

        # Sidebar (inclui area dos botoes desenhada internamente)
        sidebar_r = draw_sidebar(screen, (mx, my))

        # Botoes (desenhados sobre a sidebar na zona reservada)
        run_btn_r, rst_btn_r = draw_action_buttons(screen, run_active, (mx, my))

        # Canvas
        c_surf = draw_canvas(nodes, conns, mx_c, my_c,
                              connecting, conn_src, conn_from_yes, conn_drag)
        screen.blit(c_surf, (OX, OY))
        pygame.draw.rect(screen, C["cborder"], canvas_rect, 2)

        # KPIs
        draw_metrics(screen, metrics)

        # Feedback
        if fb_t > 0 and fb_msg:
            alpha = min(255, int(255 * min(fb_t, 600) / 600))
            fbs = pygame.Surface((440, 38), pygame.SRCALPHA)
            pygame.draw.rect(fbs, (*fb_col, alpha), (0,0,440,38), border_radius=9)
            fbs.blit(F["body"].render(fb_msg, True, C["white"]), (12, 9))
            screen.blit(fbs, (OX + 16, OY + 12))

        if connecting:
            draw_text(screen, "Clique na porta ENTRADA do no destino | ESC cancela",
                      F["small"], C["anim_dot"], (OX+16, OY+canvas_rect.height-26))

        pygame.display.flip()

if __name__ == "__main__":
    main()