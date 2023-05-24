library(rpart)# Pour l’arbre de décision
library(rpart.plot) # Pour la représentation de l’arbre de décision

#Chargement des données
data("ptitanic")
#Description des données
summary(ptitanic)

#Création d’un dataset d’apprentissage et d’un dataset de validation
nb_lignes <- floor((nrow(ptitanic)*0.75)) #Nombre de lignes de l’échantillon d’apprentissage : 75% du dataset
ptitanic <- ptitanic[sample(nrow(ptitanic)), ] #Ajout de numéros de lignes
ptitanic.train <- ptitanic[1:nb_lignes, ] #Echantillon d’apprentissage
ptitanic.test <- ptitanic[(nb_lignes+1):nrow(ptitanic), ] #Echantillon de test

#Construction de l’arbre
ptitanic.Tree <- rpart(survived~.,data=ptitanic.train,method= "class", control=rpart.control(minsplit=5,cp=0))

#Affichage du résultat
plot(ptitanic.Tree, uniform=TRUE, branch=0.5, margin=0.1)
text(ptitanic.Tree, all=FALSE, use.n=TRUE)

#On cherche à minimiser l’erreur pour définir le niveau d’élagage
plotcp(ptitanic.Tree)

#Affichage du cp optimal
print(ptitanic.Tree$cptable[which.min(ptitanic.Tree$cptable[,4]),1])

#Elagage de l’arbre avec le cp optimal
ptitanic.Tree_Opt <- prune(ptitanic.Tree,cp=ptitanic.Tree$cptable[which.min(ptitanic.Tree$cptable[,4]),1])
prp(ptitanic.Tree_Opt,extra=1)


#Prédiction du modèle sur les données de test
ptitanic.test_Predict<-predict(ptitanic.Tree_Opt,newdata=ptitanic.test, type= "class")

#Matrice de confusion
mc<-table(ptitanic.test$survived,ptitanic.test_Predict)
print(mc)

#Erreur de classement
erreur.classement<-1.0-(mc[1,1]+mc[2,2])/sum(mc)
print(erreur.classement)

#Erreur de classement
erreur.classement<-1.0-(mc[1,1]+mc[2,2])/sum(mc)
print(erreur.classement)

#Taux de prédiction
prediction=mc[2,2]/sum(mc[2,])
print(prediction)

#Affichage des règles de construction de l’arbre
print(ptitanic.Tree_Opt)
