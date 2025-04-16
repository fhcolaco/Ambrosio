import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import tkintermapview
from functions import *
from algorithms import *

DEPTH_LIMIT = 3  # Limite de profundidade para a pesquisa em profundidade limitada (DLS)

# Configuração global do CustomTkinter: modo Dark e tema com cores vibrantes
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")  # Você pode testar com "green", "blue", "dark-blue", etc.

class MapApp:
    def __init__(self):
        # Inicializa os dados e a interface gráfica
        self.cached_locations = loadCachedLocations()
        self.selected_file = None
        self.cities = []
        self.city_names = []
        self.algorithms = ['DLS', 'A*', 'Greedy Search', 'Uniform Cost']
        self.map_view = None

        # Cria a janela principal usando CustomTkinter
        self.root = ctk.CTk()
        self.root.geometry("1280x720")
        self.root.title("Projeto IA")
        self.root.configure(bg="#1F1F1F")

        # Criação de um frame principal com padding para simular o "container" moderno
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=15, fg_color="#2B2B2B")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Frame lateral para os controles, estilizado com corner radius e cor de fundo diferenciada
        self.left_frame = ctk.CTkFrame(self.main_frame, width=250, corner_radius=15, fg_color="#3C3C3C")
        self.left_frame.pack(side="left", fill="y", padx=(20,10), pady=20)

        # Área central para o mapa
        self.center_frame = ctk.CTkFrame(self.main_frame, corner_radius=15, fg_color="#2B2B2B")
        self.center_frame.pack(side="right", fill="both", expand=True, padx=(10,20), pady=20)

        self._create_widgets()

    def _create_widgets(self):
        # Botão para selecionar o ficheiro do mapa
        self.select_map_file_button = ctk.CTkButton(
            self.left_frame, text="Select Map File",
            command=self.select_map_file,
            width=200, corner_radius=10
        )
        self.select_map_file_button.pack(pady=(20, 10))

        # Combobox para a cidade de partida
        self.start_city_label = ctk.CTkLabel(self.left_frame, text="Start City:")
        self.start_city_label.pack(pady=(10, 0))
        self.start_city_combobox = ctk.CTkComboBox(
            self.left_frame, values=['Select map first'], width=200
        )
        self.start_city_combobox.set('Select map first')
        self.start_city_combobox.bind("<<ComboboxSelected>>", self.populate_cities)
        self.start_city_combobox.pack(pady=(5, 10))

        # Combobox para a cidade de destino
        self.end_city_label = ctk.CTkLabel(self.left_frame, text="End City:")
        self.end_city_label.pack(pady=(10, 0))
        self.end_city_combobox = ctk.CTkComboBox(
            self.left_frame, values=['Select map first'], width=200
        )
        self.end_city_combobox.set('Select map first')
        self.end_city_combobox.bind("<<ComboboxSelected>>", self.populate_cities)
        self.end_city_combobox.pack(pady=(5, 10))

        # Combobox para selecionar o algoritmo de pesquisa
        self.algorithm_label = ctk.CTkLabel(self.left_frame, text="Algorithm:")
        self.algorithm_label.pack(pady=(10, 0))
        self.algorithm_combobox = ctk.CTkComboBox(
            self.left_frame, values=self.algorithms, width=200
        )
        self.algorithm_combobox.set(self.algorithms[0])
        self.algorithm_combobox.pack(pady=(5, 10))

        # Botão para calcular o percurso
        self.calculate_route_button = ctk.CTkButton(
            self.left_frame, text="Calculate Route",
            command=self.handle_calculate_route,
            state="disabled", width=210, corner_radius=10
        )
        self.calculate_route_button.pack(pady=(10, 5))

        # Botão para adicionar marcadores e caminhos no mapa
        self.add_markers_and_paths_button = ctk.CTkButton(
            self.left_frame, text="Add Markers and Paths",
            command=self.add_paths_to_map,
            state="disabled", width=210, corner_radius=10
        )
        self.add_markers_and_paths_button.pack(pady=(5, 5))

        # Botão para limpar os marcadores e os caminhos
        self.clear_markers_and_distances_button = ctk.CTkButton(
            self.left_frame, text="Clear Markers",
            command=self.clear_markers_and_paths,
            state="disabled", width=210, corner_radius=10
        )
        self.clear_markers_and_distances_button.pack(pady=(5, 15))

        # Caixa de texto para exibir o percurso calculado (substituindo Listbox para melhor integração visual)
        self.path_textbox = ctk.CTkTextbox(self.left_frame, width=220, height=150, corner_radius=10)
        self.path_textbox.configure(state="disabled")
        self.path_textbox.pack(pady=(5, 20))

        # Mensagem central que indica a necessidade de selecionar um ficheiro de mapa
        self.select_map_message = ctk.CTkLabel(
            self.center_frame, text="Select a file to load the map.", font=("Arial", 20),
            text_color="#CCCCCC", bg_color="transparent"
        )
        self.select_map_message.place(relx=0.5, rely=0.5, anchor="center")

    def handle_calculate_route(self):
        # Limpa a caixa de texto e obtém as seleções efetuadas pelo utilizador
        self.path_textbox.configure(state="normal")
        self.path_textbox.delete("1.0", tk.END)
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
            self.populate_cities()  # Atualiza as comboboxes com as cidades

            print(f"Number of cities: {len(self.cities)}")
            for city in self.cities:
                city.printConnections()

            # Ativa os widgets após carregar o mapa
            self.start_city_combobox.configure(state="readonly")
            self.end_city_combobox.configure(state="readonly")
            self.algorithm_combobox.configure(state="readonly")
            self.calculate_route_button.configure(state="normal")
            self.add_markers_and_paths_button.configure(state="normal")
            self.clear_markers_and_distances_button.configure(state="normal")
        except Exception as e:
            print("Error:", str(e))

    def populate_cities(self, event=None):
        if not self.city_names:
            return
        if event is None:
            self.start_city_combobox.configure(values=[self.city_names[0]] + self.city_names[2:])
            self.end_city_combobox.configure(values=self.city_names[1:])
            self.start_city_combobox.set(self.city_names[0])
            self.end_city_combobox.set(self.city_names[1])
        else:
            widget = event.widget
            if widget == self.start_city_combobox:
                self.end_city_combobox.configure(values=[city for city in self.city_names if city != self.start_city_combobox.get()])
            elif widget == self.end_city_combobox:
                self.start_city_combobox.configure(values=[city for city in self.city_names if city != self.end_city_combobox.get()])

    def clear_markers_and_paths(self):
        # Remove todos os marcadores e caminhos do mapa e limpa a caixa de texto
        self.path_textbox.configure(state="normal")
        self.path_textbox.delete("1.0", tk.END)
        self.path_textbox.configure(state="disabled")
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
            output = f"Total Cost: {total_cost}\nRoute:\n"
            previous_city_location = None
            for city in path:
                accumulated_cost = sum(map(int, cost[:path.index(city) + 1]))
                output += f"{city:22} {accumulated_cost}\n"
                location = getGeolocation(city, self.cached_locations)
                self.map_view.set_marker(location[0], location[1], city)
                if previous_city_location:
                    self.map_view.set_path([previous_city_location, (location[0], location[1])])
                previous_city_location = (location[0], location[1])
            self.path_textbox.configure(state="normal")
            self.path_textbox.insert("1.0", output)
            self.path_textbox.configure(state="disabled")

    def add_paths_to_map(self):
        if self.map_view:
            self.map_view.delete_all_path()
            self.add_markers_to_all_locations()
            for city in self.cities:
                for connection_data in city.getConnections():
                    connection_city = next(c for c in self.cities if c.getName() == connection_data['name'])
                    path = [(city.latitude, city.longitude), (connection_city.latitude, connection_city.longitude)]
                    self.map_view.set_path(path)

    def load_map(self, country_location):
        # Oculta a mensagem de seleção e inicializa o widget do mapa na área central
        self.select_map_message.place_forget()
        map_view = tkintermapview.TkinterMapView(self.center_frame, width=800, height=700)
        map_view.set_position(country_location[0], country_location[1])
        map_view.set_zoom(7)
        map_view.pack(fill=tk.BOTH, expand=True)
        return map_view

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = MapApp()
    app.run()
