import asyncio
import os
import gradio as gr
from loguru import logger
from revChatGPT.Official import AsyncChatbot
from dotenv import load_dotenv

def launch(meta:dict):
    demo = gr.Interface(fn=handle_response,
        inputs=gr.Textbox(lines=5, placeholder="ChatGPT proxy server, ask your questions here..."), 
        outputs=gr.Textbox(lines=5)
    )

    host = "0.0.0.0"
    port = 8082

    share = meta.get("share")
    username = meta.get("username")
    password = meta.get("password")
    if (not username) or (not password):
        demo.launch(server_name=host, server_port=port, share=share)
    else:
        # https://discuss.huggingface.co/t/gradio-authentication-not-working-in-spaces/25629
        demo.launch(server_name=host, server_port=port, share=share, auth=(username, password))

async def handle_response(message) -> str:
    logger.info(message)
    response = await chatbot.ask(message)
    try:
        responseMessage = response["choices"][0]["text"]
    except Exception as e:
        logger.error(e)
        return "Server Error"
        
    return responseMessage

async def test():
    rsp = await handle_response("Hi")
    print(rsp)

async def run():
    meta = {
        "share": False if os.getenv("SHARE") == 0 else True,
        "username": os.getenv("USERNAME"),
        "password": os.getenv("PASSWORD"),
    }
    logger.info('starting...')
    launch(meta)

if __name__ == "__main__":
    logger.add("app.log", rotation="10 MB", retention="365 days")

    load_dotenv()
    key = os.getenv("OPENAI_KEY")
    if (not key) or (not key.startswith("sk-")):
        logger.error("invalid openai key, please check ...")
    
    # FIXME: text-davinci-003 is a paid model, it will cost fees
    model = os.getenv("MODEL", "text-davinci-003")        
    chatbot = AsyncChatbot(api_key=key, engine=model)

    asyncio.run(run())