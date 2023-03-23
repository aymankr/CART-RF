library(rpart)# Pour l’arbre de décision
library(rpart.plot) # Pour la représentation de l’arbre de décision

#Chargement des données
data = read.csv2("data_bigbig.csv", sep = ",")
#Description des données
summary(data)
data$X2 = as.numeric(data$X2)
data

#Construction de l’arbre
data.Tree <- rpart(Y~.,data=data,method= "class", control=rpart.control(minsplit=1,cp=0))
plot(data.Tree, uniform=TRUE, branch=0.5, margin=0.1)
text(data.Tree, all=TRUE, use.n=TRUE)

#On cherche à minimiser l’erreur pour définir le niveau d’élagage
plotcp(data.Tree)

#Affichage du cp optimal
print(data.Tree$cptable[which.min(data.Tree$cptable[,4]),1])

#Elagage de l’arbre avec le cp optimal
data.Tree_Opt <- prune(data.Tree,cp=data.Tree$cptable[which.min(data.Tree$cptable[,4]),1])
prp(data.Tree_Opt,extra=1)
