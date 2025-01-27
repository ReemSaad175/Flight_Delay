
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    layout="wide",
    page_title="Flight Delays"
)

# Load dataset
df = pd.read_csv("Flight_Delay.csv")

st.title("Airline Delay Cause Analysis")

# side bar
x= st.sidebar.checkbox('Show Data', False, key=1)

Year= st.sidebar.selectbox("Select Year", df['year'].unique())
Carrier= st.sidebar.selectbox("Select Carrier", df['carrier_name'].unique())
Airport= st.sidebar.selectbox("Select Airport", df['airport_name'].unique())
Month= st.sidebar.selectbox("Select Month", df['month name'].unique())

year_df = df[df['year'] == Year]
carrier_df = df[df['carrier_name'] == Carrier]
airport_df = df[df['airport_name'] == Airport]
month_df = df[df['month name'] == Month]
        
            

if x:
    st.header('Dataset Sample')
    st.dataframe(df.head(10))
    

tab1, tab2, tab3 = st.tabs(['📊Top Causes','📊Delay Patterns', '📊Distributions'])

with tab1:
         
    st.header("Top causes of Delay")
 
    #highest cause of delay?
    delay_causes = ['carrier_delay', 'weather_delay', 'nas_delay', 'security_delay', 'late_aircraft_delay']
    delay_contributions = df[delay_causes].mean()

    fig= px.bar(x=delay_contributions.index, y=delay_contributions.values, 
            color_discrete_sequence=px.colors.sequential.Viridis, 
               title='Flight Delay Causes')
    fig.update_layout(
    xaxis_title="Delay Cause",
    yaxis_title="Average Delays (minutes)")
    st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns([5,2,5])
    with col1:
        #top 5 years in delay?
        top_year_delay = df.groupby('year')['arr_delay'].mean().sort_values(ascending=False).head(10)
        fig = px.bar(top_year_delay, y='arr_delay', title='Top 10 years with Flight Delays', template="plotly")
        fig.update_layout(
                xaxis_title="Year",
                yaxis_title="Average Delay (minutes)")
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        #top 5 carrier in delay
        top_carrier_delay = df.groupby('carrier_name')['arr_delay'].mean().sort_values(ascending=False).head(5)
        fig = px.bar(top_carrier_delay, y='arr_delay', title='Top 5 Carriers with Flight Delays', template="plotly")
        fig.update_layout(
                xaxis_title="Carrier",
                yaxis_title="Average Delay (minutes)")
        st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns([5,2,5])
    with col1:
        #top month in delay
        top_month_delay = df.groupby('month name')['arr_delay'].mean().sort_values(ascending=False).head(5)
        fig = px.bar(top_month_delay, y='arr_delay', title='Top 5 Months with Flight Delays', template="plotly")
        fig.update_layout(
                xaxis_title="Month",
                yaxis_title="Average Delay (minutes)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        #top season in delay
        top_season_delay = df.groupby('season')['arr_delay'].mean().sort_values(ascending=False)
        fig = px.bar(top_season_delay, y='arr_delay', title='Top Season with Flight Delays', template="plotly")
        fig.update_layout(
                xaxis_title="Season",
                yaxis_title="Average Delay (minutes)")
        st.plotly_chart(fig, use_container_width=True)

    #top 10 airports with highest delay
    top_airport_delay = df.groupby('airport_name')['arr_delay'].mean().sort_values(ascending=False).head(10)
    fig = px.bar(top_airport_delay, y='arr_delay', title='Top 10 Airports with Flight Delays', template="plotly")
    fig.update_layout(
                xaxis_title="Airport",
                yaxis_title="Average Delay (minutes)")
    st.plotly_chart(fig, use_container_width=True)
    
    
    #top 10 airports with highest delay (interactive)
    delay_causes = ['carrier_delay', 'weather_delay', 'nas_delay', 'security_delay', 'late_aircraft_delay']
    selected_column = st.selectbox("Select Delay Cause", delay_causes)
    top_10_delays = df.groupby('airport_name')[selected_column].mean().sort_values(ascending=False).head(10)
    
    fig= px.bar (top_10_delays, x= top_10_delays.index, y=selected_column,
                 title= 'Top 10 Airports with Highest Delays')
    st.plotly_chart(fig,use_container_width=True)

with tab2:
    
    st.header("Delay Patterns")

    # Seasonal Patterns in Delays
    
    col1, col2, col3 = st.columns([5,2,5])
    with col1:
        month_delay = year_df.groupby('month name')['arr_delay'].mean().sort_index()
        fig = px.bar(month_delay, y='arr_delay', title=f"Flight Delays in {Year}", template="plotly")
        fig.update_layout(
                xaxis_title=f"Average Arrival Delay in {Year}",
                yaxis_title="Average Delay (minute)")
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        #Delay over time
        delay_over_time = month_df.groupby('date')['arr_delay'].sum()
        fig = px.line(delay_over_time, y='arr_delay', title=f"Delay over the years in {Month}", template="plotly")
        fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Delay (minute)")
        st.plotly_chart(fig, use_container_width=True)
        

    col1, col2, col3 = st.columns([5,2,5])
    with col1:
        # Delays by Carrier

        carrier_delay = carrier_df.groupby('carrier_name')[['arr_delay', 'carrier_delay']].mean().sort_values(by='arr_delay', ascending=False)
        fig = px.bar(delay_over_time, y='arr_delay',
                     title=f"Average Delays by {Carrier}", template="plotly")
        fig.update_layout(
                xaxis_title="Carrier",
                yaxis_title="Average Delay (minutes)")
        st.plotly_chart(fig, use_container_width=True)
    

    with col3:
        #weather related delays
        
        airport_weather_delay = year_df.groupby('airport_name')[['arr_delay','weather_delay']].mean().sort_values(by='arr_delay', ascending=False).head(15)
        fig = px.bar(airport_weather_delay, y='arr_delay',
                     title=f"Airports Weather-Related Delays in {Year}", template="plotly", 
                    labels = {"airport_name": "Airport", "arr_delay":"Average Delay (minutes)"})
        st.plotly_chart(fig)

       
        
with tab3:

    #Flight Distribution
    flights = ['arr_flights', 'arr_del15', 'arr_cancelled', 'arr_diverted']
    flights_distributions = df[flights].sum()

    # Bar plot for delay contributions
    fig1= px.bar(x=flights_distributions.values, y=flights_distributions.index, 
                 color_discrete_sequence=px.colors.sequential.Viridis,
                 title='Flight Distribution')
    fig1.update_layout(
    xaxis_title="Number of Flights",
    yaxis_title="Delay type")
    st.plotly_chart(fig1, use_container_width=True)
   
    col1, col2, col3 = st.columns([5,5,5])
    with col1:
        # Check which filters are selected and apply them one by one
        if Year:
            # Create the bar plot based on the filtered data
            flight_summary = year_df[flights].sum().reset_index()

            # Create the bar chart for the filtered data
            fig = px.bar(flight_summary, x='index', y=0, title="Yearly Flights", template="plotly")
            fig.update_layout(
            xaxis_title=f"in {Year}",
            yaxis_title='Number of Flights')
            st.plotly_chart(fig, use_container_width=True)
            
            
    with col2:
        if Carrier:
            flight_summary = carrier_df[flights].sum().reset_index()

            fig = px.bar(flight_summary, x='index', y=0, title="Flights by Carrier", template="plotly")
            fig.update_layout(
            xaxis_title=f"for {Carrier}",
            yaxis_title='Number of Flights')
            st.plotly_chart(fig, use_container_width=True)
            
            
    with col3:
        if Airport:
            flight_summary = airport_df[flights].sum().reset_index()

            fig = px.bar(flight_summary, x='index', y=0, title="Flights in Airport", template="plotly")
            fig.update_layout(
            xaxis_title=f"for {Airport}",
            yaxis_title='Number of Flights')
            st.plotly_chart(fig, use_container_width=True) 
            


    #Delay distribution
    delay_causes = ['carrier_ct', 'weather_ct', 'nas_ct', 'security_ct', 'late_aircraft_ct']
    cause_contributions = df[delay_causes].sum()

    fig2= px.bar(x=cause_contributions.values, y=cause_contributions.index, 
            color_discrete_sequence=px.colors.sequential.Viridis, 
               title='Contribution of Each Cause to Total Delays')
    fig2.update_layout(
    xaxis_title="Number of Delays",
    yaxis_title="Delay type")
    st.plotly_chart(fig2, use_container_width=True)
    
    
    col1, col2, col3 = st.columns([5,5,5])
    with col1:
        # Check which filters are selected and apply them one by one
        if Year:
            year_df = df[df['year'] == Year]

            delay_summary = year_df[delay_causes].sum().reset_index()

            fig = px.bar(delay_summary, x='index', y=0, title="Yearly Delay Causes", template="plotly")
            fig.update_layout(
                xaxis_title=f"in {Year}",
                yaxis_title="Number of Delays")
            st.plotly_chart(fig, use_container_width=True)
            
            
    with col2:
        if Carrier:
            carrier_df = df[df['carrier_name'] == Carrier]
        
            delay_summary = carrier_df[delay_causes].sum().reset_index()
            
            fig = px.bar(delay_summary, x='index', y=0, title="Delay Causes by Carrier", template="plotly")
            fig.update_layout(
                xaxis_title=f"for {Carrier}",
                yaxis_title="Number of Delays")
            st.plotly_chart(fig, use_container_width=True)
            
            
    with col3:
        if Airport:
            airport_df = df[df['airport_name'] == Airport]
            
            delay_summary = airport_df[delay_causes].sum().reset_index()

            fig = px.bar(delay_summary, x='index', y=0, title="Delay Causes For Airports", template="plotly")
            fig.update_layout(
                xaxis_title=f"for {Airport}",
                yaxis_title="Number of Delays")
            st.plotly_chart(fig, use_container_width=True)

    # Select column for analysis
    numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
    selected_column = st.selectbox("Select Numerical Column", numerical_cols)

    fig= px.histogram (df[selected_column], x=selected_column , title= f'Distribution of {selected_column}', width= 700 )
    st.plotly_chart(fig,use_container_width=True)

        
