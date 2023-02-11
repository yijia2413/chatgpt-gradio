import asyncio
import os
from revChatGPT.Official import AsyncChatbot
from dotenv import load_dotenv
import gradio as gr
from log import setup_logger

def launch(meta:dict):
    demo = gr.Interface(fn=handle_response,
        inputs=gr.Textbox(lines=5, placeholder="ChatGPT proxy server, ask your questions here..."), 
        outputs=gr.Textbox(lines=5)
    )

    host = '0.0.0.0'
    port = 8082

    share = meta.get('share')
    username = meta.get('username')
    password = meta.get('password')
    print(meta)
    if (not username) or (not password):
        demo.launch(server_name=host, server_port=port, share=share)
    else:
        demo.launch(server_name=host, server_port=port, share=share, auth=(username, password))

async def handle_response(message) -> str:
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
        'share': False if os.getenv("SHARE") == 0 else True,
        'username': os.getenv("USERNAME"),
        'password': os.getenv("PASSWORD"),
    }
    launch(meta)

if __name__ == '__main__':
    logger = setup_logger(__name__)

    load_dotenv()
    key = os.getenv("OPENAI_KEY")
    if (not key) or (not key.startswith('sk-')):
        logger.error("invalid openai key, please check ...")
    
    # FIXME: now openai default model works again (2023-02-11), if not work, please change
    model = os.getenv("MODEL", "text-davinci-003")        
    chatbot = AsyncChatbot(api_key=key, engine=model)

    asyncio.run(run())