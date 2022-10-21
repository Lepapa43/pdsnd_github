
import time
import pandas as pd
import numpy as np




CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }



# Get input from user
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    while True:
        city = input("\n Enter the name of the City (chicago,new york city,washington) : ").lower()
        if city in CITY_DATA.keys():
            break
        else:
            print("\n Invalid: Enter a Valid City Name!!!")

    # get user input for month (all, january, february, ... , june)
    months= ['january','february','march','april','june','may','all']
    while True:
        month = input("\n Enter the Month name (January,February,March,April,May,June): ").lower()
        if month in months:
            break
        else:
            print("\n Invalid: Enter Valid Month Name!!!")
        

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days= ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']
    while True:
        day = input("\n Enter Day Name (Monday,Tuesday,Wednesday,Thursday,Friday): ").lower()
        if day in days:
            break
        else:
            print("\n Invalid: Enter Valid Day Name!!!")

    print('-'*40)
    return city, month, day



# load data from csv files based on the info provided by the user above
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load data into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month from Start Time
    df['month'] = df['Start Time'].dt.month_name()
    
    # extract day of the week from Start Time
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # filter by month if applicable
    if month != 'all':
    
        # filter by month to create the new dataframe
        df = df[df['month'].str.startswith(month.title())] 

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'].str.startswith(day.title())]

        
    return df




#1 popular times of travel
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['month'] = df['Start Time'].dt.month_name()
    most_common_month = df['month'].mode()[0]
    print("Most common month is ", most_common_month)


    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.day_name()
    most_common_day = df['day_of_week'].mode()[0]
    print('The most common day is ', most_common_day)



    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print('The most common hour is ', most_common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



#2 popular stations and trips
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    pop_start_station= df['Start Station'].mode()[0]
    print("The most commonly used Start Station is {}".format(pop_start_station))

    # display most commonly used end station
    pop_end_station= df['End Station'].mode()[0]
    print("The most commonly used End Station is {}".format(pop_end_station))



    # display most frequent combination of start station and end station trip
    df['combination']=df['Start Station']+" "+"to"+" "+ df['End Station']
    pop_com= df['combination'].mode()[0]
    print("The most frequent combination of Start and End Station is {} ".format(pop_com))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



#3 trip duration
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration=df['Trip Duration'].sum()
    minute,second=divmod(total_duration,60)
    hour,minute=divmod(minute,60)
    print("The total trip duration: {} hour(s) {} minute(s) {} second(s)".format(hour,minute,second))


    # display mean travel time
    average_duration=round(df['Trip Duration'].mean())
    m,sec=divmod(average_duration,60)
    if m>60:
        h,m=divmod(m,60)
        print("The total trip duration: {} hour(s) {} minute(s) {} second(s)".format(h,m,sec))
    else:
        print("The total trip duration: {} minute(s) {} second(s)".format(m,sec))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



#4 user info
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts= df['User Type'].value_counts()
    print("The user types are:\n",user_counts)

    
    # Display counts of gender
    try:
        print("Gender is\n", df['Gender'].value_counts())
         # Display earliest, most recent, and most common year of birth
        print("The oldest user(Earliest) is born of the year", df['Birth Year'].min())
        print("The youngest user(most recent) is born of the year", df['Birth Year'].max())
        print("Most common year of birth is", df['Birth Year'].mode()[0])    
        
    except:
        print('No filter with gender allowed in Washington city!')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Asking if the user want show more data
def ask_more_data(df):
    more_data = input("Would you like to view 5 rows of data? Enter yes or no? ").lower()
    start_loc = 0
    while more_data == 'yes':
        print(df.iloc[0:5])
        start_loc += 5
        more_data = input("Would you like to view 5 more rows of data? Enter yes or no? ").lower()
        
    return df
# main function
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        ask_more_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()





