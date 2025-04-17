import pandas as pd
import matplotlib.pyplot as plt
import ast
import os
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class DataLoader:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.df = None

    def load_data(self):
        if not os.path.exists(self.filepath):
            raise FileNotFoundError("Fichier CSV introuvable.")
        self.df = pd.read_csv(self.filepath)
        self._parse_columns()
        return self.df

    def _parse_columns(self):
        self.df["StartPos"] = self.df["StartPos"].apply(ast.literal_eval)
        self.df["ObjectifPos"] = self.df["ObjectifPos"].apply(ast.literal_eval)
        self.df["JumpsPos"] = self.df["JumpsPos"].apply(ast.literal_eval)

class Plotter:
    def __init__(self, root, dataframe: pd.DataFrame, back_to_menu_callback):
        self.df = dataframe
        self.root = root
        self.back_to_menu_callback = back_to_menu_callback  # Callback pour revenir au menu
        self.root.title("Jeu de Plateforme - Graphiques")

        # Création du notebook (onglets)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=1, fill='both')

        # Création des onglets et affichage des graphiques
        self.plot_time_per_attempt()
        self.plot_success_rate()
        self.plot_actions_per_attempt()
        self.plot_jump_paths()

        # Ajouter le bouton pour revenir au menu principal
        self.back_button = tk.Button(self.root, text="Retour au Menu", command=self.back_to_menu)
        self.back_button.pack(pady=10)

    def display_figure(self, fig, tab_name):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=tab_name)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill='both')

    def plot_time_per_attempt(self):
        fig = Figure(figsize=(5, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(self.df["Temps"], marker='o', linestyle='-', color='blue')
        ax.set_title("Temps par essai")
        ax.set_xlabel("Essai")
        ax.set_ylabel("Temps (secondes)")
        ax.grid(True)
        self.display_figure(fig, "Temps par essai")

    def plot_success_rate(self):
        win_counts = self.df["Win"].value_counts()
        labels = ["Succès", "Échec"]
        colors = ["green", "red"]

        fig = Figure(figsize=(4, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.pie(win_counts, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        ax.set_title("Taux de réussite")
        ax.axis('equal')
        self.display_figure(fig, "Taux de réussite")

    def plot_actions_per_attempt(self):
        fig = Figure(figsize=(5, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(range(len(self.df)), self.df["ActNb"], color='orange')
        ax.set_title("Nombre d'actions par essai")
        ax.set_xlabel("Essai")
        ax.set_ylabel("Nombre d'actions")
        ax.grid(axis='y')
        self.display_figure(fig, "Actions par essai")

    def plot_jump_paths(self):
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)

        for i, jumps in enumerate(self.df["JumpsPos"]):
            xs = [pos[0] for pos in jumps]
            ys = [pos[1] for pos in jumps]
            color = 'green' if self.df["Win"][i] else 'red'
            ax.plot(xs, ys, marker='o', label=f'Essai {i} {"GOOD" if self.df["Win"][i] else "BAD"}',
                    alpha=0.6, color=color)

        ax.set_title("Trajectoires des sauts")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.invert_yaxis()
        ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1.0))
        ax.grid(True)
        self.display_figure(fig, "Trajectoires des sauts")

    def back_to_menu(self):
        self.back_to_menu_callback()  # Appelle le callback pour revenir au menu
