import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Please input city (chicago, new york city, washington): ").lower()

    while city not in ['chicago', 'new york city', 'washington']:
        city = input(
        "City is incorrect! Please input another name: ").lower()

    # get user input for month (all, january, february, ... , june)
    month = input("Please input month (January - June, or all): ").lower()

    while month not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
      month = input(
      "month is incorrect! Please input another name: ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please input day (monday - sunday, or all): ").lower()
    while day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
        day = input('day is incorrect! Please input another name')

    print('-'*40)
    return city, month, day


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

    #loading the file into data frame
    df = pd.read_csv(CITY_DATA[city])
    print( df.head() )
    # Converting start and end time columns to datetimes
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Extracting day and month from Start Time into new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    # filter by month if applicable
    if month != 'all':
   	 	# converting months to int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

    	# filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, popular_month, day_of_week):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('The most common month:', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('The most common day:', day_of_week)


    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most common hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most common start station is: {} ".format(
        df['Start Station'].mode().values[0]))

    # display most commonly used end station
    print("The most common end station is: {}".format(
        df['End Station'].mode().values[0]))

    # display most frequent combination of start station and end station trip
    df['routes'] = df['Start Station']+ " " + df['End Station']
    print("The most common start and end station combo is: {}".format(
        df['routes'].mode().values[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    Total_Travel_Time = sum(df['Trip Duration'])
    print('Total travel time:', Total_Travel_Time/86400, " Days")

    # display mean travel time
    Mean_Travel_Time = df['Trip Duration'].mean()
    print('Mean travel time:', Mean_Travel_Time/60, " Minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user = df['User Type'].value_counts()
    print('Counts of user type are {}.'.format(count_user))

    # Display counts of gender
    if "Gender" in df.columns:
        genders = df['Gender'].value_counts()
        print('gender count:', genders)
    else:
        print ('gender does not exist')

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        print("The earliest birth year is: {}".format(
        str(int(df['Birth Year'].min()))))
    else:
        print('birth year does not exist')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw(df):
    """
    Display contents of the CSV file if requested by the user.
    """

    start_spot = 0
    end_spot = 5

    display_active = input("Would you like to see the raw data (yes or no)?: ").lower()

    if display_active == 'yes':
        while end_spot <= df.shape[0] - 1:
            print(df.iloc[start_spot:end_spot,:])
            start_spot += 5
            end_spot += 5

            end_display = input("Would you like to continue (yes or no): ").lower()
            if end_display == 'no':
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, day, month)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
