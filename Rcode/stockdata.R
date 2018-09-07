setwd("/Users/liuyu/copula")
library(zoo)
library(xts)
library(quantmod)
library(umap)

# Now, we get the news data without the days that the stock market is closed
# The length of news data is 312

# get news date, but this date from 2018-08-17 to 2017-05-23
# We want get the date from 2017-05-23 to 2018-08-17, so we need to reverse the date

news <- read.csv('csv/BABA0523-0817 final.csv')
date <- news$date

#################
### BABA stock ##
#################
getSymbols("BABA", src = "yahoo", from = "2017-04-25", to = "2018-8-17")
High<-as.numeric(BABA[,2])
Low<-as.numeric(BABA[,3])
Price<-as.numeric(BABA[,4])
## Data Matrix for Stock Returns Modelling
CovStock<-matrix(rep(1,332*7),ncol=7)
colnames(CovStock)<-c("ReturnY","RMA1","RMA5","RMA20 ","CloseAbs95","CloseSqrt95","MaxMin95")

## Return
for(t in 2:length(Price)){
  CovStock[t,1]<-100*log(Price[t]/Price[t-1])
}
CovStock[1,1][1]<-0
ReturnY<-CovStock[,1]

## Last Day's Return
CovStock[,2]<-c(0,ReturnY[-332])

## Last Week's Return
for(t in 6:332){
  CovStock[t,3]<-sum(ReturnY[(t-5):(t-1)])/5
}

## Last Month's Return
for(t in 21:332){
  CovStock[t,4]<-sum(ReturnY[(t-20):(t-1)])/20
}

rou<-0.95
## CloseAbs95
for(t in 4:332){
  n<-t-4
  CovStock[t,5]<-(1-rou)*sum(sapply(0:n,function(n) rou^n*abs(ReturnY[(t-2)-n])))
}

## CloseSqrt95
CloseSqrt95<-rep(0,length(Price))
for(t in 4:332){
  n<-t-4
  CovStock[t,6]<-sqrt((1-rou)*sum(sapply(0:n,function(n) rou^n*((ReturnY[(t-2)-n])^2))))
}

## Maxmin95
for(t in 3:332){
  n<-t-3
  CovStock[t,7]<-(1-rou)*sum(sapply(0:n,function(n) rou^n*(100*(log(High[(t-1)-n])-log(Low[(t-1)-n])))))
}

## CovStock332 matrix 252*7
BABA_Stock<-CovStock[-(1:20),]
rownames(BABA_Stock) <- rev(date)

#################
### JD stock ####
#################

getSymbols("JD", src = "yahoo", from = "2017-04-25", to = "2018-8-17")

High<-as.numeric(JD[,2])
Low<-as.numeric(JD[,3])
Price<-as.numeric(JD[,4])
## Data Matrix for Stock Returns Modelling
CovStock<-matrix(rep(1,332*7),ncol=7)
colnames(CovStock)<-c("ReturnY","RMA1","RMA5","RMA20 ","CloseAbs95","CloseSqrt95","MaxMin95")

## Return
for(t in 2:length(Price)){
  CovStock[t,1]<-100*log(Price[t]/Price[t-1])
}
CovStock[1,1][1]<-0
ReturnY<-CovStock[,1]

## Last Day's Return
CovStock[,2]<-c(0,ReturnY[-332])

## Last Week's Return
for(t in 6:332){
  CovStock[t,3]<-sum(ReturnY[(t-5):(t-1)])/5
}

## Last Month's Return
for(t in 21:332){
  CovStock[t,4]<-sum(ReturnY[(t-20):(t-1)])/20
}

rou<-0.95
## CloseAbs95
for(t in 4:332){
  n<-t-4
  CovStock[t,5]<-(1-rou)*sum(sapply(0:n,function(n) rou^n*abs(ReturnY[(t-2)-n])))
}

## CloseSqrt95
CloseSqrt95<-rep(0,length(Price))
for(t in 4:332){
  n<-t-4
  CovStock[t,6]<-sqrt((1-rou)*sum(sapply(0:n,function(n) rou^n*((ReturnY[(t-2)-n])^2))))
}

## Maxmin95
for(t in 3:332){
  n<-t-3
  CovStock[t,7]<-(1-rou)*sum(sapply(0:n,function(n) rou^n*(100*(log(High[(t-1)-n])-log(Low[(t-1)-n])))))
}

## CovStock332 matrix 252*7
JD_Stock<-CovStock[-(1:20),]
rownames(JD_Stock) <- rev(date)


###############
## Covariate###
###############
BABA_array <- read.csv('csv/BABA_array.csv')
BABA.umap <- umap(BABA_array)
BABA_covariate <- BABA.umap$layout
colnames(BABA_covariate) <- c('BABA_covariate1', 'BABA_covariate2')
rownames(BABA_covariate) <- rev(date)

JD_array <- read.csv('csv/JD_array.csv')
JD.umap <- umap(JD_array)
JD_covariate <- JD.umap$layout
colnames(JD_covariate) <- c('JD_covariate1', 'JD_covariate2')
rownames(JD_covariate) <- rev(date)

covarite <- as.matrix(cbind(JD_covariate, BABA_covariate))

X <- list(JD_Stock[, -1],
          BABA_Stock[, -1], 
          covarite)

names(X) <- list('JDStock', 'BABAStock', 'Covarites')

Y <- list(as.matrix(JD_Stock[, 1]),
          as.matrix(BABA_Stock[, 1]))
names(Y) <- list('JDStock', 'BABAStock')



JD_mean_RMA1 <- mean(X[["JDStock"]][,1])
JD_mean_RMA5 <- mean(X[["JDStock"]][,2])
JD_mean_RMA20 <- mean(X[["JDStock"]][,3])
JD_mean_CloseAbs95 <- mean(X[["JDStock"]][,4])
JD_mean_CloseSqrt95 <- mean(X[["JDStock"]][,6])
JD_mean_MaxMin95 <- mean(X[["JDStock"]][,5])
JD_mean <- list(JD_mean_RMA1, JD_mean_RMA5, JD_mean_RMA20,
             JD_mean_CloseAbs95, JD_mean_CloseSqrt95, JD_mean_MaxMin95)
names(JD_mean) <- c('RMA1', 'RMA5', 'RMA20',
                    'CloseAbs95', 'CloseSqrt95', 'MaxMin95')

JD_sd_RMA1 <- var(X[["JDStock"]][,1])
JD_sd_RMA5 <- var(X[["JDStock"]][,2])
JD_sd_RMA20 <- var(X[["JDStock"]][,3])
JD_sd_CloseAbs95 <- var(X[["JDStock"]][,4])
JD_sd_CloseSqrt95 <- var(X[["JDStock"]][,6])
JD_sd_MaxMin95 <- var(X[["JDStock"]][,5])

JD_sd <- list(JD_sd_RMA1, JD_sd_RMA5, JD_sd_RMA20,
                JD_sd_CloseAbs95, JD_sd_CloseSqrt95, JD_sd_MaxMin95)
names(JD_sd) <- c('RMA1', 'RMA5', 'RMA20',
                    'CloseAbs95', 'CloseSqrt95', 'MaxMin95')

JDstock.config <- list(JD_mean, JD_sd)
names(JDstock.config) <- c('JD_mean', 'JD_sd')



BABA_mean_RMA1 <- mean(X[["BABAStock"]][,1])
BABA_mean_RMA5 <- mean(X[["BABAStock"]][,2])
BABA_mean_RMA20 <- mean(X[["BABAStock"]][,3])
BABA_mean_CloseAbs95 <- mean(X[["BABAStock"]][,4])
BABA_mean_CloseSqrt95 <- mean(X[["BABAStock"]][,6])
BABA_mean_MaxMin95 <- mean(X[["BABAStock"]][,5])
BABA_mean <- list(JD_mean_RMA1, JD_mean_RMA5, JD_mean_RMA20,
                JD_mean_CloseAbs95, JD_mean_CloseSqrt95, JD_mean_MaxMin95)
names(BABA_mean) <- c('RMA1', 'RMA5', 'RMA20',
                    'CloseAbs95', 'CloseSqrt95', 'MaxMin95')


BABA_sd_RMA1 <- var(X[["BABAStock"]][,1])
BABA_sd_RMA5 <- var(X[["BABAStock"]][,2])
BABA_sd_RMA20 <- var(X[["BABAStock"]][,3])
BABA_sd_CloseAbs95 <- var(X[["BABAStock"]][,4])
BABA_sd_CloseSqrt95 <- var(X[["BABAStock"]][,6])
BABA_sd_MaxMin95 <- var(X[["BABAStock"]][,5])

BABA_sd <- list(BABA_sd_RMA1, BABA_sd_RMA5, BABA_sd_RMA20,
                BABA_sd_CloseAbs95, BABA_sd_CloseSqrt95, BABA_sd_MaxMin95)
names(BABA_sd) <- c('RMA1', 'RMA5', 'RMA20',
                  'CloseAbs95', 'CloseSqrt95', 'MaxMin95')

BABAstock.config <- list(BABA_mean, BABA_sd)
names(BABAstock.config) <- c('BABA_mean', 'BABA_sd')

X.config <- list(JDstock.config, BABAstock.config)
names(X.config) <- c('JDStock', 'BABAStock')



JDStock_mean <- mean(Y[["JDStock"]])
JDStock_sd <- var(Y[["JDStock"]])
JDStock_method <- 'norm-0-1'

JD_Y <- list(JDStock_mean, JDStock_sd, JDStock_method)
names(JD_Y) <- c('mean', 'sd', 'method')


BABAStock_mean <- mean(Y[["BABAStock"]])
BABAStock_sd <- var(Y[["BABAStock"]])
BABAStock_method <- 'norm-0-1'

BABA_Y <- list(BABAStock_mean, BABAStock_sd, BABAStock_method)
names(BABA_Y) <- c('mean', 'sd', 'method')

Y.config <- list(JD_Y, BABA_Y)
names(Y.config) <- c('JDStock', 'BABAStock')



save(X, X.config, Y, Y.config, file = 'JD_BABAstock.Rdata')
