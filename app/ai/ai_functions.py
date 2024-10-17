from dotenv import load_dotenv
from typing import List
import openai
from fastapi import HTTPException
from logs.handle_logger import logger
import os

dotenv_path = os.path.join(os.path.dirname(os.path.dirname
                                           (os.path.dirname(__file__))),
                           '.lambda_env')
load_dotenv(dotenv_path)
openai.api_type = os.getenv('OPENAI-API-TYPE')
openai.api_base = os.getenv('OPENAI-API-BASE')
openai.api_key = os.getenv('OPENAI-API-KEY')
openai.api_version = os.getenv('OPENAI-API-VERSION')
OPENAI_DEPLOYMENT_NAME_GPT_4 = os.getenv('OPENAI-API-DEPLOYMENT')


async def generate_creative_projects(ideas: List[str]) -> str:
    try:
        logger.debug("Creating project with the given ideas")
        response = openai.ChatCompletion.create(
            engine=OPENAI_DEPLOYMENT_NAME_GPT_4,
            messages=[{"role": "system", "content": f"""Utilizando estas ideas:
                        {ideas}, genera un proyecto
                        menciona las ventajas, y las desventajas."""}]
        )
        creative_project = response['choices'][0]["message"].get("content", "")
        return creative_project
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=404, detail=f"{str(e)}"
        )
