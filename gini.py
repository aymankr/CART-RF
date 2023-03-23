
import pandas as pd
import graphviz
import uuid

class Gini():
    def __init__(self, file) -> None:
        self.df = pd.read_csv(file)
        self.df = pd.DataFrame(self.df)
        self.seuils_optimaux = [] # arbre contenant les informations : les seuils optimaux, avec leur gini, la variable, les ID de noeuds correspondant, le niveau dans l'arbre
        self.tree = {} # arbre qui servira pour l'affichage, dictionnaire stockant des noeuds, leurs noeuds fils et les modalités de ces noeuds fils
        self.main()

    def division(self, df):
        def calcul_gini(noeud, total):
            p1, p2 = noeud.value_counts().get('A', 0), noeud.value_counts().get('B', 0)
            n = p1 + p2
            if n == 0:
                return 0
            return (1 - ((p1/n)**2 + (p2/n)**2)) * (n/total)
        
        tab_gini = pd.DataFrame(columns=['variable', 'seuil', 'gini'])
        total = len(df)

        i = 0
        for x in df.columns[1:]:
            for seuil in df[x].unique():
                noeud_gauche = df[df[x] < seuil].Y
                noeud_droite = df[df[x] >= seuil].Y

                gini = calcul_gini(df['Y'], total) - (calcul_gini(noeud_gauche, total) + calcul_gini(noeud_droite, total))
                tab_gini.loc[i] = [x, seuil, gini]
                i += 1

        tab_gini.sort_values(by="gini", ascending=False, inplace=True)
        tab_gini.reset_index(drop=True, inplace=True)
        return tab_gini.iloc[0]


    def recursion(self, df, level=0, parent_noeud_id=None):
        result = self.division(df)  # obtenir la meilleure division pour ce noeud

        noeud_id = len(self.seuils_optimaux)  # générer un ID pour ce noeud
        self.seuils_optimaux.append([level, result['variable'], result['seuil'], result['gini'], noeud_id])

        # récupérer les modalités pour les ensembles gauche et droit
        mg = list(df[df[result['variable']] < result['seuil']].Y)
        md = list(df[df[result['variable']] >= result['seuil']].Y)

        # ajouter le noeud à l'arbre avec ses informations
        self.tree[noeud_id] = {'parent': parent_noeud_id, 'enfant': [], 'mg': mg, 'md': md}

        # si le noeud a un parent, ajouter ce noeud comme enfant gauche ou droit du parent
        if parent_noeud_id is not None:
            # ajouté en tant qu'enfant gauche ou droit de son parent 
            # en fonction de la majorité des éléments qui sont inférieurs ou égaux au seuil du parent
            parent_seuil = self.seuils_optimaux[parent_noeud_id][2]
            parent_variable = self.seuils_optimaux[parent_noeud_id][1]
            direction = 'g' if (df[parent_variable] < parent_seuil).sum() > (df[parent_variable] >= parent_seuil).sum() else 'd'
            self.tree[parent_noeud_id]['enfant'].append((noeud_id, direction))

        # effectuer des appels récursifs pour les ensembles gauche et droit si les modalités sont différentes
        for c in ['g', 'd']:
            if 'A' in self.tree[noeud_id][f'm{c}'] and 'B' in self.tree[noeud_id][f'm{c}']:
                new_df = df[df[result['variable']] < result['seuil']] if c == 'g' else df[df[result['variable']] >= result['seuil']]
                
                if len(new_df) < len(df):
                    self.recursion(new_df, level + 1, noeud_id)


    def display(self):
        dot = graphviz.Digraph(comment='Arbre de décision',
                            graph_attr={'size': '20,20!', 'fontsize': '14'})

        for noeud in self.seuils_optimaux:
            level, variable, seuil, _, noeud_id = noeud
            mg = self.tree[noeud_id]['mg']
            md = self.tree[noeud_id]['md']

            nb_A_gauche, nb_B_gauche = mg.count('A'), mg.count('B')
            nb_A_droite, nb_B_droite = md.count('A'), md.count('B')

            # afficher les enfants decoulant de ce noeud
            if level > 0:
                enfants = []

                if not ('A' in mg and 'B' in mg):
                    enfants.append((mg, f"{variable} < {seuil:.2f}", nb_A_gauche, nb_B_gauche))
                if not ('A' in md and 'B' in md):
                    enfants.append((md, f"{variable} ≥ {seuil:.2f}", nb_A_droite, nb_B_droite))

                for _, label, nb_A, nb_B in enfants:
                    enfant_id = str(uuid.uuid4())
                    dot.node(enfant_id, label=f"A: {nb_A}\nB: {nb_B}", shape="oval")
                    dot.edge(f"{noeud_id}", enfant_id, label=label)

            dot.node(f"{noeud_id}", label=f"A: {nb_A_gauche + nb_A_droite}\nB: {nb_B_gauche + nb_B_droite}", shape="oval")

            # lier ce noeud avec son parent
            if level > 0:
                parent_id = self.tree[noeud_id]['parent']
                parent_noeud = [n for n in self.seuils_optimaux if n[-1] == parent_id][0]
                _, parent_variable, parent_seuil, _, _ = parent_noeud

                enfant_gauche = next((enfant for enfant in self.tree[parent_id]['enfant'] if enfant[0] == noeud_id and enfant[1] == 'g'), None)
                direction = '<' if enfant_gauche is not None else '≥'
                dot.edge(f"{parent_id}", f"{noeud_id}", label=f"{parent_variable} {direction} {parent_seuil:.2f}")


        dot.render("arbre_decision", view=True, format="png")


    def main(self):
        self.recursion(self.df)
        self.display()
        print(self.tree)

if __name__ == "__main__":
    Gini('data_bigbig.csv')
