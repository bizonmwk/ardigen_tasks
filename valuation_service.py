import pandas as pd
pd.options.mode.chained_assignment = None

def read_data():
    """
    Function to load data from .csv files
    returns data, matching, currencies DataFrames
    """

    data = pd.read_csv("Files/data.csv")
    matchings = pd.read_csv("Files/matchings.csv")
    currencies = pd.read_csv("Files/currencies.csv")

    return data,matchings,currencies

def write_data(filtered_data,directory='Files/top_products.csv'):

    """
    Function to write output to .csv file
    """
    filtered_data.to_csv(directory,index=False)

def conversion(data,currencies):
    """
    Function for converting all curriences to PLN
    returns converted data DataFrame
    """

    for index,row in data.iterrows():
        if row['currency'] ==  'GBP':
            data['price'][index] = row['price'] * currencies['ratio'].loc[
                                    currencies['currency'] =='GBP']
            data['currency'].loc[index] ='PLN'
            data['total_price'] = data['price'] * data['quantity']

        elif row['currency'] == 'EU':
            data['price'][index] = row['price'] * currencies['ratio'].loc[
                                    currencies['currency'] == 'EU']
            data['currency'].loc[index] ='PLN'
            data['total_price'] = data['price'] * data['quantity']

        elif row['currency'] == 'PLN':
            data['total_price'] = data['price'] * data['quantity']

    return data

def filter(data,matchings):
    """
    Function for calculations and creating final DataFrame,
    returns filtered_data - output for saving .csv DataFrame
    """

    data = data.sort_values(by=['matching_id','total_price'],ascending=False)
    data_copy = data.copy()
    filtered_data = pd.DataFrame(columns=['ignored_products_count','currency'])

    for index,row in matchings.iterrows():
        data[data['matching_id'] == row['matching_id']] = data[
             data['matching_id']==row['matching_id']].iloc[
                                    0:row['top_priced_count']]

    filtered_data = filtered_data.reset_index(drop=True)
    filtered_data['total_price'] = data.groupby('matching_id')[
                                    'total_price'].sum()
    filtered_data['avg_price'] = data.groupby(['matching_id'])[
                                    'total_price'].mean()
    data = data.dropna()
    filtered_data['matching_id'] = filtered_data.index

    for index,row in filtered_data.iterrows():
        filtered_data['ignored_products_count'].loc[index] = len(data_copy[
                     data_copy['matching_id'] == row['matching_id']]) - len(
                     data[data['matching_id'] == row['matching_id']])

        filtered_data['currency'][index] = data['currency'][index]

    filtered_data = filtered_data.reset_index(drop=True)
    filtered_data = filtered_data[['matching_id','total_price','avg_price',
                                   'currency','ignored_products_count']]


    """If line below is commented, we will receive an error in unit tests """
    filtered_data['ignored_products_count'] = pd.to_numeric(
                                filtered_data['ignored_products_count'])

    return filtered_data

if __name__ == "__main__":
    """
    Runs all functions
    """

    data,matchings,currencies = read_data()
    converted_data = conversion(data,currencies)
    filtered_data = filter(converted_data,matchings)
    write_data(filtered_data)
