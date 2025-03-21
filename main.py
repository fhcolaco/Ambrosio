import heapq
from collections import deque

# Distância quilométrica entre cidades Portuguesas
cidades = {
    'Aveiro': {'Porto': 68, 'Viseu': 95, 'Coimbra': 68, 'Leiria': 115},
    'Braga': {'Viana do Castelo': 48, 'Vila Real': 106, 'Porto': 53},
    'Bragança': {'Vila Real': 137, 'Guarda': 202},
    'Beja': {'Évora': 78, 'Faro': 152, 'Setúbal': 142},
    'Castelo Branco': {'Coimbra': 159, 'Guarda': 106, 'Portalegre': 80, 'Évora': 203},
    'Coimbra': {'Viseu': 96, 'Leiria': 67},
    'Évora': {'Lisboa': 150, 'Santarém': 117, 'Portalegre': 131, 'Setúbal': 103},
    'Faro': {'Setúbal': 249, 'Lisboa': 299},
    'Guarda': {'Vila Real': 157, 'Viseu': 85},
    'Leiria': {'Lisboa': 129, 'Santarém': 70},
    'Lisboa': {'Santarém': 78, 'Setúbal': 50},
    'Porto': {'Viana do Castelo': 71, 'Vila Real': 116, 'Viseu': 133},
    'Vila Real': {'Viseu': 110}
}

# Distância quilométrica em linha reta entre diferentes cidades e Faro
heuristica = {
    'Aveiro': 366, 'Braga': 454, 'Bragança': 487, 'Beja': 99, 'Castelo Branco': 280,
    'Coimbra': 319, 'Évora': 157, 'Faro': 0, 'Guarda': 352, 'Leiria': 278,
    'Lisboa': 195, 'Portalegre': 228, 'Porto': 418, 'Santarém': 231, 'Setúbal': 168,
    'Viana do Castelo': 473, 'Vila Real': 429, 'Viseu': 363
}

def tornar_bidirecional(grafo):
    bidirecional = {}
    for cidade, adjacentes in grafo.items():
        if cidade not in bidirecional:
            bidirecional[cidade] = {}
        for adj, dist in adjacentes.items():
            if adj not in bidirecional:
                bidirecional[adj] = {}
            bidirecional[cidade][adj] = dist
            bidirecional[adj][cidade] = dist
    return bidirecional

cidades = tornar_bidirecional(cidades)

def custo_uniforme(origem, destino):
    fila = []
    heapq.heappush(fila, (0, origem, [origem]))
    visitados = set()
    iteracao = 0

    while fila:
        custo, cidade_atual, caminho = heapq.heappop(fila)
        iteracao += 1

        if cidade_atual in visitados:
            continue
        visitados.add(cidade_atual)

        print(f"Iteração #{iteracao} | Cidade atual: {cidade_atual}, Custo acumulado: {custo}, Caminho: {' -> '.join(caminho)}")

        if cidade_atual == destino:
            return caminho, custo

        for adjacente, distancia in cidades.get(cidade_atual, {}).items():
            if adjacente not in visitados:
                novo_custo = custo + distancia
                heapq.heappush(fila, (novo_custo, adjacente, caminho + [adjacente]))

    return None, float('inf')

def aprofundamento_progressivo(origem, destino, profundidade_max):
    def busca_limitada(cidade_atual, destino, profundidade, caminho, custo):
        if profundidade == 0 and cidade_atual == destino:
            return caminho, custo
        if profundidade > 0:
            for adjacente, distancia in cidades.get(cidade_atual, {}).items():
                if adjacente not in caminho:
                    resultado = busca_limitada(adjacente, destino, profundidade - 1, caminho + [adjacente], custo + distancia)
                    if resultado:
                        return resultado
        return None

    for profundidade in range(profundidade_max + 1):
        resultado = busca_limitada(origem, destino, profundidade, [origem], 0)
        if resultado:
            return resultado
    return None, float('inf')


def procura_sofrega(origem, destino):
    fila = []
    heapq.heappush(fila, (heuristica[origem], origem, [origem], 0))
    visitados = set()

    while fila:
        _, cidade_atual, caminho, custo = heapq.heappop(fila)

        if cidade_atual in visitados:
            continue
        visitados.add(cidade_atual)

        if cidade_atual == destino:
            return caminho, custo

        for adjacente, distancia in cidades[cidade_atual].items():
            if adjacente not in visitados:
                heapq.heappush(fila, (heuristica[adjacente], adjacente, caminho + [adjacente], custo + distancia))

    return None, float('inf')


def a_star(origem, destino):
    fila = []
    heapq.heappush(fila, (heuristica[origem], 0, origem, [origem]))
    visitados = set()

    while fila:
        _, custo, cidade_atual, caminho = heapq.heappop(fila)

        if cidade_atual in visitados:
            continue
        visitados.add(cidade_atual)

        if cidade_atual == destino:
            return caminho, custo

        for adjacente, distancia in cidades[cidade_atual].items():
            if adjacente not in visitados:
                novo_custo = custo + distancia
                heapq.heappush(fila, (novo_custo + heuristica[adjacente], novo_custo, adjacente, caminho + [adjacente]))

    return None, float('inf')

if __name__ == '__main__':
    origem = 'Porto'
    destino = 'Faro'
    profundidade_maxima = 10
    caminho, distancia = custo_uniforme(origem, destino)

    print(f"\nCusto Uniforme:")
    if caminho:
        print(f"Caminho encontrado: {' -> '.join(caminho)}")
        print(f"Distância total: {distancia} km")
    else:
        print("Nenhum caminho encontrado.")

    caminho, custo = aprofundamento_progressivo(origem, destino, profundidade_maxima)
    print(f"\nAprofundamento Progressivo:")
    if caminho:
        print(f"Caminho encontrado: {' -> '.join(caminho)}")
        print(f"Distância total: {custo} km")
    else:
        print("Nenhum caminho encontrado.")

    caminho_sofrega, custo_sofrega = procura_sofrega(origem, destino)
    print(f"\nProcura Sôfrega: {' -> '.join(caminho_sofrega)} com custo {custo_sofrega} km")

    caminho_astar, custo_astar = a_star(origem, destino)
    print(f"\nProcura A*: {' -> '.join(caminho_astar)} com custo {custo_astar} km")