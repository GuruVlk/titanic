import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit_shadcn_ui as ui

st.set_page_config(page_title="Titanic Data Analysis", page_icon=":ship:", layout="wide")
st.header("Titanic Data Analysis")
st.subheader("Data Analysis of Titanic Dataset using Streamlit")

### --- Load Titanic Dataset --- ###
excel_file = 'titanic.csv'
df = pd.read_csv(excel_file)

with st.expander("Show list of Passengers", expanded=False):
    st.dataframe(df)

# Group by Age and count the number of passengers
age_distribution = df.groupby('age').size().reset_index(name='Count')

# Create a bar chart for Age Distribution
bar_chart = px.bar(age_distribution, x='age', y='Count', title='Passenger Age Distribution')
st.plotly_chart(bar_chart)

st.write("## People on Board the Titanic")

# Count the number of male and female passengers
male_count = df[df['gender'] == 'male'].shape[0]
female_count = df[df['gender'] == 'female'].shape[0]

# Calculate the total number of passengers
total_passengers = df.shape[0]

cols =st.columns(3)
with cols[0]:
    ui.metric_card(
        title='Total Number of People',
        content=total_passengers,
        description='Passengers and crew on board the Titanic'
    )

with cols[1]:
    ui.metric_card(
        title='Male Passengers',
        content=male_count,
        description='Passengers and crew on board the Titanic'
    )

with cols[2]:
    ui.metric_card(
        title='Female Passengers',
        content=female_count,
        description='Passengers and crew on board the Titanic'
    )




# Group by 'class' and count the number of people in each class
class_counts = df.groupby('class').size()

# Assign the sums to variables for each class
third_class_count = class_counts.get('3rd', 0)
second_class_count = class_counts.get('2nd', 0)
first_class_count = class_counts.get('1st', 0)
engineering_crew_count = class_counts.get('engineering crew', 0)
victualling_crew_count = class_counts.get('victualling crew', 0)
restaurant_staff_count = class_counts.get('restaurant staff', 0)
deck_crew_count = class_counts.get('deck crew', 0)






# Example of how to display these counts using Streamlit
# First row
cols2 = st.columns(7)
with cols2[0]:
    ui.metric_card(
        title='1st Class',
        content=int(first_class_count),  # Cast to int
        description='Passenger'
    )
with cols2[1]:
    ui.metric_card(
        title='2nd Class',
        content=int(second_class_count),  # Cast to int
        description='Passenger'
    )
with cols2[2]:
    ui.metric_card(
        title='3rd Class',
        content=int(third_class_count),  # Cast to int
        description='Passenger'
    )
with cols2[3]:
    ui.metric_card(
        title='Engineering',
        content=int(engineering_crew_count),
        description='Crew'
    )
with cols2[4]:
    ui.metric_card(
        title='Victualling',
        content=int(victualling_crew_count),
        description='Crew'
    )
with cols2[5]:
    ui.metric_card(
        title='Restaurant',
        content=int(restaurant_staff_count),
        description='Crew'
    )
with cols2[6]:
    ui.metric_card(
        title='Deck',
        content=int(deck_crew_count),
        description='Crew'
    )



# Group by 'class' and 'survived' columns and count the number of people in each group

st.write("## Passenger Survival Rate Per Class")

df['survived_numeric'] = df['survived'].map({'yes': 1, 'no': 0})

# Calculate survival rates by class
survival_rates_by_class = df.groupby('class')['survived_numeric'].mean()

# Convert the survival rates to a DataFrame for easier plotting
survival_rates_df = survival_rates_by_class.reset_index()

# Sort the DataFrame in ascending order by the 'survived_numeric' column
survival_rates_df = survival_rates_df.sort_values(by='survived_numeric', ascending=False)

# Rename columns for clarity in the plot
survival_rates_df.columns = ['Passenger Class', 'Survival Rate']


# Create a Plotly bar chart
fig = px.bar(survival_rates_df, x='Passenger Class', y='Survival Rate',
             text='Survival Rate',
             labels={'Survival Rate':'Survival Rate (%)'})

# Update the text on the bars to show percentages with 1 decimal place
fig.update_traces(texttemplate='%{text:.1%}', textposition='outside')

# Update layout for a cleaner look
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

# Display the plot in Streamlit
st.plotly_chart(fig)



# Show People grouped by Country Crew
st.write("## People by Country")


# Group by 'country' and count the number of crew members in each country
crew_counts = df[df['class'].isin(['engineering crew', 'victualling crew', 'restaurant staff', 'deck crew'])].groupby('country').size()

# Create a pie chart for crew members by country
pie_chart_crew = px.pie(crew_counts, values=crew_counts.values, names=crew_counts.index, title='Crew Members by Country')
st.plotly_chart(pie_chart_crew)




# Group by 'country' and count the number of crew members in each country
crew_counts = df[df['class'].isin(['1st', '2nd', '3rd', 'Passengers'])].groupby('country').size()

# Create a pie chart for crew members by country
pie_chart_crew = px.pie(crew_counts, values=crew_counts.values, names=crew_counts.index, title='Passengers Members by Country')
st.plotly_chart(pie_chart_crew)


# Show Deat rate by Country 
st.write("## Survival Rate by Country Relative to Total Passengers from that Country") 

df['survived_numeric'] = df['survived'].map({'yes': 1, 'no': 0})

# Calculate survival rates by class
survival_rates_by_class = df.groupby('country')['survived_numeric'].mean()

# Convert the survival rates to a DataFrame for easier plotting
survival_rates_df = survival_rates_by_class.reset_index()

# Sort the DataFrame in ascending order by the 'survived_numeric' column
survival_rates_df = survival_rates_df.sort_values(by='survived_numeric', ascending=False)

# Rename columns for clarity in the plot
survival_rates_df.columns = ['Passenger Class', 'Survival Rate']


# Create a Plotly bar chart
fig = px.bar(survival_rates_df, x='Passenger Class', y='Survival Rate',
             text='Survival Rate',
             labels={'Survival Rate':'Survival Rate (%)'})

# Update the text on the bars to show percentages with 1 decimal place
fig.update_traces(texttemplate='%{text:.1%}', textposition='outside')

# Update layout for a cleaner look
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

# Display the plot in Streamlit
st.plotly_chart(fig)


# Show Deat rate by Country 
st.write("## Deaths by Country") 

# Group by 'country' and count the number of deaths in each country
death_counts = df[df['survived'] == 'no'].groupby('country').size()
# Sort the death counts in descending order
death_counts = death_counts.sort_values(ascending=False)

# Create a bar chart for deaths by country
bar_chart_deaths = px.bar(death_counts, x=death_counts.index, y=death_counts.values, title='Deaths by Country')
st.plotly_chart(bar_chart_deaths)