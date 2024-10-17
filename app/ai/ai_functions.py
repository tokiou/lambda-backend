from dotenv import load_dotenv
from typing import List
import openai
from fastapi import HTTPException
import os

load_dotenv("/lambda-backend/.lambda_env")
openai.api_type = os.getenv('OPENAI-API-TYPE')
openai.api_base = os.getenv('OPENAI-API-BASE')
openai.api_key = os.getenv('OPENAI-API-KEY')
openai.api_version = os.getenv('OPENAI-API-VERSION')
OPENAI_DEPLOYMENT_NAME_GPT_4 = os.getenv('OPENAI-API-DEPLOYMENT')


async def generate_creative_projects(ideas: List[str]) -> str:
    try:
        response = openai.ChatCompletion.create(
            engine=OPENAI_DEPLOYMENT_NAME_GPT_4,
            messages=[{"role": "system", "content": f"""Utilizando estas ideas:
                        {ideas}, genera un proyecto
                        menciona las ventajas, y las desventajas."""}]
        )
        creative_project = response['choices'][0]["message"].get("content", "")
        return creative_project
    except Exception as e:
        raise HTTPException(
            status_code=404, detail=f"{str(e)}"
        )
