import streamlit as st
import datetime
import requests
import json
import pandas as pd

page = st.sidebar.selectbox('Choose', ['users', 'rooms', 'bookings'])

if page == 'users':
  st.title('User create')
  with st.form(key='user'):
    # user_id: int = random.randint(0, 10)
    user_name: str = st.text_input('user name', max_chars=12)
    data = {
      # 'user_id': user_id,
      'user_name': user_name
    }
    submit_button = st.form_submit_button(label='SEND')

  if submit_button:
    url = 'http://127.0.0.1:8000/users'
    res = requests.post(
      url,
      data=json.dumps(data)
    )
    if res.status_code == 200:
      st.success('completed')
    st.json(res.json())

elif page == 'rooms':
  st.title('Room Create')
  with st.form(key='room'):
    # room_id: int = random.randint(0, 10)
    room_name: str = st.text_input('room name', max_chars=12)
    capacity: int = st.number_input('cap', step=1)
    data = {
      # 'room_id': room_id,
      'room_name': room_name,
      'capacity': capacity
    }
    submit_button = st.form_submit_button(label='SEND')

  if submit_button:
    url = 'http://127.0.0.1:8000/rooms'
    res = requests.post(
      url,
      data=json.dumps(data)
    )
    if res.status_code == 200:
      st.success('completed')
    st.json(res.json())

elif page == 'bookings':
  st.title('booking create')

  url_users = 'http://localhost:8000/users'
  res = requests.get(url_users)
  users = res.json()
  users_name = {}

  for user in users:
    users_name[user['user_name']] = user['user_id']

  url_rooms = 'http://localhost:8000/rooms'
  res = requests.get(url_rooms)
  rooms = res.json()
  rooms_name = {}

  for room in rooms:
    rooms_name[room['room_name']] = {
      'room_id': room['room_id'],
      'capacity': room['capacity']
    }

  st.write('### rooms')
  df_rooms = pd.DataFrame(rooms)
  df_rooms.columns = ['name', 'cap', 'id']
  st.table(df_rooms)

  url_bookings = 'http://localhost:8000/bookings'
  res = requests.get(url_bookings)
  bookings = res.json()
  df_bookings = pd.DataFrame(bookings)

  users_id = {}
  for user in users:
    users_id[user['user_id']] = user['user_name']

  rooms_id = {}
  for room in rooms:
    rooms_id[room['room_id']] = {
      'room_name': room['room_name'],
      'capacity': room['capacity'],
    }

  to_user_name = lambda x: users_id[x]
  to_room_name = lambda x: rooms_id[x]['room_name']
  to_datetime = lambda x: datetime.datetime.fromisoformat(x).strftime('%y/%m/%d %H:%M')

  df_bookings['user_id'] = df_bookings['user_id'].map(to_user_name)
  df_bookings['room_id'] = df_bookings['room_id'].map(to_room_name)
  df_bookings['start_datetime'] = df_bookings['start_datetime'].map(to_datetime)
  df_bookings['end_datetime'] = df_bookings['end_datetime'].map(to_datetime)

  df_bookings = df_bookings.rename(columns={
    'user_id': 'user',
    'room_id': 'room',
    'booked_num': 'cap',
    'start_datetime': 'start',
    'end_datetime': 'end',
    'booking_id': 'id',
  })

  st.write('### bookings')
  st.table(df_bookings)

  with st.form(key='booking'):
    user_name: str = st.selectbox('user', users_name.keys())
    room_name: str = st.selectbox('room', rooms_name.keys())
    booked_num: int = st.number_input('cap', step=1, min_value=1)
    date = st.date_input('date: ', min_value=datetime.date.today())
    start_time = st.time_input('start: ', value=datetime.time(hour=9, minute=0))
    end_time = st.time_input('end: ', value=datetime.time(hour=20, minute=0))
    submit_button = st.form_submit_button(label='SEND')


  if submit_button:
    user_id: int = users_name[user_name]
    room_id: int = rooms_name[room_name]['room_id']
    capacity: int = rooms_name[room_name]['capacity']
    data = {
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

    if booked_num > capacity:
      st.error(f'{room_name} is till {capacity}')

    elif start_time >= end_time:
      st.error(f'{start_time} is over')

    elif start_time < datetime.time(hour=9, minute=0, second=0) or end_time > datetime.time(hour=20, minute=0, second=0):
      st.error(f'time is between 9 and 20')

    else:
      url = 'http://127.0.0.1:8000/bookings'
      res = requests.post(
        url,
        data=json.dumps(data)
      )
      if res.status_code == 200:
        st.success('completed')
        st.json(res.json())
      elif res.status_code == 404 and res.json()['detail'] == 'Already booked':
        st.error('booking is already')
      