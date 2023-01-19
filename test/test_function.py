import pandas as pd
import unittest
from function import function

class TestSelectFirstMonth(unittest.TestCase):
    def test_select_first_month(self):
        # Create a test DataFrame
        df = pd.DataFrame({
            'ID':[1,1,1,3,3,4,4], 
            'MONTHS_BALANCE' : [0, -1, -2, 0, -1, 0,-1], 
            'STATUS' : ['X', 0, 0, 'C', 1, 'X', 1]})
        
        # Call the function and store the result
        result = function.select_first_month(df)
        
        # Create a reference DataFrame with the expected output
        expected_result = pd.DataFrame({
            'ID':[1,3,4], 
            'MONTHS_BALANCE' : [-2, -1, -1], 
            'STATUS' : [0, 1, 1]})
        
        # Assert that the result is equal to the expected result
        pd.testing.assert_frame_equal(result, expected_result)