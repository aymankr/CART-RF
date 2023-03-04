import pandas as pd

class Gini():
    def __init__(self, file) -> None:
        self.df = pd.read_csv(file)
        self.df = pd.DataFrame(self.df)
        self.main()

    def main(self):
        df = self.df # dataframe
        tab_gini = pd.DataFrame(columns=['variable', 'seuil','gini']) # stocker les valeurs des indices de Gini, leurs seuils et variables correspondantes
        
        # calcul de Dk
        p1 = df['Y'].value_counts().A # nombre de modalités A dans ce noeud
        p2 = df['Y'].value_counts().B
        n = p1 + p2 # nombre d'individus
        Dk = 1 - ((p1/n)**2 + (p2/n)**2) # indice de Gini avant séparation
        
        # parcourir chaque variable X1, X2...
        
        i = 0
        for x in df.columns[1:]:
            # parcourir chaque valeur de cette variable comme seuil
            for seuil in df[x]:
                noeud_gauche = df[df[x] <= seuil].Y # liste des modalités du noeud de gauche respectant le seuil
                noeud_droite = df[df[x] > seuil].Y
                
                # calculer l'indice de gini seulement lorsque le noeud n'est pas totalement pur (contient des modalités différentes)
                if 'A' in noeud_gauche.tolist() and 'B' in noeud_gauche.tolist():
                    p1g = noeud_gauche.value_counts().A 
                    p2g = noeud_gauche.value_counts().B
                    ng = p1g + p2g 
                    Dkg = (1 - ((p1g/ng)**2 + (p2g/ng)**2)) * (ng/n) # indice de Gini de ce noeud
                    
                
                if 'A' in noeud_droite.tolist() and 'B' in noeud_droite.tolist():
                    p1d = noeud_droite.value_counts().A
                    p2d = noeud_droite.value_counts().B
                    nd = p1d + p2d
                    Dkd = (1 - ((p1d/nd)**2 + (p2d/nd)**2)) * (nd/n)
                
                gini = Dk - (Dkg + Dkd) # indice de Gini global
                tab_gini.loc[i] = [x, seuil, gini] # ajout des informations
                i += 1
        
        tab_gini.sort_values(by="gini", ascending=False, inplace = True)
        tab_gini.reset_index(drop=True, inplace=True)
        print(tab_gini)
    
if __name__ == "__main__":
    Gini('data.csv')