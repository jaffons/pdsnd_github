"""
UDACITY bikeshare python project that let's you display statistics of US bikeshare data
"""

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def print_rows(df):
    """
    Displays 5 rows at the time until key or record ends

    Args:
        df - Pandas DataFrame containing city data filtered by month and day

    """
    rows = 0
    done = False
    current_row = 0
    while not done:
        if 'b' in (input("\nReady to print next 5 rows of raw data. Hit [B] to stop: \n").lower()):
            break
        else:
            rows += 5
            print("last row: {}".format(df.shape[0]) )
            if rows > df.shape[0]:
                rows = df.shape[0]
                done = True
            else:
                done = False
        for row in range(current_row, rows):
            print(df.iloc[row])
            print("")
            row +=1
        current_row = rows

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by
        (str) day - name of the day of week to filter by
    """

    def choose_thing(list):
        """ Ask for input and find corresponding item from list """
        print("\n\nAvailable options for filter are ", end='')
        print(*list, sep=', ', end = '. ')
        print("\n")
        selection = ''
        while selection not in list:
            try:
                sel = input("Filter: ").lower()
                if sel[0] == 'b':
                    return 'back'
                for n in list:
                    if sel[0] in n[0] and sel[:3] in n[:3]:
                        selection = n
                        print(selection, end='')
                        return selection

                print("Option not found. ", end='')
                selection = ''
            except:
                continue

    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    filter_modes = ['month','day','none']
    cities = ['chicago', 'new york city', 'washington']
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    wds = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'satruday', 'sunday']

    while True:
        city = ''
        filter_mode = ''
        month = ''
        day = ''
        city = choose_thing(cities)
        if city == 'back':
            continue
        filter_mode = choose_thing(filter_modes)
        if filter_mode == 'month':
            month = choose_thing(months)
            if month == 'back':
                continue
        elif filter_mode == 'day':
            day = choose_thing(wds)
            if day == 'back':
                continue
        elif filter_mode == 'back':
            continue
        else:
            filter_mode = 'none'

        print("\n\nCity selcted:\t\t{} \nFilter selected:\t{} \n\t\t\t{}{}".format(
            city.title(),
            filter_mode,
            month,
            day)
            )
        try:
            if input("\nGo back by pressing [B] or else proceed...: ").lower() == 'b':
                continue
            else:
                break
        except:
            continue
    return city, month, day


def load_data(city, month, wday):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) wday - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
        (str) - filter day/month/daymonth for

    example of data:
    id  Start Time  End Time    Trip Duration   Start Station   End Station User type   Gender  Birth Year

    ,		    Start Time,			    End Time,			    Trip Duration,	Start Station,			End Station,		User Type
    1621326,    2017-06-21 08:36:34,    2017-06-21 08:44:43,    489.066,		14th & Belmont St NW,	15th & K St NW,		Subscriber

    """
    months = {'january':1, 'february':2, 'march':3, 'april':4, 'may':5, 'june':6}
    days = {'monday':0, 'tuesday':1, 'wednesday':2, 'thursday':3, 'friday':4, 'satruday':5, 'sunday':6}
    filter = 'daymonth'

    df = pd.read_csv(CITY_DATA[city])
    # make 'Start Time' column to datetime-format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # make separate columns for month and wday
    df['month'] = df['Start Time'].dt.month
    df['wday'] = df['Start Time'].dt.weekday
    # data to match the filter
    if len(month) > 0:
        df = df.loc[df['month'] == months[month]]
        filter = 'month'
    elif len(wday) > 0:
        df = df.loc[df['wday'] == days[wday]]
        filter = 'day'
    try:
        print_rows(df)
    except:
        print("Couldn't print raw data!\n")

    """
    print(df.isnull().any())
    # We print some information about sheet
    print('Sheet is of type:', type(df))
    print('sheet info:', df.info())
    print('Sheet has shape:', df.shape)
    print('head of data:\n', df.head())
    """
    return df, filter


def time_stats(df, filter = 'daymonth'):
    """Displays statistics on the most frequent times of travel.

    Args:
        (str) filter - 'month'/'weekday'/'daymonth' to exclude unnessecary statistics
        df - Pandas DataFrame containing city data filtered by month and day

    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    months = {1:'january', 2:'february', 3:'march', 4:'april', 5:'may', 6:'june'}
    days = {0:'monday', 1:'tuesday', 2:'wednesday', 3:'thursday', 4:'friday', 5:'satruday', 6:'sunday'}

    try:
        if 'day' in filter:
            # display the most common month
            pop_month = df['month'].mode()[0]
            print("Most common month:  {}".format(months[int(pop_month)]) )
        if 'month' in filter:
            # display the most common day of week
            pop_day = df['wday'].mode()[0]
            print("Most common weekday: {}".format(days[int(pop_day)]) )

        # display the most common start hour
        df['hour'] = df['Start Time'].dt.hour
        pop_hour = df['hour'].mode()[0]
        print("Most common hour: {}".format(int(pop_hour)) )

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except:
        print("Couldn't print time related statistics!\n")


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    station_start_count = df['Start Station'].value_counts()
    print("5 Most used start stations:\n{}".format(station_start_count[:5]) )

    # display most commonly used end station
    station_end_count = df['End Station'].value_counts()
    print("\n5 Most used end stations:\n{}".format(station_end_count[:5]) )

    # display most frequent combination of start station and end station trip
    # combine start and end station to new column
    # count all trips by StartStop_Station
    print("\n5 most frequent trips (start station - end station):\n")
    df['StartStop_Station'] = df['Start Station'] + ['   to   '] + df['End Station']
    print(df['StartStop_Station'].value_counts()[:5] )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time in minutes
    print("Total trip duration in seconds: {}".format(df['Trip Duration'].sum()) )
    print("\nTotal trip duration in minutes: {}".format(df['Trip Duration'].sum() / 60) )

    # display mean travel time
    print("\nMean trip duration in minutes: {}".format(df['Trip Duration'].mean()) )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    try:
        # Display counts of user types
        print("\nTotal User account types of every trip: \n{}".format(df['User Type'].value_counts(dropna=True)) )
    except KeyError:
        print("\nSorry no user data available!")

    try:
    # Display counts of gender
        print("\nTotal user genders of every trip: \n{}".format(df['Gender'].value_counts(dropna=True)) )
    except KeyError:
        print("\nSorry no gender data available!")

    try:
        # Display earliest, most recent, and most common year of birth
        print("\nOldest user has born in {}".format(df['Birth Year'].min()) )
        print("\nYoungest user has born in {}".format(df['Birth Year'].max()) )
        byear_count = df['Birth Year'].value_counts(dropna=True)
        print("\nMost common birth years are:\n{}".format(byear_count) )
    except KeyError:
        print("\nSorry no birth year data available!")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, wday = get_filters()
        df, filter = load_data(city, month, wday)

        time_stats(df, filter)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        try:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower()[0] != 'y':
                break
        except IndexError:
            break


if __name__ == "__main__":
	main()
