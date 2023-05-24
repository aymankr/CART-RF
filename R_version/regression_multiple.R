library(rpart)
library(rpart.plot)
library(MASS)
library(caret)
data <- read.csv2("datasport.csv")
data <- subset(data, select = -sport)
# Analyse descriptive des variables numériques
summary(data)
# 1 variables quali, le reste quanti
# Diviser le dataset en ensembles d'entraînement et de test
set.seed(123)
trainIndex <- createDataPartition(data$rcc, p = 0.8, list = FALSE)
trainData <- data[trainIndex, ] #données d'entraînement = 80%
testData <- data[-trainIndex, ] #données de test = 20%
# Créer un modèle de régression linéaire multiple avec stepAIC
linear_model <- lm(rcc ~ ., data = trainData)
step_linear_model <- stepAIC(linear_model, direction = "both")
summary(step_linear_model)
selected_vars <- names(coef(step_linear_model))
cat("Variables sélectionnées dans la régression linéaire multiple:", "\n")
print(selected_vars) #il y 1 variables sélectionnées dans ce modèle
# Créer un modèle d'arbre de régression CART
tree_model <- rpart(rcc ~ ., data = trainData, control = rpart.control(cp = 0.01))
#arbre élagué,
#cp = 0.01 signifie que pour qu'une division supplémentaire ait lieu, elle doit
#améliorer la SSE d'au moins 0,01.
#Si une division potentielle n'améliore pas suffisamment la SSE, l'élagage se produit ->
#éviter le suraprentissage
rpart.plot(tree_model)
printcp(tree_model)
tree_vars <- unique(tree_model$frame$var)
tree_vars <- tree_vars[tree_vars != "<leaf>"] # Supprimez les nœuds feuilles
cat("Variables sélectionnées dans l'arbre de régression CART:", "\n")
print(tree_vars) #seule la variable hc est utilisée pour la construction de l'arbe
# Prédire sur l'ensemble de test
linear_preds <- predict(step_linear_model, testData)
tree_preds <- predict(tree_model, testData)
# Calculer l'erreur quadratique moyenne (MSE) pour chaque modèle
linear_mse <- mean((testData$rcc - linear_preds)^2)
tree_mse <- mean((testData$rcc - tree_preds)^2)
# Afficher les résultats
cat("MSE for linear regression model:", linear_mse, "\n")
cat("MSE for CART tree model:", tree_mse, "\n")
# Prédire sur l'ensemble d'entraînement
linear_train_preds <- predict(step_linear_model, trainData)
tree_train_preds <- predict(tree_model, trainData)
# Calculer l'erreur quadratique moyenne (MSE) pour chaque modèle sur l'ensemble
#d'entraînement
linear_train_mse <- mean((trainData$rcc - linear_train_preds)^2)
tree_train_mse <- mean((trainData$rcc - tree_train_preds)^2)
# Afficher les résultats
cat("MSE for linear regression model on training data:", linear_train_mse, "\n")
cat("MSE for CART tree model on training data:", tree_train_mse, "\n")
# Afficher les résultats
cat("MSE for linear regression model on training data:", linear_train_mse, "\n")
cat("MSE for linear regression model on test data:", linear_mse, "\n")
cat("Difference in MSE for linear regression model:", abs(linear_train_mse -
linear_mse), "\n\n")
cat("MSE for CART tree model on training data:", tree_train_mse, "\n")
cat("MSE for CART tree model on test data:", tree_mse, "\n")
cat("Difference in MSE for CART tree model:", abs(tree_train_mse - tree_mse), "\n")
#différence plus importante entre les MSE d'entraînement et de test pour l'arbre de
#régression CART que pour la régression linéaire multiple.
#Cela pourrait indiquer un surapprentissage pour l'arbre de régression CART. Toutefois,
#la différence n'est pas très grande,
#il est donc peu probable que cela soit un problème majeur.
# Charger les bibliothèques nécessaires
library(ggplot2)
# Créer un dataframe pour stocker les prédictions et les valeurs réelles
predictions <- data.frame(
TrueValue = testData$rcc,
LinearPrediction = linear_preds,
TreePrediction = tree_preds
) 
#Créer un graphique de dispersion pour la régression linéaire multiple
plot(testData$rcc, linear_preds,
main = "Linear Regression Predictions vs True Values",
xlab = "True Value",
ylab = "Predicted Value",
col = "blue")
abline(0, 1, col = "red", lty = 2)
# Créer un graphique de dispersion pour les arbres de régression CART
plot(testData$rcc, tree_preds,
main = "CART Tree Predictions vs True Values",
xlab = "True Value",
ylab = "Predicted Value",
col = "blue")
abline(0, 1, col = "red", lty = 2)
#la regression linéaire multiple est la meilleure méthode dans ce cas-là (on le remarque
#grace au MSE, et graphiquement)