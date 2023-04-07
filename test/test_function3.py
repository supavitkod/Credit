import pandas as pd
import unittest
from function import function
from function import convert_day

class TestConvertDay(unittest.TestCase):
    def test_convert_day_to_year(self):
       # Create a test DataFrame
        df = pd.DataFrame({
            'ID':[1,2,3,4,5,6], 
            'DAYS_BIRTH' : [-3650, -3650, -3650, -3650, -3650, -3650]})
        
        # Call the function and store the result
        df['DAYS_BIRTH'] = df['DAYS_BIRTH'].apply(convert_day.convert_day_to_year)
        result = df
        # result = assess_risk.risk_assess(df)
        
        # Create a reference DataFrame with the expected output
        expected_result = pd.DataFrame({
            'ID':[1,2,3,4,5,6], 
            'DAYS_BIRTH' : [10.0, 10.0, 10.0, 10.0, 10.0, 10.0]})
        # Assert that the result is equal to the expected result
        pd.testing.assert_frame_equal(result, expected_result)