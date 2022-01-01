import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("\nHello! Let's explore some US bikeshare data!\n")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input("\nLet's select a city to focus on! \nPlease select either Chicago, New York City, Washington, or All if you would like to look at the entire dataset.\n").lower()
        except:
            print("\nThat is not a valid selection! Please try again.\n")
        else:
            if city not in ['chicago', 'new york city', 'washington', 'all']:
                print("\nThat is not a valid selection! Please try again.\n")
            else:
                print("\nYou selected {}!\n".format(city.title()))
                break

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input("\nLet's select a month to focus on as well! \nPlease enter a month January through June or all to see data for every month.\n").lower()
        except:
            print("\nThat is not a valid selection! Please try again.\n")
        else:
            if month not in months:
                print("\nThat is not a valid selection! Please try again.\n")
            else:
                print("\nYou selected {}!\n".format(month.capitalize()))
                break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input("\nLastly, we would like you to select a day of the week for our analysis. \nPlease indicate a day or all to look at the entire week.\n").lower()
        except:
            print("\nThat is not a valid selection!\n")
        else:
            if day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
                print("\nThat is not a valid selection! Please try again.\n")
            else:
                print("\nYou selected {}!\n".format(day.capitalize()))
                break

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
    # City Filter
    if city != 'all':
        df = pd.read_csv(CITY_DATA[city])
    else:
        df = pd.read_csv('chicago.csv')
        df = df.append(pd.read_csv('new_york_city.csv'))
        df = df.append(pd.read_csv('washington.csv'))

    # DateTime Conversions
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Date Extractions
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_of_week

    # Month Filter
    if month != 'all':
        month = months.index(month) + 1
        df = df[df['Month'] == month]

    # Day Filter
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)
        df = df[df['Day of Week'] == day]

    return df

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        month_mode = df['Month'].mode()[0]
        print("The month with the most number of trips was {}.".format(months[month_mode - 1].title()))

    # display the most common day of week
    if day == 'all':
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_mode = df['Day of Week'].mode()[0]
        print("The most popular day of the week to travel was {}.".format(days[day_mode]))

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    hour_mode = int(df['Hour'].mode()[0])
    if hour_mode == 0:
        hour_mode = 'midnight'
    elif hour_mode > 12:
        hour_mode = '{} pm'.format(hour_mode - 12)
    else:
        hour_mode = '{} am'.format(hour_mode)
    print("Most travelers started their trips at about {}.".format(hour_mode))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station_mode = df['Start Station'].mode()[0]
    print("The most popular start station was {}.".format(start_station_mode))

    # display most commonly used end station
    end_station_mode = df['End Station'].mode()[0]
    print("The most popular end station was {}.".format(end_station_mode))

    # display most frequent combination of start station and end station trip
    df['Route'] = df['Start Station'] + ' to ' + df['End Station']
    route_mode = df['Route'].mode()[0]
    print("The most popular route was {}.".format(route_mode))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Trip Duration'] = df['Trip Duration']
    total_time = df['Trip Duration'].sum()
    seconds = total_time % 60
    minutes = total_time // 60
    hours = minutes // 60
    minutes = int(minutes % 60)
    days = hours // 24
    hours = int(hours % 24)
    weeks = days // 7
    days = int(days % 7)
    years = int(weeks // 52)
    weeks = int(weeks % 52)

    if years > 0:
        print("Total travel time was {} year(s), {} week(s), {} day(s), {} hour(s), {} minute(s), and {} second(s)."
        .format(years, weeks, days, hours, minutes, seconds))
    elif weeks > 0:
        print("Total travel time was {} week(s), {} day(s), {} hour(s), {} minute(s), and {} second(s)."
        .format(weeks, days, hours, minutes, seconds))
    elif days > 0:
        print("Total travel time was {} day(s), {} hour(s), {} minute(s), and {} second(s)."
        .format(days, hours, minutes, seconds))
    elif hours > 0:
        print("Total travel time was {} hour(s), {} minute(s), and {} second(s)."
        .format(hours, minutes, seconds))
    else:
        print("Total travel time was {} minute(s) and {} second(s)."
        .format(minutes, seconds))

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    trip_minutes = int(mean_time // 60)
    trip_seconds = mean_time % 60
    print("The average trip duration was {} minute(s) and {} second(s).".format(trip_minutes, trip_seconds))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Here are the number of travelers by user type:")
    print(user_types.to_string())

    #Data Disclaimer
    if city == 'all':
        print("\nThe following information only represents subscribers in Chicago and New York city."
        "\nDemographic data was not collected for Washington.\n")

    # Display counts of gender
    if city in ['chicago', 'new york city', 'all']:
        gender = df['Gender'].value_counts()
        print("\nHere are the number of subscribers by gender:")
        print(gender.to_string())


    # Display earliest, most recent, and most common year of birth
    if city in ['chicago', 'new york city', 'all']:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        birth_year_mode = int(df['Birth Year'].mode()[0])
        print("\nFor our subscribers, the earliest birth year was {}, the most recent birth year was {}, and the most common birth year was {}.".format(earliest_birth_year, most_recent_birth_year, birth_year_mode))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Displays raw data."""

    while True:
        try:
            initial_display = input("\nWould you like to see the first 5 rows of raw data? Enter yes or no.\n")
        except:
            print("That is not a valid selection! Please try again.\n")
        else:
            if initial_display.lower() not in ['yes', 'no']:
                print("That is not a valid selection! Please try again.\n")
            elif initial_display.lower() == 'yes':
                row_index = 0
                print(df.head(5))
                break
            else:
                break

    if initial_display.lower() == 'yes':
        while True:
            try:
                more_rows = input("\nWould you like to see the next 5 rows of data? Enter yes or no.\n")
            except:
                print("That is not a valid selection! Please try again.\n")
            else:
                if more_rows.lower() not in ['yes', 'no']:
                    print("That is not a valid selection! Please try again.\n")
                elif more_rows.lower() == 'yes':
                    row_index += 5
                    print(df.iloc[row_index : row_index + 5])
                else:
                    break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
