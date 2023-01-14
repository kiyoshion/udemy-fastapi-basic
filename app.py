import streamlit as st
import random
import requests
import json

st.title('User API TEST (User)')

with st.form(key='user'):
  user_id: int = random.randint(0, 10)
  user_name: str = st.text_input('user name', max_chars=12)
  data = {
    'user_id': user_id,
    'user_name': user_name
  }
  submit_button = st.form_submit_button(label='SEND')

if submit_button:
  st.write('## data')
  st.json(data)
  st.write('## response')
  url = 'http://127.0.0.1:8000/users'
  res = requests.post(
    url,
    data=json.dumps(data)
  )
  st.json(res.json())
