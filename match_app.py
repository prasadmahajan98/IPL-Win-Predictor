import streamlit as st
import pickle
import pandas as pd
pipe = pickle.load(open('pipe.pkl','rb'))

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://cdn.pixabay.com/photo/2022/02/16/04/15/cricketer-7015983_960_720.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()

teams =  [
    'Sunrisers Hyderabad',
    'Mumbai Indians',
    'Royal Challengers Bangalore',
    'Kolkata Knight Riders',
    'Kings XI Punjab',
    'Chennai Super Kings',
    'Rajasthan Royals',
    'Delhi Capitals'
]

cities = ['Delhi', 'Port Elizabeth', 'Mumbai', 'Raipur', 'Chennai', 'Jaipur',
       'Sharjah', 'Hyderabad', 'Pune', 'Kolkata', 'Cape Town',
       'Centurion', 'Dharamsala', 'Visakhapatnam', 'Bangalore',
       'Abu Dhabi', 'Chandigarh', 'Bengaluru', 'Indore', 'Durban',
       'Johannesburg', 'Bloemfontein', 'Mohali', 'Cuttack', 'Ranchi',
       'Ahmedabad', 'East London', 'Kimberley', 'Nagpur']

st.title('IPL Match Win Predictor')

# Batting and Bowling Team
col1,col2 = st.columns(2)
 
with col1:
    batting_team = st.selectbox('Select Batting Team',sorted(teams))

with col2:
    bowling_team = st.selectbox('Select Bowling Team',sorted(teams))

# Select City
selected_city = st.selectbox('Select the Host City',sorted(cities))

# Target
target = st.number_input('Target')

#

col3,col4,col5 = st.columns(3)

with col3:
    score = st.number_input('Current Score')

with col4:
    overs = st.number_input('Overs Completed')

with col5:
    wickets = st.number_input('Wickets Down')

# Display Probability

if  st.button('Predict Probablity'):
    runs_left = target - score
    balls_left = 120 - (overs*6)
    wickets_in_hand = 10 - wickets
    crr = score/overs
    rrr = (runs_left*6)/(balls_left)

    input_df = pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],'city':[selected_city],
    'runs_left':[runs_left],'balls_left':[balls_left],'wickets_in_hand':[wickets_in_hand],'total_runs_x':[target],'crr':[crr],'rrr':[rrr]})

    st.table(input_df)

    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    
    st.text("Win Percentage of both teams")
    st.text(batting_team + " - " + str(round(win*100)) + "%")
    st.text(bowling_team + " - " + str(round(loss*100)) + "%")