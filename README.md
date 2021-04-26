# Vocabulary bot

## This project helps to learn new worlds using telegram.

For datastore it is used simple yaml file in the data folder (in future will move into db and will add the possibility to add new words without yaml file)

For using it you have to have TelegramAPI Token (You can request it in https://t.me/botfather) and pass it into container.


## Requirements

> Docker  
> Make  
## The command for building and running:
> make build  
> make run token='Your token'  
 
## Bot supports next commands:
> /help - for output all supported commands  

> all - to display a number of all blocks  

> any number (f.e. 4) - to display the block of words with translation.  

>  /game - for checking words, you can choose a block of words by number, then bot will show you only english words, you can check yourself and ask bot to show translation. 

> /tenses to get the tenses rules, you can choose tense, bot will send you examples with this tense.  
