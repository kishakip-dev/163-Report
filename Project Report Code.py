# Kisha Kiprop
# CSE 163 AE
# Creates visualizations for the California Food Affordability
# with columns of interest (cost_yr, median_income, county_name,
# ave_fam_size)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def main():
    # reads data from the excel file and prints the column names
    california_data = pd.read_excel('data.xls')
    print(f"Total number of families in the dataset: {len(california_data)}")

    # groups the data by county and calculates the average cost per year,
    # median income, and average family size for each county
    county_spending = california_data.groupby(
        "county_name")["cost_yr"].mean().reset_index()
    county_salary = california_data.groupby(
        "county_name")["median_income"].mean().reset_index()
    county_family_size = california_data.groupby(
        "county_name")["ave_fam_size"].mean().reset_index()

    # merges the three dataframes on the county_name column to create a
    # new dataframe with all the relevant information for each county
    county_joined = pd.merge(county_spending,
                             county_salary,
                             on="county_name")

    county_joined = pd.merge(county_joined,
                             county_family_size,
                             on="county_name")

    # drops any rows with missing values and resets the index of the dataframe
    county_joined = county_joined.dropna().reset_index(drop=True)

    # prints the seven number summary for the cost_yr column
    seven_number_summary(county_joined, "cost_yr")
    print()

    # prints the seven number summary for the median_income column
    seven_number_summary(county_joined, "median_income")
    print()

    # prints the seven number summary for the average family size column
    seven_number_summary(county_joined, "ave_fam_size")
    print()

    # prints each unique county name in the dataset
    print(
        f"\nThe {
            len(county_joined)} unique county names in the dataset are: {
            county_joined['county_name'].tolist()}")
    avg_cost_per_year_by_county(county_joined)

    # Creates a new column in the county_joined dataframe that calculates
    # the ratio of median income to cost per year for each county
    salary_vs_cost(county_joined)

    individual_affordability(california_data)
    result_validity(california_data)
    print()

    test_seven_number_summary()
    test_salary_vs_cost()


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

    return stats


def avg_cost_per_year_by_county(county_joined):
    # Creates a bar chart showing the average cost per year by county
    # saves the chart as a PNG file
    fig, ax = plt.subplots(figsize=(18, 10))

    county_joined.plot(kind='bar',
                       x='county_name',
                       y='cost_yr',
                       ax=ax,
                       legend=False)
    ax.set_title('Average Cost per Year by County')
    ax.set_xlabel('County')
    ax.set_ylabel('Average Cost per Year')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('average_cost_per_year_by_county.png')


def salary_vs_cost(data):
    # Creates a new column in a dataframe that calculates the ratio of median
    # income to cost per year for each county
    df_no_nan = data.dropna(subset=['median_income', 'cost_yr'])
    ratio = (df_no_nan['median_income'] -
             df_no_nan['cost_yr']) / df_no_nan['median_income'] * 100

    data['ratio'] = ratio


def individual_affordability(data):
    # Creates a new column in a dataframe that calculates the ratio of median
    # income to cost per year for each county
    # Creates a bar chart showing the number of families that
    # spend more than 50% of their salary on food
    salary_vs_cost(data)
    data = data.dropna(subset=['ratio'])
    data['more_than_50_percent'] = data['ratio'] > 50

    affordability_counts = {
        'More than 50% left':
        int(len(data[data['more_than_50_percent']])),
        '50% or less left':
        int(len(data[~data['more_than_50_percent']]))
        }

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x=list(affordability_counts.keys()),
        y=list(affordability_counts.values()),
        ax=ax,
        hue=['#FF9999', '#99FF99'],
        legend=False
    )
    ax.set_title(
        'How Much of Families\' Salaries are Left After Paying for Food'
        )
    ax.set_xlabel('')
    ax.set_ylabel('Number of Families')
    plt.tight_layout()
    plt.savefig('family_affordability.png')


def result_validity(data):
    # Test whether less than half of families have
    # over 50% of income left.
    # Under the null, each family has a 50% chance
    # of being above the threshold.
    salary_vs_cost(data)

    ratios = data['ratio'].to_numpy(dtype=float)
    valid_ratios = ratios[np.isfinite(ratios)]
    sample_size = valid_ratios.size

    successes = int(np.count_nonzero(valid_ratios > 50))
    simulation_count = 10000
    simulated_successes = np.random.binomial(
        n=sample_size,
        p=0.5,
        size=simulation_count
    )
    p_value = np.count_nonzero(simulated_successes <=
                               successes) / simulation_count
    alpha = 0.05
    reject_null = p_value < alpha

    print("\nAffordability hypothesis test:")
    print("H0: At least half of families have more than 50% of income left.")
    print("Ha: Fewer than half of families have more than 50% of income left.")
    print(f"Families above 50%: {successes} of {sample_size}")
    print(f"Estimated one-sided p-value from {
        simulation_count} simulations: {p_value:.4f}")
    if reject_null:
        print(f"Reject H0 at alpha = {alpha}: evidence supports Ha.")
    else:
        print(f"Fail to reject H0 at alpha = {alpha}; this does not prove H0.")

    return {
        'sample_size': sample_size,
        'successes': successes,
        'p_value': p_value,
        'alpha': alpha,
        'simulations': simulation_count,
        'reject_null': reject_null
    }


def test_seven_number_summary():
    # Test the seven_number_summary function with a sample dataframe
    test_data = pd.DataFrame({
        'cost_yr': [1000, 2000, 3000, 4000, 5000]
    })
    test_summary = seven_number_summary(test_data, 'cost_yr')
    assert test_summary['mean'] == 3000


def test_salary_vs_cost():
    # Test the salary_vs_cost function with a sample dataframe
    test_data = pd.DataFrame({
        'median_income': [50000, 60000, 70000],
        'cost_yr': [20000, 25000, 30000]
    })
    salary_vs_cost(test_data)
    expected_ratios = [((50000 - 20000) / 50000 * 100),
                       ((60000 - 25000) / 60000 * 100),
                       ((70000 - 30000) / 70000 * 100)]
    assert (test_data['ratio'].tolist() == expected_ratios)


if __name__ == "__main__":
    main()
