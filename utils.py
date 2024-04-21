'''from openai import OpenAI
import logging
import os

client = OpenAI(
    api_key="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"
)

async def generate_text(prompt) -> dict:
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'], response['usage']['total_tokens']
    except Exception as e:
        logging.error(e)'''

import logging
import datetime
import db

from openai import OpenAI

history = {}

client = OpenAI(
    api_key="API_KEY",
    base_url="https://api.proxyapi.ru/openai/v1",
)

async def CheckResetTokens():
    for reg_time in await db.GetRegistrationTime():
        current_time = datetime.datetime.now()
        specified_time = datetime.datetime.strptime(reg_time, '%Y-%m-%d %H:%M:%S')

        time_diff = current_time - specified_time

        if time_diff >= datetime.timedelta(days=1):
            await db.UpdateTokensWithRegDate(specified_time, await db.GetTokensWithRegDate(specified_time) + 500)
            await db.UpdateDataWithRegDate(specified_time, "ResetTokens", 7)
            await db.UpdateTextDataWithRegDate(specified_time, "RegDate", current_time)
        else:
            await db.UpdateDataWithRegDate(specified_time, "ResetTokens", await db.GetResetTokensTimeWithRegDate(specified_time)-1)

async def generate_text(prompt, uid, model) -> dict:
    
    new_messages = [{"role": "user", "content": prompt}]

    if len(history[uid]) != 0:
        new_messages.insert(0, history[uid][0])
        new_messages.insert(0, history[uid][1])

    try:
        response = client.chat.completions.create(
            model=model,
            messages=new_messages
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(e)

async def reset_context(uid):
    history[uid].clear()

async def check_subscribe(chat_member):
    if chat_member['status'] != 'left':
        return True
    else:
        return False
