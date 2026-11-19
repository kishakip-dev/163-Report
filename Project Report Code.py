# Kisha Kiprop
# CSE 163 AE
# Creates visualizations for the California County Report
# based on the research questions
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def main():
    # reads data from the excel file and prints the column names
    california_data = pd.read_excel('data.xls')
    print(f"Total number of families in the dataset: {len(california_data)}")

    # drops any rows with missing values
    california_data =california_data.dropna().reset_index(drop=True)
    print(f"Total number of families in the dataset after dropping missing values: {len(california_data)}\n")

    # groups the data by county and calculates the average cost per year, median income, and average family size for each county
    county_spending = california_data.groupby("county_name")["cost_yr"].mean().reset_index()
    county_salary = california_data.groupby("county_name")["median_income"].mean().reset_index()
    county_family_size = california_data.groupby("county_name")["ave_fam_size"].mean().reset_index()

    # prints the seven number summary for the cost_yr column
    seven_number_summary(county_spending, "cost_yr")
    print()

    # prints the seven number summary for the median_income column
    seven_number_summary(county_salary, "median_income")
    print()

    # prints the seven number summary for the average family size column
    seven_number_summary(county_family_size, "ave_fam_size")
    print()

    # prints each unique county name in the dataset
    print(f"\nThe {len(county_spending)} unique county names in the dataset are: {county_spending['county_name'].tolist()}")

    # merges the three dataframes on the county_name column to create a new dataframe with all the relevant information for each county
    county_joined = pd.merge(county_spending, county_salary, on="county_name")
    county_joined = pd.merge(county_joined, county_family_size, on="county_name")

    avg_cost_per_year_by_county(county_joined)

    # Creates a new column in the county_joined dataframe that calculates 
    # the ratio of median income to cost per year for each county
    salary_vs_cost(county_joined)

    individual_affordability(california_data)


def seven_number_summary(data, column_name):
    # Calculates the seven number summary for a given column in a dataframe
    stats = {
        "mean": data[column_name].mean(),
        "median": data[column_name].median(),
        "minimum": data[column_name].min(),
        "maximum": data[column_name].max(),
        "first_quartile": data[column_name].quantile(0.25),
        "third_quartile": data[column_name].quantile(0.75),
        "std_dev": data[column_name].std()
    }

    print(f"Seven number summary for {column_name}:")
    for key, value in stats.items():
        print(f"{key}: {value}")


def avg_cost_per_year_by_county(county_joined):
    # Creates a bar chart showing the average cost per year by county
    # saves the chart as a PNG file
    fig, ax = plt.subplots(figsize=(18, 10))

    county_joined.plot(kind='bar', x='county_name', y='cost_yr', ax=ax, legend=False)
    ax.set_title('Average Cost per Year by County')
    ax.set_xlabel('County')
    ax.set_ylabel('Average Cost per Year')
    plt.xticks(rotation=45)
    plt.tight_layout()  
    plt.savefig('average_cost_per_year_by_county.png')


def salary_vs_cost(data):
    # Creates a new column in a dataframe that calculates the ratio of median
    # income to cost per year for each county
    ratio = (data['median_income'] - data['cost_yr']) / data['median_income'] * 100

    data['ratio'] = ratio


def individual_affordability(data):
    # Creates a new column in a dataframe that calculates the ratio of median
    # income to cost per year for each county
    # Creates a bar chart showing the number of families that spend more than 50% of their salary on food
    salary_vs_cost(data)

    data['more_than_50_percent'] = data['ratio'] > 50

    affordability_counts = {
        'Less than 50% of salary': len(data[data['more_than_50_percent'] == True]),
        'More than 50% of salary': len(data[data['more_than_50_percent'] == False])
    }

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x=list(affordability_counts.keys()),
        y=list(affordability_counts.values()),
        ax=ax, 
        hue=['#FF9999', '#99FF99']
    )
    ax.set_title('Families Spending More Than 50% of Salary on Food')
    ax.set_xlabel('')
    ax.set_ylabel('Number of Families')
    plt.tight_layout()
    plt.savefig('individual_affordability.png')


#def result_validity(data):

if __name__ == "__main__":
    main()
