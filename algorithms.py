from functions import *

def get_city_object(cities, city_name):
    # Retorna a primeira cidade cujo nome corresponde a city_name
    return next(city for city in cities if city.getName() == city_name)


def uniform_cost_algorithm_build_path(is_append_start_city, current_city, connection_distance, start_city=None, lowest_cost_path=None):
    # Constrói um novo percurso com base na cidade atual e no percurso anterior (se existir)
    if is_append_start_city:
        aux_paths = [start_city.getName()]
        aux_costs = []
        aux_total_cost = 0
    else:
        aux_paths = lowest_cost_path["paths"].copy()
        aux_costs = lowest_cost_path["costs"].copy()
        aux_total_cost = lowest_cost_path["total_cost"]

    aux_paths.append(current_city.getName())
    aux_costs.append(int(connection_distance))
    aux_total_cost += int(connection_distance)

    return {"paths": aux_paths, "costs": aux_costs, "total_cost": aux_total_cost}


def uniform_cost_algorithm(cities, start_city, end_city, is_from_a_star=False):
    # Executa o algoritmo de custo uniforme (ou A* se is_from_a_star for True)
    paths = []
    complete_path = None
    lowest_cost_path = None
    latest_lowest_cost_path = None
    first_iteration = True

    while True:
        for connection in start_city.getConnections():
            city = get_city_object(cities, connection["name"])
            new_path = uniform_cost_algorithm_build_path((not paths) or first_iteration, city,
                                                         connection["distance"], start_city, lowest_cost_path)
            paths.append(new_path)
            if city.getName() == end_city.getName():
                if complete_path is None or new_path["total_cost"] < complete_path["total_cost"]:
                    complete_path = new_path

        if first_iteration:
            first_iteration = False

        # Seleciona o percurso com menor custo acumulado (acrescenta a heurística se A* estiver activo)
        lowest_cost_path = min(
            paths,
            key=lambda path: path["total_cost"] + (h(start_city, end_city) if is_from_a_star else 0)
        )

        # Se encontrar um percurso completo com custo inferior, retorna-o
        if complete_path is not None and complete_path["total_cost"] < lowest_cost_path["total_cost"]:
            result = (complete_path["paths"], complete_path["costs"])
            complete_path = None
            paths.clear()
            return result

        # Expande o percurso de menor custo
        if lowest_cost_path != latest_lowest_cost_path or latest_lowest_cost_path is None:
            latest_lowest_cost_path = lowest_cost_path
            next_city = get_city_object(cities, lowest_cost_path["paths"][-1])
            paths.remove(lowest_cost_path)
            start_city = next_city


def uniform_cost(cities, start_city, end_city):
    # Função wrapper para o algoritmo de custo uniforme
    return uniform_cost_algorithm(cities, start_city, end_city)


def depth_limited_search(cities, start_city, end_city, depth_limit):
    # Procura em profundidade limitada; retorna listas de nomes de cidades e respetivos custos
    if depth_limit == 0:
        return [], []

    for connection in start_city.getConnections():
        city = get_city_object(cities, connection["name"])
        if city.getName() == end_city.getName():
            return [start_city.getName(), city.getName()], [int(connection["distance"])]

        path = depth_limited_search(cities, city, end_city, depth_limit - 1)
        if path is not None and path[0]:
            return [start_city.getName()] + path[0], [int(connection["distance"])] + path[1]

    # Se nenhum percurso for encontrado, retorna listas vazias
    return [], []


def greedy_search(cities, start_city, end_city, greedypath=None, greedycost=None):
    # Procura gananciosa que utiliza uma heurística para selecionar o próximo nó
    if greedypath is None:
        greedypath = []
    if greedycost is None:
        greedycost = []

    greedypath.append(start_city.getName())

    # Verifica se existe ligação directa para a cidade de destino
    for connection in start_city.getConnections():
        city = get_city_object(cities, connection["name"])
        if city.getName() == end_city.getName():
            greedypath.append(city.getName())
            greedycost.append(int(connection["distance"]))
            return greedypath.copy(), greedycost.copy()

    # Seleciona a cidade com o menor valor heurístico
    next_city = None
    next_city_distance = None
    min_heuristic = float('inf')
    for connection in start_city.getConnections():
        city = get_city_object(cities, connection["name"])
        heuristic_value = h(city, end_city)
        if heuristic_value < min_heuristic:
            min_heuristic = heuristic_value
            next_city = city
            next_city_distance = int(connection["distance"])

    if next_city is None:
        # Caso não haja caminho possível, retorna falha
        return [], []

    greedycost.append(next_city_distance)
    return greedy_search(cities, next_city, end_city, greedypath, greedycost)


def a_star(cities, start_city, end_city):
    # Função wrapper para o algoritmo A*, que utiliza o custo uniforme com heurística
    return uniform_cost_algorithm(cities, start_city, end_city, is_from_a_star=True)
