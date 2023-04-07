import pandas as pd
import unittest
from function import function
from function import assess_risk

class TestAssessRisk(unittest.TestCase):
    def test_assess_risk(self):
        # Create a test DataFrame
        df = pd.DataFrame({
            'ID':[1,2,3,4,5,6], 
            'STATUS' : [0, 1, 2, 3, 4, 5]})
        
        # Call the function and store the result
        df['STATUS'] = df['STATUS'].apply(assess_risk.risk_assess)
        result = df
        # result = assess_risk.risk_assess(df)
        
        # Create a reference DataFrame with the expected output
        expected_result = pd.DataFrame({
            'ID':[1,2,3,4,5,6], 
            'STATUS' : [0, 1, 1, 1, 1, 1]})
        
        # Assert that the result is equal to the expected result
        pd.testing.assert_frame_equal(result, expected_result)