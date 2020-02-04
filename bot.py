# -*- coding: utf8 -*-
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import discord
from discord.ext import commands

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
SPREADSHEET_ID = ''
RANGE_NAME = ''

creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    pass

bot = commands.Bot(command_prefix='>')