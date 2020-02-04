# -*- coding: utf8 -*-
from __future__ import print_function

import os.path
import pickle

import discord
from discord.ext import commands
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
SPREADSHEET_ID = ''
RANGE_NAME = ''

# init Google Spreadsheets API

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

# init Discord bot API
with open('bottoken.txt', 'r') as tokenfile:
    btoken = tokenfile.read()
bot = commands.Bot(command_prefix='>')

bot.run(btoken)
