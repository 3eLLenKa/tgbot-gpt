import sqlite3
import datetime

connection = sqlite3.connect('telebot.db')
cursor = connection.cursor()

async def registration(user_id):

    user = cursor.execute(f"SELECT TgId FROM Users WHERE TgId = {user_id}").fetchone()

    if user is None:
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO Users (TgId, RegDate) VALUES (?, ?)", (user_id, current_datetime))
        connection.commit()

async def GetResetTokensTimeWithRegDate(date):
    resetTokensTime = cursor.execute(f"SELECT ResetTokens FROM Users WHERE RegDate = '{date}'").fetchone()[0]
    return resetTokensTime

async def GetResetTokensTime(user_id):
    resetTokensTime = cursor.execute(f"SELECT ResetTokens FROM Users WHERE TgId = {user_id}").fetchone()[0]
    return resetTokensTime

async def GetTokensWithRegDate(date):
    tokens = cursor.execute(f"SELECT Tokens FROM Users WHERE RegDate = '{date}'").fetchone()[0]
    return tokens

async def GetTokens(user_id):
    tokens = cursor.execute(f"SELECT Tokens FROM Users WHERE TgId = {user_id}").fetchone()[0]
    return tokens

async def GetBalance(user_id):
    balance = cursor.execute(f"SELECT Balance FROM Users WHERE TgId = {user_id}").fetchone()[0]
    return balance

async def GetModel(user_id):
    model = cursor.execute(f"SELECT Model FROM Users WHERE TgId = {user_id}").fetchone()[0]
    return model

async def GetAdmin(user_id):
    admin = cursor.execute(f"SELECT Admin FROM Users WHERE TgId = {user_id}").fetchone()[0]
    return admin

async def GetSubscribe(user_id):
    subscribe = cursor.execute(f"SELECT Subscribe FROM Users WHERE TgId = {user_id}").fetchone()[0]
    return subscribe

async def GetQuestionsCount(user_id):
    questionsCount = cursor.execute(f"SELECT QuestionsCount FROM Users WHERE TgId = {user_id}").fetchone()[0]
    return questionsCount

async def GetRegistrationTime():
    regTime = list(cursor.execute(f"SELECT RegDate FROM Users").fetchone())
    return regTime

async def UpdateData(user_id, column, data):
    cursor.execute(f"UPDATE Users SET {column} = {data} WHERE TgId = {user_id}")
    connection.commit()

async def UpdateTextData(user_id, column, data):
    cursor.execute(f"UPDATE Users SET {column} = '{data}' WHERE TgId = {user_id}")
    connection.commit()

async def UpdateTokensWithRegDate(reg_date, data):
    cursor.execute(f"UPDATE Users SET Tokens = {data} WHERE RegDate = '{reg_date}'")
    connection.commit()

async def UpdateDataWithRegDate(date, column, data):
    cursor.execute(f"UPDATE Users SET {column} = {data} WHERE RegDate = '{date}'")
    connection.commit()

async def UpdateTextDataWithRegDate(date, column, data):
    cursor.execute(f"UPDATE Users SET {column} = '{data}' WHERE RegDate = '{date}'")
    connection.commit()