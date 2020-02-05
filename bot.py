# -*- coding: utf8 -*-
from __future__ import print_function

import os.path
import pickle
import json
import discord
from discord.ext import commands
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


with open('ids.json') as json_file:
    data = json.load(json_file)

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
SPREADSHEET_ID = data['spreadsheetID']
BOT_TOKEN = data['botToken']

# init Google Spreadsheets API
print('Connecting to Google Sheets API...')
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()
print('Connected to Google Sheets API')

# init Discord bot API

print('Connecting to Discord bot API...')
bot = commands.Bot(command_prefix='?')

@bot.event
async def on_ready():
    print(f'Logged in as:\n{bot.user.name}\n{bot.user.id}\n------')

# bot commands
@bot.command()
async def mapwr(ctx, map: str):
    pass

bot.run(BOT_TOKEN)
