# Centro de un árbol — Pelado de hojas en O(n)

Proyecto 2 del curso **CS2023 · Algoritmos y Estructuras de Datos (2026-2)**.

## Descripción del proyecto

El **centro de un árbol** es el nodo (o par de nodos adyacentes) cuya **excentricidad** es mínima, es decir, el nodo que minimiza la distancia al nodo más lejano:

- `exc(v) = max d(v, u)` sobre todos los nodos `u`
- `centro = v` con `exc(v)` mínima

Todo árbol tiene **1 o 2 centros**; si son 2, son adyacentes.

### Algoritmo: pelado de hojas (*leaf trimming*)

En lugar de lanzar un BFS desde cada nodo (O(n²)), se eliminan **todas las hojas capa por capa** (como un BFS topológico) hasta que quedan 1 o 2 nodos. Esos son los centros.

1. Calcular el grado de cada nodo y encolar las hojas (grado 1).
2. Mientras queden más de 2 nodos: quitar todas las hojas de la ronda actual, decrementar el grado de sus vecinos y encolar los que pasen a ser hojas.
3. Los nodos que quedan en la cola son los centros.

| | Tiempo | Espacio |
|---|---|---|
| Pelado de hojas | **O(n)** | O(n) |
| Ingenuo (BFS desde cada nodo) | O(n²) | O(n) |

Cada nodo se quita una sola vez y cada arista se revisa una sola vez. El número de rondas es igual al radio del árbol.

**Aplicaciones:** elegir la raíz que minimiza la altura del árbol, ubicar un servidor/hub minimizando el peor retardo, calcular el diámetro (`2·radio` con 1 centro, `2·radio − 1` con 2 centros).

### Estructura del repositorio

```
Proyecto_2_AED/
├── centro_arbol.cpp        # Implementación en C++ (clases Arbol y ArbolCentro)
└── Animacion/
    └── centro_arbol.py     # Video explicativo hecho con Manim Community
```

- **`centro_arbol.cpp`**
  - `Arbol`: árbol no dirigido con lista de adyacencia (`agregarArista`, `vecinos`, `grado`).
  - `ArbolCentro` (hereda de `Arbol`): `esHoja` y `encontrarCentros()`, que devuelve un `vector<int>` con 1 o 2 centros.
- **`Animacion/centro_arbol.py`** — escena `CentroDeUnArbol`: definición, idea del algoritmo, demostración paso a paso sobre un árbol de 11 nodos, verificación por excentricidades (BFS), casos borde (n = 1, n = 2, camino de 6 nodos) y análisis de complejidad.

## Software requerido

### Implementación en C++
- Compilador **g++ ≥ 7** (o Clang) con soporte para **C++17**
  - Linux: `sudo apt install g++`
  - Windows: MinGW-w64 / MSYS2
  - macOS: `xcode-select --install`

> El código usa `<bits/stdc++.h>`, que es propio de GCC. En Clang/MSVC reemplázalo por `<vector>`, `<queue>` e `<iostream>`.

### Animación
- **Python 3.10+** (probado con 3.12)
- **Manim Community** (`manim`)
- **FFmpeg** (lo usa Manim para generar el video)
- Dependencias de sistema de Manim (Cairo y Pango). No se necesita LaTeX: la animación solo usa `Text`.

Guía oficial de instalación: https://docs.manim.community/en/stable/installation.html

## Compilación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/maydelithzuniga/Proyecto_2_AED.git
cd Proyecto_2_AED
```

### 2. C++

`centro_arbol.cpp` contiene solo las clases (no tiene `main`). Para probarlo, crea un archivo `main.cpp` en la misma carpeta:

```cpp
#include "centro_arbol.cpp"

int main() {
    int n;
    cin >> n;                       // número de nodos
    ArbolCentro arbol(n);
    for (int i = 0; i < n - 1; i++) {
        int u, v;
        cin >> u >> v;              // aristas (nodos indexados desde 0)
        arbol.agregarArista(u, v);
    }
    for (int c : arbol.encontrarCentros()) cout << c << " ";
    cout << "\n";
    return 0;
}
```

Compilar y ejecutar:

```bash
g++ -std=c++17 -O2 main.cpp -o centro
./centro            # en Windows: centro.exe
```

**Formato de entrada:** primera línea `n`; luego `n − 1` líneas con las aristas `u v` (0-indexado).

**Ejemplo 1** — árbol de 11 nodos (el mismo de la animación):

```bash
echo "11
0 1
1 2
2 3
3 4
4 5
5 6
3 7
7 8
4 9
2 10" | ./centro
```
Salida: `3`

**Ejemplo 2** — camino de 6 nodos (2 centros):

```bash
echo "6
0 1
1 2
2 3
3 4
4 5" | ./centro
```
Salida: `2 3`

### 3. Animación (Manim)

Instalar Manim (dentro de un entorno virtual, recomendado):

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install manim
```

Renderizar la escena:

```bash
cd Animacion
manim -pql centro_arbol.py CentroDeUnArbol    # calidad baja (480p15), rápido
manim -pqh centro_arbol.py CentroDeUnArbol    # calidad alta (1080p60)
```

- `-p` abre el video al terminar.
- `-ql` / `-qm` / `-qh` / `-qk` → calidad baja / media / alta / 4K.

El video se guarda en:

```
Animacion/media/videos/centro_arbol/<calidad>/CentroDeUnArbol.mp4
```

## Referencias
- Manim Community — https://www.manim.community/
- Estilo visual inspirado en 3Blue1Brown.
