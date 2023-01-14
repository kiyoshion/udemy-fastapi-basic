import streamlit as st
import datetime
import random
import requests
import json

page = st.sidebar.selectbox('Choose', ['users', 'rooms', 'bookings'])

if page == 'users':
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

elif page == 'rooms':
  st.title('Room API TEST (Room)')
  with st.form(key='room'):
    room_id: int = random.randint(0, 10)
    room_name: str = st.text_input('room name', max_chars=12)
    capacity: int = st.number_input('cap', step=1)
    data = {
      'room_id': room_id,
      'room_name': room_name,
      'capacity': capacity
    }
    submit_button = st.form_submit_button(label='SEND')

  if submit_button:
    st.write('## data')
    st.json(data)
    st.write('## response')
    url = 'http://127.0.0.1:8000/rooms'
    res = requests.post(
      url,
      data=json.dumps(data)
    )
    st.json(res.json())

elif page == 'bookings':
  st.title('booking API TEST (booking)')
  with st.form(key='booking'):
    booking_id: int = random.randint(0, 10)
    user_id: int = random.randint(0, 10)
    room_id: int = random.randint(0, 10)
    booked_num: int = st.number_input('cap', step=1)
    date = st.date_input('date: ', min_value=datetime.date.today())
    start_time = st.time_input('start: ', value=datetime.time(hour=9, minute=0))
    end_time = st.time_input('end: ', value=datetime.time(hour=20, minute=0))
    data = {
      'booking_id': booking_id,
      'user_id': user_id,
      'room_id': room_id,
      'booked_num': booked_num,
      'start_datetime': datetime.datetime(
        year=date.year,
        month=date.month,
        day=date.day,
        hour=start_time.hour,
        minute=start_time.minute
      ).isoformat(),
      'end_datetime': datetime.datetime(
        year=date.year,
        month=date.month,
        day=date.day,
        hour=end_time.hour,
        minute=end_time.minute
      ).isoformat(),
    }
    submit_button = st.form_submit_button(label='SEND')

  if submit_button:
    st.write('## data')
    st.json(data)
    st.write('## response')
    url = 'http://127.0.0.1:8000/bookings'
    res = requests.post(
      url,
      data=json.dumps(data)
    )
    st.json(res.json())
