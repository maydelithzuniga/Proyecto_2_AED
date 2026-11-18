#include <bits/stdc++.h>
using namespace std;

class Arbol {
protected:
    int numVertices;
    vector<vector<int>> adyacencia;

public:
    Arbol(int n) : numVertices(n), adyacencia(n) {}

    virtual ~Arbol() = default;

    void agregarArista(int u, int v) {
        if (u >= 0 && u < numVertices && v >= 0 && v < numVertices) {
            adyacencia[u].push_back(v);
            adyacencia[v].push_back(u);
        }
    }

    const vector<int>& vecinos(int v) const {
        return adyacencia[v];
    }

    int grado(int v) const {
        return vecinos(v).size();
    }
};

class ArbolCentro : public Arbol {
public:
    ArbolCentro(int n) : Arbol(n) {}

    bool esHoja(int v) const {
        if (numVertices == 1) {
            return true;
        }
        return grado(v) == 1;
    }

    vector<int> encontrarCentros() const {
        vector<int> centros;

        if (numVertices == 0) return centros;
        if (numVertices == 1) return {0};

        vector<int> gradosActuales(numVertices);
        queue<int> hojas;

        for (int i = 0; i < numVertices; i++) {
            gradosActuales[i] = grado(i);

            if (esHoja(i)) {
                hojas.push(i);
            }
        }

        int nodosRestantes = numVertices;

        while (nodosRestantes > 2) {
            int cantidadHojas = hojas.size();
            nodosRestantes -= cantidadHojas;

            for (int i = 0; i < cantidadHojas; i++) {
                int hoja = hojas.front();
                hojas.pop();

                for (int vecino : vecinos(hoja)) {
                    gradosActuales[vecino]--;

                    if (gradosActuales[vecino] == 1) {
                        hojas.push(vecino);
                    }
                }
            }
        }

        while (!hojas.empty()) {
            centros.push_back(hojas.front());
            hojas.pop();
        }

        return centros;
    }
};