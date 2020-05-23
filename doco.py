#!/usr/bin/env python3
from bottle import post, template, get, route, run, request, response
import re, json
from time import sleep
import RPi.GPIO as GPIO

GARAGE_UP = 23
GARAGE_DOWN = 24
GARAGE_IMPULSE = 25
GARAGE_CLIMATE = 8

FENCE_OPEN = 7
FENCE_CLOSE = 1
FENCE_IMPULSE = 12
FENCE_HALF = 16

INTERVAL = 0.1

def _initialize():
  global my_token

  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)

  GPIO.setup(GARAGE_UP, GPIO.OUT)
  GPIO.setup(GARAGE_DOWN, GPIO.OUT)
  GPIO.setup(GARAGE_IMPULSE, GPIO.OUT)
  GPIO.setup(GARAGE_CLIMATE, GPIO.OUT)
  GPIO.setup(FENCE_OPEN, GPIO.OUT)
  GPIO.setup(FENCE_CLOSE, GPIO.OUT)
  GPIO.setup(FENCE_IMPULSE, GPIO.OUT)
  GPIO.setup(FENCE_HALF, GPIO.OUT)

  GPIO.output(GARAGE_UP,GPIO.HIGH)
  GPIO.output(GARAGE_DOWN,GPIO.HIGH)
  GPIO.output(GARAGE_IMPULSE,GPIO.HIGH)
  GPIO.output(GARAGE_CLIMATE,GPIO.HIGH)
  GPIO.output(FENCE_OPEN,GPIO.HIGH)
  GPIO.output(FENCE_CLOSE,GPIO.HIGH)
  GPIO.output(FENCE_IMPULSE,GPIO.HIGH)
  GPIO.output(FENCE_HALF,GPIO.HIGH)

  f = open("/srv/www/doco/my_token.tok", "r")
  my_token = str.strip(f.read())

def _control(command):
  GPIO.output(command, GPIO.LOW)
  sleep(INTERVAL)
  GPIO.output(command, GPIO.HIGH)

@post('/move')
def move():

  #read JSON Content
  try:
    try:
      data = request.json
    except:
      raise ValueError
    if data is None:
      raise ValueError

    if data['token'] is None:
      raise ValueError
    else:
      token = data['token']

    if data['gate'] is None:
      raise ValueError
    else:
      gate = data['gate']

    if data['direction'] is None:
      raise ValueError
    else:
      dir = data['direction']

  except ValueError:
    response.status = 400
    return

  #validate content
  try:
    if my_token is None:
      response.status = 500
      raise
    elif my_token == "":
      response.status = 500
      raise
    elif my_token != token:
      response.status = 403
      raise

    if not (gate == "garage" or gate == "fence"):
      response.status = 400
      raise

    if gate == "garage":
      if dir == "up":
        _control(GARAGE_UP)
      elif dir == "down":
        _control(GARAGE_DOWN)
      elif dir == "impulse":
        _control(GARAGE_IMPULSE)
      elif dir == "climate":
        _control(GARAGE_CLIMATE)
      else:
        response.status = 400
        raise
    elif gate == "fence":
      if dir == "open":
        _control(FENCE_OPEN)
      elif dir == "close":
        _control(FENCE_CLOSE)
      elif dir == "impulse":
        _control(FENCE_IMPULSE)
      elif dir == "half":
        _control(FENCE_HALF)
      else:
        response.status = 400
        raise
    else:
      response.status = 400
      raise

  except:
    return

  response.status = 200
  return;



#Main
_initialize()
run(host='0.0.0.0', port=8080)