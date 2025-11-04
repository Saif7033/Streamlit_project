import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.set_page_config(layout="wide",page_title='Startup Analysis')
df= pd.read_csv('cleaned_startup_data.csv')
df['date']= pd.to_datetime(df['date'],errors='coerce')
df['month']= df['date'].dt.month
df['year']= df['date'].dt.year

def overall_analysis():
    #totol amount invested on startup
    total_amount= round(df['amount'].sum())
    col1, col2,col3,col4 = st.columns(4)
    with col1:
        st.metric('Total Amount', str(total_amount) + ' Cr')

    #max amount invested
    with col2:
        max_amount= df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(1).values[0]
        st.metric('Max Amount', str(round(max_amount)) + ' Cr')

    #AVERAGE INVESTMENT  ON STARTUP
    with col3:
        average_amount= df.groupby('startup')['amount'].sum().mean()
        st.metric('Average Amount', str(round(average_amount)) + ' Cr')

    #count of investments
    with col4:
        count= df['startup'].nunique()
        st.metric('Total Investments',count)
    #mom
    st.header('Month on Month Graph')
    selected_option= st.selectbox('Select Type',['Total','Count'])
    if selected_option == 'Total':

        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
        plot_column = 'amount'
        y_label = 'Total Amount (Cr)'
    else:
        temp_df = df.groupby(['year', 'month'])['startup'].count().reset_index()
        plot_column = 'startup'  # This column now holds the count
        y_label = 'Number of Investments'

    temp_df['month_year'] = pd.to_datetime(temp_df[['year', 'month']].assign(day=1))
    temp_df = temp_df.sort_values('month_year')

    fig4, ax4 = plt.subplots(figsize=(10, 6)) # Make it a bit wider
    ax4.plot(temp_df['month_year'], temp_df[plot_column])
    ax4.set_ylabel(y_label)

    ax4.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%b'))
    fig4.autofmt_xdate()  # Auto-rotates dates

    st.pyplot(fig4)
def investor_details(investor):
    #name of investor
    st.title(investor)
    #last five investors
    last_investors= df[df['investors'].str.contains(investor)].head()[
        ['date', 'startup', 'vertical', 'subvertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last_investors)

    #Biggest investment
    col1, col2 = st.columns(2)
    with col1:
        biggest_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().head(
            10).sort_values(ascending=False).head(10)
        st.subheader('Top Investments Companies')
        fig, ax = plt.subplots()
        ax.bar(biggest_series.index, biggest_series.values)
        st.pyplot(fig)

    # Sector pie chart
    with col2:
        sectors_pie= df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Top Invested Sectors')
        fig1, ax1 = plt.subplots()
        ax1.pie(sectors_pie, labels=sectors_pie.index,autopct='%1.1f%%', shadow=False, startangle=90)
        st.pyplot(fig1)


    #for which stage
    col4,col5= st.columns(2)
    with col4:
        stages_pie= df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum().head(
            10).sort_values(ascending=False).head(10)
        st.subheader('Stages ')
        fig3, ax3 = plt.subplots()
        ax3.pie(stages_pie, labels=stages_pie.index, autopct='%1.1f%%', shadow=False)
        st.pyplot(fig3)


    #for the highest city
    with col5:
        biggest_city = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum().head(
            10).sort_values(ascending=False).head(10)

        st.subheader('Top Invested Cities')

        fig2, ax2 = plt.subplots(figsize=(6, 6))
        ax2.pie(biggest_city.values, labels=biggest_city.index, autopct='%1.1f%%', shadow=False,
                startangle=90)
        ax2.axis('equal')
        st.pyplot(fig2)

    #YEAR ON YEAR INVESTMENT

    year_series = df.groupby('year')['amount'].sum()

    if year_series.empty:
        st.write("No year-on-year data found.")
    else:
     
        fig5, ax5 = plt.subplots(figsize=(8, 6))
        ax5.plot(year_series.index, year_series.values, marker='o')
        ax5.set_xlabel("Year")
        ax5.set_ylabel("Amount Invested (Cr)")
        st.pyplot(fig5)  

st.sidebar.header('Menu')
option =st.sidebar.selectbox('Whats you need ?',['Overall Data Visualization','Startup','Investors'])


if option == 'Overall Data Visualization':

    bt1= st.sidebar.button('Search overall data')
    if bt1:
        st.title('General Data Visualization')
        overall_analysis()



elif option == 'Startup':
    st.sidebar.selectbox('Choose your startup',sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button('Search about Startup')
    st.title ('Startup')
elif option == 'Investors':
    selected_investor= st.sidebar.selectbox('Choose your investors',sorted(set(df['investors'].str.split(',').sum())))
    btn2= st.sidebar.button('Search about Investors')
    if btn2:
        investor_details(selected_investor)


