import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def getFilters():
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


def convertToDatetime(dataframe, column):
    """
    Convert data in one column into datetime type

    """
    dataframe[column] = pd.to_datetime(dataframe[column])


def loadData(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    convertToDatetime(df, 'Start Time')

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


def timeStats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    startTime = time.time()

    # Display the most common month
    popularMonth = df['month'].mode()[0]
    print('Most Popular Month: ', popularMonth)

    # Display the most common day of week
    popularDay = df['day_of_week'].mode()[0]
    print('\n Most Popular Day of week: ', popularDay)

    # Display the most common start hour
    popularHour = df['hour'].mode()[0]
    print('\n Most Popular Start Hour: ', popularHour)

    print("\nThis took %s seconds." % (time.time() - startTime))
    print('-'*40)


def stationStats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    startTime = time.time()

    # Display most commonly used start station
    popularStartStation = df['Start Station'].mode()[0]
    print('The most commonly used start station: ', popularStartStation)

    # Display most commonly used end station
    popularEndStation = df['End Station'].mode()[0]
    print('\n The most commonly used end station: ', popularEndStation)

    # Display most frequent combination of start station and end station trip
    popularCombination = df.groupby(
        ['Start Station', 'End Station']).size().idxmax()
    print('\n The most frequent combination of start station and end station trip: ',
          popularCombination)

    print("\nThis took %s seconds." % (time.time() - startTime))
    print('-'*40)


def tripDurationStats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    startTime = time.time()

    # convert the Start Time  and End column to datetime
    convertToDatetime(df, 'Start Time')
    convertToDatetime(df, 'End Time')

    # Create a column Travel Time
    df['Travel Time'] = df['End Time'] - df['Start Time']

    # Display total travel time
    sumTravel = df['Travel Time'].sum()
    print("The total travel time: ", sumTravel)

    # Display mean travel time
    meanTravel = df['Travel Time'].mean()
    print("\nThe mean travel time: ", meanTravel)

    print("\nThis took %s seconds." % (time.time() - startTime))
    print('-'*40)


def userStats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    startTime = time.time()

    # Display counts of user types
    userTypes = df['User Type'].value_counts()
    print("This is the count of each type of user: \n", userTypes)

    # Display counts of gender for New York City and Chicago
    if city != 'washington':
        gender = df['Gender'].value_counts()
        print("\nThis is the count of each gender: \n", gender)

        # Display earliest, most recent, and most common year of birth
        popularYear = df['Birth Year'].mode()[0]
        print("\nThe most common year of birth: ", popularYear)
        print("\nThe earliest year of birth:", df['Birth Year'].min())
        print("\nThe most recent year of birth:", df['Birth Year'].max())

    print("\nThis took %s seconds." % (time.time() - startTime))
    print('-'*40)


def displayData(df):
    """
    Display raw data upon request by the user

    """
    # Ask user if he/she want to see raw data
    answer = input("Do you want to see raw data?(yes or no)\n").lower()
    # Display data if answer is 'yes' and ask again if they want to see more lines
    if answer == 'yes':
        startIndex = 0
        endIndex = 6
        data = df.iloc[startIndex:endIndex]
        print(data)
        newAnswer = input("Do you want to see more 5 lines of raw data?\n").lower()
        while newAnswer != 'no':
            startIndex += 5
            endIndex += 5
            newData = df.iloc[startIndex:endIndex]
            print(newData)
            newAnswer = input("Do you want to see more 5 lines of raw data?\n").lower()


def main():
    while True:
        city, month, day = getFilters()
        df = loadData(city, month, day)

        timeStats(df)
        stationStats(df)
        tripDurationStats(df)
        userStats(df, city)
        displayData(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
