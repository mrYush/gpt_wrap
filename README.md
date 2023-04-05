# gpt_wrap
## describe
Telegram wrapper to use GPT models.

To launch code you need telegram token and openai token
- How to get telegram token: https://core.telegram.org/api
- How to get openai token: https://platform.openai.com/docs/api-reference

## set enviroment
```
poetry shell
poetry install
```

## configurate
Fill config file
```
cp config.yaml.example config.yaml
vim config.yaml
```
be sure that you fill all parameters in config correctly


## launch
And launch bot
```
python src/main.py
```
