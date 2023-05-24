import tkinter as tk
import pandas as pd
import numpy as np
from tkinter import filedialog, messagebox
from gini_model import Gini

class Interface:
    """
        Créer une fenêtre Tkinter
    """
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Arbre de Classification - Séparation de Gini")
        self.window.config(bg='white')
        self.gini = None
        self.csv_file = None

        self.instructions = tk.Label(self.window, text="Le fichier CSV doit respecter le format suivant :\n"
                                                        "- Il doit contenir au moins deux colonnes.\n"
                                                        "- La première colonne doit être nommée 'Y' et contenir uniquement les valeurs 'A' et 'B'.\n"
                                                        "- Les autres colonnes doivent contenir uniquement des valeurs numériques.", font=("Arial", 10), bg='white')
        self.instructions.grid(row=0, column=0, columnspan=2)

        self.open_button = tk.Button(self.window, text="Importer le CSV", command=self.open_csv, font=("Arial", 10), bg='lightgray')
        self.open_button.grid(row=1, column=0, sticky='w')

        self.run_button = tk.Button(self.window, text="Lancer", command=self.run, state=tk.DISABLED, font=("Arial", 10), bg='lightgray')
        self.run_button.grid(row=1, column=1, sticky='e')

    """
        Ouvrir une fenêtre de dialogue pour choisir un fichier CSV
    """
    def open_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

        if not file_path:
            return

        df = pd.read_csv(file_path)
        if not self.check_format(df):
            messagebox.showerror("Erreur", "Format invalide")
            return

        self.csv_file = file_path
        self.run_button['state'] = tk.NORMAL

    """
        Vérifier que le fichier a plus d'une colonne, que 
        la première colonne s'appelle 'Y' et contient 
        uniquement les valeurs 'A' et 'B', 
        et que toutes les autres colonnes contiennent uniquement des valeurs numériques.
    """
    def check_format(self, df):
        return (
            len(df.columns) > 1 and 
            df.columns[0] == 'Y' and
            set(df['Y'].unique()) == {'A', 'B'} and
            df.loc[:, df.columns != 'Y'].applymap(np.isreal).all().all()
        )
    
    """
        Lancer l'algorithme de Gini
    """
    def run(self):
        if not self.csv_file:
            return

        self.gini = Gini(self.csv_file)

    def run_app(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = Interface()
    app.run_app()
