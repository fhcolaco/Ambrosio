import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import tkintermapview
from functions import *
from algorithms import *

DEPTH_LIMIT = 3  # Limite de profundidade para a pesquisa em profundidade limitada (DLS)

class MapApp:
    def __init__(self):
        # Inicializa os dados e a interface gráfica
        self.cached_locations = loadCachedLocations()
        self.selected_file = None
        self.cities = []
        self.city_names = []
        self.algorithms = ['DLS', 'A*', 'Greedy Search', 'Uniform Cost']
        self.map_view = None

        self.root = tk.Tk()
        self.root.tk.call('source', 'style/forest-light.tcl')
        ttk.Style().theme_use('forest-light')
        
        # Configuração do tamanho e posicionamento da janela principal
        window_width, window_height = 1280, 720
        screen_width, screen_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.title("Projeto IA")
        self.root.configure(background='#DDD')

        # Criação do frame lateral para os controles
        self.left_frame = tk.Frame(self.root, width=200, background='#DDD')
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, ipadx=15)

        self._create_widgets()

    def _create_widgets(self):
        # Botão para selecionar o ficheiro do mapa
        self.select_map_file_button = ttk.Button(
            self.left_frame, text="Select Map File", command=self.select_map_file, width=20, style='Accent.TButton'
        )
        self.select_map_file_button.pack(pady=(20, 0))

        # Combobox para a cidade de partida
        self.start_city_label = tk.Label(self.left_frame, text="Start City:", width=20, background='#DDD')
        self.start_city_label.pack(pady=(10, 0))
        self.start_city_combobox = ttk.Combobox(
            self.left_frame, values=['Select map first'], width=20, state="disabled"
        )
        self.start_city_combobox.set(self.start_city_combobox['values'][0])
        self.start_city_combobox.bind("<<ComboboxSelected>>", self.populate_cities)
        self.start_city_combobox.pack()

        # Combobox para a cidade de destino
        self.end_city_label = tk.Label(self.left_frame, text="End City:", width=20, background='#DDD')
        self.end_city_label.pack(pady=(10, 0))
        self.end_city_combobox = ttk.Combobox(
            self.left_frame, values=['Select map first'], width=20, state="disabled"
        )
        self.end_city_combobox.set(self.end_city_combobox['values'][0])
        self.end_city_combobox.bind("<<ComboboxSelected>>", self.populate_cities)
        self.end_city_combobox.pack()

        # Combobox para selecionar o algoritmo de pesquisa
        self.algorithm_label = tk.Label(self.left_frame, text="Algorithm:", width=20, background='#DDD')
        self.algorithm_label.pack(pady=(10, 0))
        self.algorithm_combobox = ttk.Combobox(
            self.left_frame, values=self.algorithms, width=20, state="disabled"
        )
        self.algorithm_combobox.set(self.algorithms[0])
        self.algorithm_combobox.pack()

        # Botão para calcular o percurso
        self.calculate_route_button = ttk.Button(
            self.left_frame, text="Calculate Route", command=self.handle_calculate_route, state="disabled", width=25
        )
        self.calculate_route_button.pack(pady=(10, 0))

        # Botão para adicionar marcadores e caminhos no mapa
        self.add_markers_and_paths_button = ttk.Button(
            self.left_frame, text="Add Markers and Paths", command=self.add_paths_to_map, state="disabled", width=25
        )
        self.add_markers_and_paths_button.pack(pady=(10, 0))

        # Botão para limpar os marcadores e os caminhos
        self.clear_markers_and_distances_button = ttk.Button(
            self.left_frame, text="Clear Markers", command=self.clear_markers_and_paths, state="disabled", width=25
        )
        self.clear_markers_and_distances_button.pack(pady=(10, 0))

        # Listbox para exibir o percurso calculado
        self.path_list = tk.Listbox(self.left_frame, width=25, height=10, font=("Courier New", 10))
        self.path_list.pack(pady=(10, 0))

        # Mensagem central que indica a necessidade de selecionar um ficheiro de mapa
        self.select_map_message = tk.Label(
            self.root, text="Select a file to load the map.", font=("Arial", 16), foreground="#666", background="#DDD"
        )
        self.select_map_message.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def handle_calculate_route(self):
        # Limpa a listbox e obtém as seleções efetuadas pelo utilizador
        self.path_list.delete(0, tk.END)
        start_city_name = self.start_city_combobox.get()
        end_city_name = self.end_city_combobox.get()
        algorithm = self.algorithm_combobox.get()

        # Obtém os objetos correspondentes às cidades selecionadas
        start_city = next(city for city in self.cities if city.getName() == start_city_name)
        end_city = next(city for city in self.cities if city.getName() == end_city_name)

        # Seleciona o algoritmo de cálculo do percurso
        if algorithm == "DLS":
            route = depth_limited_search(self.cities, start_city, end_city, DEPTH_LIMIT)
        elif algorithm == "A*":
            route = a_star(self.cities, start_city, end_city)
        elif algorithm == "Greedy Search":
            route = greedy_search(self.cities, start_city, end_city)
        elif algorithm == "Uniform Cost":
            route = uniform_cost(self.cities, start_city, end_city)
        else:
            route = None

        self.display_calculated_path(route)

    def select_map_file(self):
        try:
            # Solicita ao utilizador a seleção de um ficheiro de mapa
            self.selected_file = filedialog.askopenfilename(
                filetypes=[("Text files", "*.txt"), ("Excel files", "*.xlsx"), ("CSV files", "*.csv")]
            )
            if not self.selected_file:
                return  # Caso o utilizador cancele a seleção

            # Processa o ficheiro com base na sua extensão
            if self.selected_file.endswith('.xlsx'):
                country_name, new_cities = parseExcelFile(self.selected_file, self.cached_locations)
            else:
                country_name, new_cities = parseTextFile(self.selected_file, self.cached_locations)

            self.city_names = sorted([city.name for city in new_cities])
            self.cities = new_cities

            # Obtém a localização geográfica do país e atualiza (ou carrega) o mapa
            country_location = getGeolocation(country_name, self.cached_locations)
            if self.map_view:
                self.map_view.set_position(country_location[0], country_location[1])
            else:
                self.map_view = self.load_map(country_location)

            self.clear_markers_and_paths()
            self.populate_cities()  # Atualiza os comboboxes com as cidades

            print(f"Number of cities: {len(self.cities)}")
            for city in self.cities:
                city.printConnections()

            # Ativa os widgets após carregar o mapa
            self.start_city_combobox.config(state="readonly")
            self.end_city_combobox.config(state="readonly")
            self.algorithm_combobox.config(state="readonly")
            self.calculate_route_button.config(state="normal")
            self.add_markers_and_paths_button.config(state="normal")
            self.clear_markers_and_distances_button.config(state="normal")
        except Exception as e:
            print("Error:", str(e))

    def populate_cities(self, event=None):
        if event is None:
            # Preenche os comboboxes com as cidades disponíveis
            if self.city_names:
                self.start_city_combobox['values'] = [self.city_names[0]] + self.city_names[2:]
                self.end_city_combobox['values'] = self.city_names[1:]
                self.start_city_combobox.set(self.city_names[0])
                self.end_city_combobox.set(self.city_names[1])
        else:
            # Atualiza as opções para evitar a seleção duplicada
            widget = event.widget
            if widget == self.start_city_combobox:
                self.end_city_combobox['values'] = [city for city in self.city_names if city != self.start_city_combobox.get()]
            elif widget == self.end_city_combobox:
                self.start_city_combobox['values'] = [city for city in self.city_names if city != self.end_city_combobox.get()]

    def clear_markers_and_paths(self):
        # Remove todos os marcadores e caminhos do mapa e limpa a listbox
        self.path_list.delete(0, tk.END)
        if self.map_view:
            self.map_view.delete_all_marker()
            self.map_view.delete_all_path()

    def add_markers_to_all_locations(self):
        # Adiciona marcadores para todas as cidades com base na sua geolocalização
        if self.map_view:
            self.map_view.delete_all_marker()
            for city in self.city_names:
                location = getGeolocation(city, self.cached_locations)
                self.map_view.set_marker(location[0], location[1], city)

    def display_calculated_path(self, path_cost):
        self.clear_markers_and_paths()
        if path_cost:
            path, cost = path_cost
            cost.insert(0, 0)  # Insere custo zero no início
            total_cost = sum(map(int, cost))
            print(f"Route: {path_cost}")
            print(f"Total Cost: {total_cost}")

            previous_city_location = None
            # Itera por cada cidade no percurso e atualiza a listbox e o mapa
            for city in path:
                accumulated_cost = sum(map(int, cost[:path.index(city) + 1]))
                spaces = " " * (22 - len(city))
                self.path_list.insert(tk.END, f"{city}{spaces}{accumulated_cost}")
                location = getGeolocation(city, self.cached_locations)
                self.map_view.set_marker(location[0], location[1], city)
                if previous_city_location:
                    self.map_view.set_path([previous_city_location, (location[0], location[1])])
                previous_city_location = (location[0], location[1])

    def add_paths_to_map(self):
        if self.map_view:
            self.map_view.delete_all_path()
            self.add_markers_to_all_locations()
            # Adiciona caminhos entre as cidades com base nas ligações definidas
            for city in self.cities:
                for connection_data in city.getConnections():
                    connection_city = next(c for c in self.cities if c.getName() == connection_data['name'])
                    path = [(city.latitude, city.longitude), (connection_city.latitude, connection_city.longitude)]
                    self.map_view.set_path(path)

    def load_map(self, country_location):
        # Oculta a mensagem de seleção e inicializa o widget do mapa
        self.select_map_message.place_forget()
        map_view = tkintermapview.TkinterMapView(self.root, width=1000, height=700)
        map_view.set_position(country_location[0], country_location[1])
        map_view.set_zoom(7)
        map_view.pack(fill=tk.BOTH, expand=True)
        return map_view

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = MapApp()
    app.run()
