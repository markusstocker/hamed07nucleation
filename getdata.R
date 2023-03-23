library(orkg)
library(ggplot2)

orkg <- ORKG(host='https://sandbox.orkg.org/')

df <- orkg$resources$by_id('R275316')$as_dataframe()

names(df) <- make.names(names(df))
df$Event.Duration..min. <- as.numeric(df$Event.Duration..min.)
df$Season <- as.factor(df$Season)

ggplot(df, aes(x=Season, y=Event.Duration..min.)) +
  geom_boxplot() +
  geom_jitter(colour = 2, width = 0.2) +
  xlab('Season') + 
  ylab('Event duration [min]')


