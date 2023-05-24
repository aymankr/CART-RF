# Charger les bibliothèques nécessaires
library(rpart)
library(rpart.plot)

# Charger les données
data <- read.csv("data.csv")

# Convertir la colonne Y en facteur
data$Y <- as.factor(data$Y)

# Construire l'arbre de décision avec la méthode rpart
arbre_decision_rpart <- rpart(Y ~ X1 + X2, data=data, method="class", parms=list(split="gini"), control=rpart.control(minsplit=1, cp=0.01))

# Afficher l'arbre de décision étape par étape
rpart.plot(arbre_decision_rpart, type=4, extra=101, fallen.leaves=FALSE, under=TRUE)
