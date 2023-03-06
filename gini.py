import pandas as pd
import graphviz


class Gini():
    def __init__(self, file) -> None:
        self.df = pd.read_csv(file)
        self.df = pd.DataFrame(self.df)
        self.tree = [] # liste qui contient les seuils optimaux, avec leur gini et variable
        self.main()

    def division(self, df):
        # stocker les valeurs des indices de Gini, leurs seuils et variables correspondantes
        tab_gini = pd.DataFrame(columns=['variable', 'seuil', 'gini'])

        # calcul de Dk
        p1 = df['Y'].value_counts().A  # nombre de modalités A dans ce noeud
        p2 = df['Y'].value_counts().B
        n = p1 + p2  # nombre d'individus
        Dk = 1 - ((p1/n)**2 + (p2/n)**2)  # indice de Gini avant séparation

        # parcourir chaque variable X1, X2...
        i = 0
        for x in df.columns[1:]:
            # parcourir chaque valeur de cette variable comme seuil
            for seuil in df[x]:
                # liste des modalités du noeud de gauche respectant le seuil
                noeud_gauche = df[df[x] <= seuil].Y
                noeud_droite = df[df[x] > seuil].Y

                # calculer l'indice de gini seulement lorsque le noeud n'est pas totalement pur (contient des modalités différentes)
                Dkg, Dkd = 0, 0
                if 'A' in noeud_gauche.tolist() and 'B' in noeud_gauche.tolist():
                    p1g = noeud_gauche.value_counts().A
                    p2g = noeud_gauche.value_counts().B
                    ng = p1g + p2g
                    Dkg = (1 - ((p1g/ng)**2 + (p2g/ng)**2)) * \
                        (ng/n)  # indice de Gini de ce noeud

                if 'A' in noeud_droite.tolist() and 'B' in noeud_droite.tolist():
                    p1d = noeud_droite.value_counts().A
                    p2d = noeud_droite.value_counts().B
                    nd = p1d + p2d
                    Dkd = (1 - ((p1d/nd)**2 + (p2d/nd)**2)) * (nd/n)

                gini = Dk - (Dkg + Dkd)  # indice de Gini global
                tab_gini.loc[i] = [x, seuil, gini]  # ajout des informations
                i += 1

        tab_gini.sort_values(by="gini", ascending=False, inplace=True)
        tab_gini.reset_index(drop=True, inplace=True)
        return tab_gini.iloc[0]

    def recursion(self, df, level=0):
        result = self.division(df) # recuperer le meilleur seuil pour ces données
        self.tree.append([level, result['variable'],
                         result['seuil'], result['gini']]) # ajouter informations du seuil dans l'arbre
        df_gauche = df[df[result['variable']] <= result['seuil']] # séparer les données selon le seuil
        df_droite = df[df[result['variable']] > result['seuil']]
        if 'A' in df_gauche.Y.tolist() and 'B' in df_gauche.Y.tolist():
            self.recursion(df_gauche, level + 1) # séparer les données récursivement
        if 'A' in df_droite.Y.tolist() and 'B' in df_droite.Y.tolist():
            self.recursion(df_droite, level + 1)

    def display(self):
        """
            tentative d'affichage de l'arbre ;)
        """
        dot = graphviz.Digraph(comment='Arbre de décision', graph_attr={'size': '10,10!'})
        for noeud in self.tree:
            level, variable, seuil, gini = noeud
            dot.node(f"{variable} {seuil} ({gini:.2f})",
                     label=f"({gini:.2f})", shape="oval")
            if level > 0:
                parent = self.tree[level - 1]
                parent_variable, parent_seuil, _ = parent[1:]
                signe = f"<={parent_variable} {parent_seuil}" if parent_variable == variable else f">{parent_variable} {parent_seuil}"
                dot.edge(
                    f"{parent_variable} {parent_seuil} ({parent[3]:.2f})", f"{variable} {seuil} ({gini:.2f})", label=signe)
        dot.render("arbre_decision", view=True, format="png")

    def main(self):
        self.recursion(self.df)
        self.display() # afficher l'arbre avec graphviz
        print(self.tree)

if __name__ == "__main__":
    Gini('data.csv')
