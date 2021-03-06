from __future__ import print_function

import json
import os.path
import pickle
from pprint import pprint

import discord
from discord.ext import commands
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

with open('ids.json') as json_file:
    data = json.load(json_file)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets/']
SPREADSHEET_ID = data['spreadsheetID']
BOT_TOKEN = data['botToken']
SPREADSHEETS_CONNECTED = False

# init Google Spreadsheets API
print('Connecting to Google Sheets API...')
creds = None
try:
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', 'https://www.googleapis.com/auth/spreadsheets')
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    SPREADSHEETS_CONNECTED = True
    print('Connected to Google Sheets API')
    
except Exception as e:
    print('Unable to connected to Google Sheets')
    print(f'Error occured: {e}')

# init Discord bot API

print('Connecting to Discord bot API...')
bot = commands.Bot(command_prefix='?')

@bot.event
async def on_ready():
    print(f'Logged in as:\n{bot.user.name}\n{bot.user.id}\n------')

# bot commands

#init bot command for spreadsheet
if SPREADSHEETS_CONNECTED:
    @bot.command()
    async def mapwr(ctx, map: str):
        result = sheet.values().batchGet(spreadsheetId=SPREADSHEET_ID, ranges=['Sheet1!H6:H26','Sheet1!L6:L26']).execute()
        mdata = result.get('valueRanges',[])
        maps = [''.join(x) for x in mdata[0]['values']]
        winrates = [''.join(x) for x in mdata[1]['values']]
        mapwr_dict = dict(zip(maps, winrates))
        try:
            winrate = mapwr_dict[map.upper()]
            if winrate == '-':
                await ctx.send('No data')
            else:
                await ctx.send(f'{map}:{winrate}')
        except:
            await ctx.send('Invalid map')

    @bot.command()
    async def addmap(ctx, *args):
        if len(args) == 0:
            await ctx.send('Format(quotes are required): "Date", "Team", "Result", "Map", "Score", "Notes"')
        elif len(args) == 6:
            response = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='Sheet1!A6:A', valueRenderOption='UNFORMATTED_VALUE').execute()
            offset = len(response['values']) + 6
            response = sheet.values().append(spreadsheetId=SPREADSHEET_ID, range=f'Sheet1!A{offset}', insertDataOption='INSERT_ROWS', valueInputOption='RAW', body={'majorDimension': 'ROWS', 'values':[[date, team, result, map, score, notes]]}).execute()
        else:
            await ctx.send('Invalid number of arguments')


@bot.command()
async def patchnotes(ctx):
    await ctx.send('https://www.esportstales.com/overwatch/list-all-hero-updates-and-balance-changes')

bot.run(BOT_TOKEN)
