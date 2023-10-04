import pandas as pd
import numpy as np
import subprocess

# Load the CSV file
file_path = "Assignment_Timecard.xlsx - Sheet1.csv"
df = pd.read_csv(file_path)
df['Pay Cycle Start Date'] = pd.to_datetime(df['Pay Cycle Start Date'])


# Function to find employees who worked 7 consecutive days
def find_consecutive_day_workers(df):
    print("Employees who worked for 7 consecutive days: ")

    # Sort the DataFrame by employee name and pay cycle start date
    df = df.sort_values(by=['Employee Name', 'Pay Cycle Start Date'])

    # Group the data by employee name
    grouped = df.groupby('Employee Name')

    for name, group in grouped:
        # Calculate the difference between consecutive pay cycle start dates
        group['day_diff'] = group['Pay Cycle Start Date'].diff().dt.days
        consecutive_days = group['day_diff'].eq(1).sum()

        # Check if an employee worked 7 consecutive days
        if consecutive_days >= 7:
            print(name, group['Position ID'].iloc[0])


# Function to find employees with shifts too close together
def find_close_shifts(df):
    print("\nEmployees with <10 hours between shifts:")

    # Sort the DataFrame by employee name and pay cycle start date
    df = df.sort_values(by=['Employee Name', 'Pay Cycle Start Date'])

    # Calculate the time difference between consecutive shifts in hours
    diff = df['Pay Cycle Start Date'].diff()

    # Filter employees with shifts less than 10 hours apart but greater than 1 hour
    close_shifts = df[(diff.dt.components['hours'] < 10) &
                      (diff.dt.components['hours'] > 1)]

    # Print the names and positions of employees
    for name, group in close_shifts.groupby('Employee Name'):
        print(name, group['Position ID'].iloc[0])


# Function to find employees who worked >14 hours in one shift
def find_long_shifts(df):
    print("\nEmployees who worked >14 hours in one shift:")

    # Convert time strings to total hours
    df['Timecard Hours (as Time)'] = df['Timecard Hours (as Time)'].apply(
        time_to_hours)

    # Filter employees who worked more than 14 hours in a single shift
    long_shifts = df[df['Timecard Hours (as Time)'] > 14]

    # Print the names and positions of employees
    for name, group in long_shifts.groupby('Employee Name'):
        print(name, group['Position ID'].iloc[0])


# Function to convert time strings to total hours
def time_to_hours(time_str):
    if pd.notna(time_str) and ':' in time_str:
        hours, minutes = map(int, time_str.split(':'))
        return hours + minutes / 60.0
    else:
        return np.nan


# Call the functions to find and print the desired information
find_consecutive_day_workers(df)
find_close_shifts(df)
find_long_shifts(df)

with open("output.txt", "wb") as f:
    subprocess.check_call(["python", "main.py"], stdout=f)
