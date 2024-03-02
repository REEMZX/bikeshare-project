import time
import pandas as pd
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}
def get_filters():
    """
    Asks user to specify city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some data.")

    # Get user input for city
    while True:
        city = input("Enter the name of the city (Chicago, New York City, Washington): ").lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print("Invalid city name. Please try again.")

    # Get user input for month
    while True:
        month = input("Enter the month to filter by (January, February, ..., June), or 'all' for no filter: ").lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            print("Invalid month. Please try again.")

    # Get user input for day
    while True:
        day = input("Enter the day of the week to filter by (Monday, Tuesday, ..., Sunday), or 'all' for no filter: ").lower()
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            break
        else:
            print("Invalid day. Please try again.")

    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load data file into a DataFrame
    filename = CITY_DATA[city]
    df = pd.read_csv(filename)

    # Convert the "Start Time" column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month, day, and hour from the Start Time column to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour

    # Filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['Month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        df = df[df['Day of Week'] == day.title()]

    return df

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    common_month = df['Month'].mode()[0]
    print(f"The most common month: {common_month}")

    # Display the most common day of week
    common_day = df['Day of Week'].mode()[0]
    print(f"The most common day of the week: {common_day}")

    # Display the most common start hour
    common_hour = df['Hour'].mode()[0]
    print(f"The most common start hour: {common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def station_stats(df):
    """
    Displays statistics on the most popular stations and trips.
    """
    print('\nCalculating The Most Popular Stations and Trips...\n')
    start_time = time.time()

    # Display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station: {common_start_station}")

    # Display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f"The most commonly used end station: {common_end_station}")

    # Display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
    common_trip = df['Trip'].mode()[0]
    print(f"The most frequent combination of start station and end station trip: {common_trip}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total travel time: {total_travel_time} seconds")

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"Mean travel time: {mean_travel_time} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

    
def user_stats(df):
    """
    Displays statistics on bikeshare users.
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display user types
    user_types = df['User Type'].value_counts()
    print("Counts of each user type:")
    print(user_types)

    # Display gender distribution (if applicable)
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of each gender:")
        print(gender_counts)
    else:
        print("\nGender information is not available.")

    # Display earliest, most recent, and most common year of birth (if applicable)
    if 'Birth Year' in df:
        earliest_birth_year = int(df['Birth Year'].min())
        print(f"\nEarliest birth year: {earliest_birth_year}")
        most_recent_birth_year = int(df['Birth Year'].max())
        print(f"Most recent birth year: {most_recent_birth_year}")
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print(f"Most common birth year: {most_common_birth_year}")
    else:
        print("\nBirth year information is not available.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)
    
def display_data(df):
    """
    Displays raw data 5 rows at a time, upon user request.

    Args:
        df - Pandas DataFrame to display
    """
    start_index = 0
    while True:
        view_data = input("Would you like to view 5 rows of raw data? Enter 'yes' or 'no': ").lower()
        if view_data == 'yes':
            print(df.iloc[start_index:start_index + 5])
            start_index += 5
        elif view_data == 'no':
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def main():
    # Loop to repeatedly prompt the user for city, month, and day filters
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # Perform various statistical analyses on the data
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Display raw data if requested
        display_data(df)
        
        # Prompt the user if they want to restart or exit the program
        restart = input('\nWould you like to restart? Enter \'yes\' or \'no\'.\n')
        
        # Validate user input for restart prompt
        while restart.lower() not in ['yes', 'no']:
            print("Invalid input. Please enter either 'yes' or 'no'.")
            restart = input('\nWould you like to restart? Enter \'yes\' or \'no\'.\n')
        
        # Break the loop and exit the program if user does not want to restart
        if restart.lower() != 'yes':
            break

        #restart = input('\nWould you like to restart? Enter \'yes\' or \'no\'.\n')
        #if restart.lower() != 'yes':
            #break

if __name__ == "__main__":
    main()