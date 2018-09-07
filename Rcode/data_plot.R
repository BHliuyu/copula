setwd("~/copula")
library(tseries)
library(ggthemes)
library(ggplot2)
library(xts)

# load date data from 2017-05-23 to 2018-08-17
# Because the function 'xts' require specific format :'%Y-%m-%d'

old_date <- read.csv('Rdata/date.csv')
date <- as.character(old_date$X0)

# load JD and BABA stock data
load('Rdata/JD_BABAstock.Rdata')
JD_return <- xts(Y[["JDStock"]], as.Date(date)) # 100 * ln(P{t} - p{t-1})
BABA_return <- xts(Y[["BABAStock"]], as.Date(date)) # 100 * ln(P{t} - p{t-1})
JD_cov1 <- xts(X[["Covarites"]][,1], as.Date(date)) 
JD_cov2 <- xts(X[["Covarites"]][,2], as.Date(date))
BABA_cov1 <- xts(X[["Covarites"]][,3], as.Date(date))
BABA_cov2 <- xts(X[["Covarites"]][,4], as.Date(date))

# load JD and BABA emotion score
JD_score <- read.csv('csv/JD_score.csv')
BABA_score <- read.csv('csv/BABA_score.csv')

score_JD <- xts(JD_score, as.Date(date))
score_BABA <- xts(BABA_score, as.Date(date))

par(mfrow = c(4,2))
plot(JD_return)
plot(BABA_return)
plot(JD_cov1)
plot(BABA_cov1)
plot(JD_cov2)
plot(BABA_cov2)
plot(score_JD)
plot(score_BABA)











