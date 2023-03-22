import json
import requests
import flask

def handler(event, context):
    print(event)
    return "Hello World!"