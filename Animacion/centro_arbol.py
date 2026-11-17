from collections import deque

import numpy as np
from manim import *


def lista_adyacencia(n, aristas):
    adj = [[] for _ in range(n)]
    for u, v in aristas:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def centro_arbol(n, aristas):
    if n == 1:
        return [0], []
    adj = lista_adyacencia(n, aristas)
    grado = [len(a) for a in adj]
    hojas = [v for v in range(n) if grado[v] == 1]
    restantes = n
    traza = []
    while restantes > 2:
        antes = restantes
        restantes -= len(hojas)
        nuevas = []
        for u in hojas:
            grado[u] = 0
            for v in adj[u]:
                if grado[v] > 0:
                    grado[v] -= 1
                    if grado[v] == 1:
                        nuevas.append(v)
        traza.append(dict(hojas=hojas, antes=antes, despues=restantes,
                          grados=grado[:]))
        hojas = nuevas
    return hojas, traza


def excentricidades(n, aristas):
    adj = lista_adyacencia(n, aristas)
    ecc = []
    for s in range(n):
        dist = [-1] * n
        dist[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if dist[v] < 0:
                    dist[v] = dist[u] + 1
                    q.append(v)
        ecc.append(max(dist))
    return ecc


ARB_N = 11
ARB_E = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
         (3, 7), (7, 8), (4, 9), (2, 10)]
ARB_POS = {0: (-5.4, 0), 1: (-3.6, 0), 2: (-1.8, 0), 3: (0, 0),
           4: (1.8, 0), 5: (3.6, 0), 6: (5.4, 0),
           7: (0, -1.4), 8: (0, -2.7), 9: (1.8, 1.4), 10: (-1.8, 1.4)}

CAM_N = 6
CAM_E = [(i, i + 1) for i in range(CAM_N - 1)]
CAM_POS = {i: (-3.75 + 1.5 * i, 0) for i in range(CAM_N)}

R_NODO = 0.28
C_NODO = BLUE_E
C_HOJA = ORANGE
C_CENTRO = GREEN


class CentroDeUnArbol(Scene):
    def construct(self):
        self.camera.background_color = "#0d1117"
        self.portada()
        self.introduccion()
        self.demo_principal()
        self.casos_borde()
        self.complejidad()
        self.creditos()

    def limpiar(self, t=0.6):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=t)

    def encabezado(self, texto):
        t = Text(texto, font_size=36, weight=BOLD).to_edge(UP, buff=0.35)
        return t

    def crear_arbol(self, n, aristas, pos, desplazar=0.3):
        P = {v: np.array([pos[v][0], pos[v][1] + desplazar, 0.0]) for v in pos}
        ar = {}
        for u, v in aristas:
            ar[(u, v)] = Line(P[u], P[v], buff=R_NODO, stroke_width=4,
                              color=GREY_B)
        nodos = {}
        for v in range(n):
            c = Circle(radius=R_NODO, color=WHITE, stroke_width=3,
                       fill_color=C_NODO, fill_opacity=1)
            lbl = Text(str(v), font_size=22)
            nodos[v] = VGroup(c, lbl).move_to(P[v])
        return nodos, ar

    def etiqueta_junto(self, nodo, txt, color=YELLOW):
        return Text(str(txt), font_size=20, color=color).move_to(
            nodo.get_center() + np.array([0.42, 0.42, 0]))

    def portada(self):
        t1 = Text("Centro de un árbol", font_size=64, weight=BOLD)
        t2 = Text("Pelado de hojas en O(n)", font_size=34, color=BLUE_B)
        curso = Text("CS2023 · Algoritmos y Estructuras de Datos · 2026-2",
                     font_size=24, color=GREY_B)
        g = VGroup(t1, t2, curso).arrange(DOWN, buff=0.45)
        self.play(FadeIn(t1, shift=UP * 0.3), run_time=1)
        self.play(FadeIn(t2), FadeIn(curso), run_time=0.8)
        self.wait(1.5)
        self.limpiar()

    def introduccion(self):
        h = self.encabezado("¿Qué es el centro de un árbol?")
        l1 = Text("Árbol: grafo conexo, acíclico y no dirigido.", font_size=28)
        l2 = Text("d(u, v) = número de aristas del único camino entre u y v.",
                  font_size=28)
        f1 = Text("exc(v) = max d(v, u)   sobre todos los nodos u", font_size=40)
        f2 = Text("centro = nodo v con exc(v) mínima", font_size=40, color=GREEN)
        l3 = Text("Todo árbol tiene 1 o 2 centros (si son 2, son adyacentes).",
                  font_size=26, color=YELLOW)
        g = VGroup(l1, l2, f1, f2, l3).arrange(DOWN, buff=0.45)
        g.next_to(h, DOWN, buff=0.5)
        self.play(FadeIn(h))
        for m in (l1, l2):
            self.play(FadeIn(m, shift=UP * 0.2), run_time=0.8)
            self.wait(0.6)
        self.play(FadeIn(f1), run_time=1.2)
        self.wait(0.6)
        self.play(FadeIn(f2), run_time=1.2)
        self.wait(0.8)
        self.play(FadeIn(l3))
        self.wait(2)
        self.limpiar()

        h = self.encabezado("¿Para qué sirve?")
        usos = VGroup(
            Text("• Mejor raíz: el árbol enraizado en el centro tiene altura mínima.",
                 font_size=27),
            Text("• Ubicar un servidor o hub minimizando el peor retardo.",
                 font_size=27),
            Text("• Diámetro = 2·radio (1 centro)  ó  2·radio − 1 (2 centros).",
                 font_size=27),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(h, DOWN, buff=0.8)
        self.play(FadeIn(h))
        for u in usos:
            self.play(FadeIn(u, shift=RIGHT * 0.3), run_time=0.8)
            self.wait(0.8)
        self.wait(1)
        self.limpiar()

        h = self.encabezado("Idea del algoritmo")
        a = Text("El centro está en el medio de cualquier camino más largo.",
                 font_size=28)
        b = Text("Entonces: quitar TODAS las hojas, capa por capa,",
                 font_size=28, color=ORANGE)
        c = Text("hasta que queden 1 o 2 nodos. Esos son los centros.",
                 font_size=28, color=GREEN)
        g = VGroup(a, b, c).arrange(DOWN, buff=0.4).next_to(h, DOWN, buff=1.0)
        self.play(FadeIn(h))
        self.play(FadeIn(a), run_time=0.8)
        self.wait(0.8)
        self.play(FadeIn(b), run_time=0.8)
        self.play(FadeIn(c), run_time=0.8)
        self.wait(2)
        self.limpiar()

    def pelar(self, titulo, n, aristas, pos, rt=1.0):
        centros, traza = centro_arbol(n, aristas)
        h = self.encabezado(titulo)
        regla = Text("Mientras queden más de 2 nodos: quitar todas las hojas.",
                     font_size=26, color=GREY_A).next_to(h, DOWN, buff=0.25)
        nodos, ar = self.crear_arbol(n, aristas, pos)
        grados = [len(a) for a in lista_adyacencia(n, aristas)]
        etq = {v: self.etiqueta_junto(nodos[v], grados[v]) for v in range(n)}
        info = Text(f"n = {n}   ·   grado en amarillo   ·   hojas = grado 1",
                    font_size=26).to_edge(DOWN, buff=0.35)

        self.play(FadeIn(h), FadeIn(regla), run_time=0.6)
        self.play(*[Create(e) for e in ar.values()],
                  *[FadeIn(nodos[v]) for v in nodos],
                  *[FadeIn(etq[v]) for v in etq],
                  FadeIn(info), run_time=1.5 * rt)
        self.wait(1.2 * rt)

        apagadas = set()
        for k, est in enumerate(traza, 1):
            hojas = est["hojas"]
            nuevo = Text(
                f"Ronda {k}: hojas = {sorted(hojas)}   ·   "
                f"nodos {est['antes']} → {est['despues']}",
                font_size=26, color=ORANGE).to_edge(DOWN, buff=0.35)
            self.play(*[nodos[u][0].animate.set_fill(C_HOJA) for u in hojas],
                      Transform(info, nuevo), run_time=0.9 * rt)
            self.wait(0.9 * rt)
            anims = []
            for u in hojas:
                anims += [nodos[u][0].animate.set_fill(GREY_D, 0.12)
                          .set_stroke(GREY_D, opacity=0.25),
                          nodos[u][1].animate.set_opacity(0.2),
                          FadeOut(etq[u])]
            for e, linea in ar.items():
                if e not in apagadas and (e[0] in hojas or e[1] in hojas):
                    apagadas.add(e)
                    anims.append(linea.animate.set_stroke(opacity=0.1))
            muertos = {u for est2 in traza[:k] for u in est2["hojas"]}
            for v in range(n):
                if v in muertos:
                    continue
                if est["grados"][v] != grados[v]:
                    grados[v] = est["grados"][v]
                    nueva = self.etiqueta_junto(nodos[v], grados[v])
                    anims.append(ReplacementTransform(etq[v], nueva))
                    etq[v] = nueva
            self.play(*anims, run_time=1.1 * rt)
            self.wait(0.7 * rt)

        fin = Text(f"Quedan {len(centros)} nodo(s): centro = {sorted(centros)}",
                   font_size=28, color=GREEN).to_edge(DOWN, buff=0.35)
        self.play(*[nodos[c][0].animate.set_fill(C_CENTRO) for c in centros],
                  *[Indicate(nodos[c], color=GREEN, scale_factor=1.5)
                    for c in centros],
                  Transform(info, fin), run_time=1.3)
        self.wait(1.5 * rt)
        return centros, traza

    def demo_principal(self):
        centros, traza = self.pelar("Demostración: árbol de 11 nodos",
                                    ARB_N, ARB_E, ARB_POS, rt=1.0)
        self.limpiar()

        ecc = excentricidades(ARB_N, ARB_E)
        h = self.encabezado("Verificación con la definición")
        nodos, ar = self.crear_arbol(ARB_N, ARB_E, ARB_POS)
        etq = {v: self.etiqueta_junto(nodos[v], ecc[v], color=YELLOW)
               for v in nodos}
        minimo = min(ecc)
        argmin = [v for v in range(ARB_N) if ecc[v] == minimo]
        assert sorted(argmin) == sorted(centros)
        for v in argmin:
            nodos[v][0].set_fill(C_CENTRO)
        txt = Text("exc(v) por BFS desde cada nodo (amarillo)", font_size=26)
        txt.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(h), *[Create(e) for e in ar.values()],
                  *[FadeIn(nodos[v]) for v in nodos],
                  *[FadeIn(etq[v]) for v in etq], FadeIn(txt))
        self.wait(1.5)
        res = Text(
            f"radio = min exc = {minimo}   ·   diámetro = max exc = {max(ecc)}"
            f"   ·   rondas = {len(traza)} = radio",
            font_size=26, color=GREEN).to_edge(DOWN, buff=0.35)
        self.play(Transform(txt, res))
        self.wait(2.5)
        self.limpiar()

    def casos_borde(self):
        self.pelar("Caso borde 1: un solo nodo (n = 1)",
                   1, [], {0: (0, 0)}, rt=0.7)
        self.limpiar()
        self.pelar("Caso borde 2: dos nodos (n = 2)",
                   2, [(0, 1)], {0: (-1.2, 0), 1: (1.2, 0)}, rt=0.7)
        self.limpiar()
        self.pelar("Caso borde 3: camino de 6 nodos (2 centros)",
                   CAM_N, CAM_E, CAM_POS, rt=0.8)
        self.limpiar()

    def complejidad(self):
        h = self.encabezado("Complejidad")
        a = Text("Cada nodo se vuelve hoja y se quita una sola vez.",
                 font_size=27)
        b = Text("Cada arista se revisa una sola vez (al quitar su hoja).",
                 font_size=27)
        f = Text("T(n) = O(n) + O(n − 1) = O(n)", font_size=44, color=GREEN)
        e = Text("Espacio: O(n)", font_size=36)
        ing = Text("Ingenuo (BFS desde cada nodo): O(n²).", font_size=26,
                   color=RED_B)
        pc = Text("Peor caso en rondas: camino, ≈ n/2 rondas, pero el trabajo total sigue siendo O(n).",
                  font_size=24, color=YELLOW)
        g = VGroup(a, b, f, e, ing, pc).arrange(DOWN, buff=0.38)
        g.next_to(h, DOWN, buff=0.45)
        self.play(FadeIn(h))
        self.play(FadeIn(a), run_time=0.8)
        self.wait(0.6)
        self.play(FadeIn(b), run_time=0.8)
        self.wait(0.6)
        self.play(FadeIn(f), run_time=1.2)
        self.play(FadeIn(e))
        self.wait(0.8)
        self.play(FadeIn(ing))
        self.wait(0.8)
        self.play(FadeIn(pc))
        self.wait(3)
        self.limpiar()

    def creditos(self):
        t = Text("Centro de un árbol", font_size=48, weight=BOLD)
        s = Text("CS2023 · Algoritmos y Estructuras de Datos · 2026-2",
                 font_size=24, color=GREY_B)
        ref = Text("Estilo inspirado en 3Blue1Brown · hecho con Manim Community",
                   font_size=22, color=GREY_B)
        g = VGroup(t, s, ref).arrange(DOWN, buff=0.45)
        self.play(FadeIn(g), run_time=1)
        self.wait(3)
        self.play(FadeOut(g))
