# Charger les packages
library(rpart)
library(rpart.plot)
library(randomForest)
# Charger le jeu de données
data <- read.csv2('datasport.csv')
data <- data[, -13]
# Diviser les données en ensembles d'entraînement et de test
set.seed(123)
trainIndex <- sample(1:nrow(data), 0.8 * nrow(data))
trainData <- data[trainIndex, ]
testData <- data[-trainIndex, ]
# Arbre de régression CART optimal (élagué)
cart_model <- rpart(rcc ~ ., data = trainData, method = "anova", control =
rpart.control(minsplit=5,cp = 0))
cart_optimal <- prune(cart_model, cp =
cart_model$cptable[which.min(cart_model$cptable[,"xerror"]),"CP"])
# Visualiser l'arbre élagué
rpart.plot(cart_optimal)
# Bagging
set.seed(123)
bagging_model <- randomForest(rcc ~ ., data = trainData, ntree = 500, mtry =
ncol(trainData), importance = TRUE)
# Forêt aléatoire
set.seed(123)
tuned.mtry <- tuneRF(trainData[,-1], trainData$rcc, mtryStart = 1, ntreeTry = 500,
stepFactor = 3, improve = 0)
mtry <- tuned.mtry[which.min(tuned.mtry[,"OOBError"]), "mtry"]
set.seed(123)
rf_model <- randomForest(rcc ~ ., data = trainData, ntree = 500, mtry = mtry, importance
= TRUE)
# Calculer l'erreur OOB pour chaque méthode
cart_test_error <- sum((predict(cart_optimal, testData) - testData$rcc)^2) /
nrow(testData)
bagging_oob <- bagging_model$mse[500]
rf_oob <- rf_model$mse[500]
# Comparer les erreurs OOB
cat("Erreur sur les données de test pour CART optimal :", cart_test_error,
"\nErreur OOB Bagging :", bagging_oob,
"\nErreur OOB Forêt aléatoire :", rf_oob)
# Importance des variables
varImpPlot(bagging_model)
varImpPlot(rf_model)