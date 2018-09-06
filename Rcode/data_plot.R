library(tseries)
library(ggthemes)
library(ggplot2)

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
par(mfrow = c(3,2))
plot(JD_return)
plot(BABA_return)
plot(JD_cov1)
plot(BABA_cov1)
plot(JD_cov2)
plot(BABA_cov2)


qplot(JD_return)



data <- data.frame(date = date,  JD_return = Y[["JDStock"]], 
                   BABA_return = Y[["BABAStock"]], 
                   JD_cov1 = X[["Covarites"]][,1], 
                   JD_cov2 = X[["Covarites"]][,2], 
                   BABA_cov1 = X[["Covarites"]][,3], 
                   BABA_cov2 = X[["Covarites"]][,4])

p <- ggplot(data, aes(x = date) + 
              geom_point(aes(y = JD_return)) + 
              geom_line(aes(y = JD_return, color = "blue")))


p <- ggplot(data, aes(x = date, y = JD_return))+ 
  geom_point()+
  geom_line()




ggplot(data, aes(x = date))+
  geom_line(aes(y = JD_return), color = "cyan")

ggplot(data, aes(x = date))+
  geom_line(aes(y = BABA_return), color = "blue") 









