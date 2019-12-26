import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    """

    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city (chicago, new york city, washington).
    city = input(
        "Would you like to see data for Chicago, New York, or Washington? \n").lower()
    # Ask user again if they enter invalid inputs
    while (city != 'chicago' and city != 'new york city' and city != 'washington'):
        city = input(
            "Would you like to see data for Chicago, New York, or Washington? \n").lower()

    # Get user input for month (all, january, february, ... , j
    month = input(
        "Which month? January, February, March, April, May, June, or all?\n").lower()
    # Ask user again if they enter invalid inputs
    while (month != 'all' and month != 'january' and month != 'february' and month != 'march' and month != 'april' and month != 'may' and month != 'june'):
        month = input(
            'Which month? January, February, March, April, May, June, or all? \n').lower()

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Which day of the week?(Monday, ... or all) \n').lower()
    # Ask user again if they enter invalid inputs
    while (day != 'all' and day != 'monday' and day != 'tuesday' and day != 'wednesday' and day != 'thursday' and day != 'friday' and day != 'saturday' and day != 'sunday'):
        day = input('Which day of the week?(Monday, ... or all)  \n').lower()

    print('-'*40)
    return city, month, day


def convert_to_datetime(dataframe, column):
    """
    Convert data in one column into datetime type

    """
    dataframe[column] = pd.to_datetime(dataframe[column])


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    convert_to_datetime(df, 'Start Time')

    # extract month,day of week, and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month: ', popular_month)

    # Display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('\n Most Popular Day of week: ', popular_day)

    # Display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('\n Most Popular Start Hour: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station: ', popular_start_station)

    # Display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('\n The most commonly used end station: ', popular_end_station)

    # Display most frequent combination of start station and end station trip
    popular_combination = df.groupby(
        ['Start Station', 'End Station']).size().idxmax()
    print('\n The most frequent combination of start station and end station trip: ',
          popular_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # convert the Start Time  and End column to datetime
    convert_to_datetime(df, 'Start Time')
    convert_to_datetime(df, 'End Time')

    # Create a column Travel Time
    df['Travel Time'] = df['End Time'] - df['Start Time']

    # Display total travel time
    sum_travel = df['Travel Time'].sum()
    print("The total travel time: ", sum_travel)

    # Display mean travel time
    mean_travel = df['Travel Time'].mean()
    print("\nThe mean travel time: ", mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("This is the count of each type of user: \n", user_types)

    # Display counts of gender for New York City and Chicago
    if city != 'washington':
        gender = df['Gender'].value_counts()
        print("\nThis is the count of each gender: \n", gender)

        # Display earliest, most recent, and most common year of birth
        popular_year = df['Birth Year'].mode()[0]
        print("\nThe most common year of birth: ", popular_year)
        print("\nThe earliest year of birth:", df['Birth Year'].min())
        print("\nThe most recent year of birth:", df['Birth Year'].max())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """
    Display raw data upon request by the user

    """
    # Ask user if he/she want to see raw data
    answer = input("Do you want to see raw data?(yes or no)\n").lower()
    # Display data if answer is 'yes' and ask again if they want to see more lines
    if answer == 'yes':
        start_index = 0
        end_index = 6
        data = df.iloc[start_index:end_index]
        print(data)
        new_answer = input("Do you want to see more 5 lines of raw data?\n").lower()
        # Continue prompting and printing the next 5 rows at a time until the user chooses 'no'
        while new_answer != 'no':
            start_index += 5
            end_index += 5
            new_data = df.iloc[start_index:end_index]
            print(new_data)
            new_answer = input("Do you want to see more 5 lines of raw data?\n").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
