import pandas as pd
import valuation_service

from pandas._testing import assert_frame_equal

def test_read_data():
    """
    Unit tests of pandas read functions
    *_r DataFrames - read with pandas function
    *_c DataFrames - created for purpose of tests
    """
    test_data_r = pd.read_csv('Test_files/test_data.csv')
    test_data_c = pd.DataFrame({'id':[1,2,3,4],
                                'price':[8000,950,2400,1150],
                                'currency':['PLN','GBP','PLN','EU'],
                                'quantity':[6,1,1,2],
                                'matching_id':[1,3,2,2,]})

    assert_frame_equal(test_data_r, test_data_c)

    test_matching_r= pd.read_csv('Test_files/test_matching.csv')
    test_matching_c = pd.DataFrame({'matching_id':[1,2,3],
                                    'top_priced_count':[1,2,1]})

    assert_frame_equal(test_matching_r,test_matching_c)

    test_currencies_r = pd.read_csv('Test_files/test_currencies.csv')
    test_currencies_c = pd.DataFrame({'currency':['GBP','EU','PLN'],
                                      'ratio':[2.6,2.2,1]})

    assert_frame_equal(test_currencies_r,test_currencies_c)

    return test_data_r,test_matching_r,test_currencies_r

def test_conversion(test_data,test_currencies):
    """
    Unit test of created, 'conversion' function.
    test_data_f - data from created function
    test_data_c - created for purpose of test, DataFrame
    """
    test_data_f = valuation_service.conversion(test_data,test_currencies)
    test_data_c = pd.DataFrame({'id':[1,2,3,4],
                                'price':[8000,2470,2400,2530],
                                'currency':['PLN','PLN','PLN','PLN'],
                                'quantity':[6,1,1,2],
                                'matching_id':[1,3,2,2,],
                                'total_price':[48000,2470,2400,5060]})

    assert_frame_equal(test_data_f,test_data_c)

    return test_data_f

def test_filter(test_converted_data,test_matching):
    """
    Unit test of created, 'filter' function.
    test_filtered_data_f - DataFrame from created functions
    test_filtered_data_c - created for purpose of test, DataFrame
    """
    test_filtered_data_f = valuation_service.filter(
                            test_converted_data,test_matching)
    test_filtered_data_c = pd.DataFrame({'matching_id':[1,2,3],
                                         'total_price':[48000,7460,2470],
                                         'avg_price':[48000,3730,2470],
                                         'currency':['PLN','PLN','PLN'],
                                         'ignored_products_count':[0,0,0]})

    assert_frame_equal(test_filtered_data_f,test_filtered_data_c)

    return test_filtered_data_f

def test_write(test_filtered_data):
    """
    Test of pandas write to csv function.
    test_data_r - DataFrame read with pandas function
    test_filtered_data - DataFrame from created functions
    """
    valuation_service.write_data(test_filtered_data,directory='Test_files/test_top_products.csv')

    test_data_r = pd.read_csv('Test_files/test_top_products.csv')

    assert_frame_equal(test_data_r,test_filtered_data)

if __name__ == "__main__":
    """
    Runs all created tests
    """
    test_data,test_matching,test_currencies = test_read_data()
    test_converted_data= test_conversion(test_data,test_currencies)
    test_filtered_data = test_filter(test_converted_data,test_matching)
    test_write(test_filtered_data)