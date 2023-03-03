import openai as ai
import os
import streamlit as st

def open_file(filepath):
    with open(filepath,'r',encoding='utf-8') as infile:
        return infile.read()


ai.api_key = open_file('key.txt')

def chatbot(prompt,engine ='text-davinci-003',temp = 0.7,tokens = 100,top_p = 1.0,freq_pen = 0.0,pres_pen = 0.0,stop=['JAX: ','USER: ']):
    prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
    response = ai.Completion.create(
        engine = engine,
        prompt = prompt,
        temperature = temp,
        max_tokens = tokens,
        top_p = top_p,
        frequency_penalty = freq_pen,
        presence_penalty = pres_pen,
        stop= stop
    )
    text = response['choices'][0]['text'].strip()
    return text

def proccess(prompt):
    response = ai.Completion.create(
        engine = 'text-curie-001',
        prompt = prompt,
        temperature = 0.7,
        max_tokens = 100,
        top_p = 1.0,
        frequency_penalty = 0.0,
        presence_penalty = 0.0,
        
    )

    text = response['choices'][0]['text']
    return text

def image_process(prompt):
    response = ai.Image.create(
        prompt = prompt,
        n = 1,
        size = "1024x1024"
    )
    image_url = response['data'][0]['url']
    return image_url

    