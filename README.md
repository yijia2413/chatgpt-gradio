# ChatGPT Gradio Proxy

## Features
* Web access ChatGPT 

## Setup
### Docker Install
* Install [Docker](https://docs.docker.com/engine/install/)
* fill in `.env`
    * `USERNAME` and `PASSWORD` is for web auth, default empty
    * [Generate](https://beta.openai.com/account/api-keys) a OpenAI API key for `OPENAI_KEY` 
* run `bash run_docker.sh`

### Local Install
* fill in `.env`
* run `bash run_local.sh`

> then you can access your ChatGPT Web on `http://{your_ip}:8082`

## Have a good chat!
![image](/png/example.png)

## Ref
* [chatGPT-discord-bot](https://github.com/Zero6992/chatGPT-discord-bot)