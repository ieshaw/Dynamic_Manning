import pandas as pd
import unittest

from check import X_check
from mip import mip

class Test_MIP(unittest.TestCase):

    def test_two_by_two_easy(self):
        S_df = pd.DataFrame([[1,2],[2,1]], 
                index=['F_1', 'F_2'], columns=['S_1', 'S_2'])
        O_df = pd.DataFrame([[1,2],[2,1]], 
                index=['S_1', 'S_2'], columns=['F_1', 'F_2'], )
        A_df = pd.DataFrame([[1],[1]], 
                index=['F_1', 'F_2'], columns=['Num_Positions'])
        X_df = pd.DataFrame([[1,0],[0,1]], 
                index=['F_1', 'F_2'], columns=['S_1', 'S_2'])
        X_mip = mip(S_df, O_df, A_df, print_to_screen=False)
        diff_df = X_mip - X_df
        self.assertEqual(0,diff_df.min().min())
        self.assertEqual(0,diff_df.max().max())

    def test_two_by_two_seeker_compete(self):
        S_df = pd.DataFrame([[1,1],[2,2]], 
                index=['F_1', 'F_2'], columns=['S_1', 'S_2'])
        O_df = pd.DataFrame([[1,2],[2,1]], 
                index=['S_1', 'S_2'], columns=['F_1', 'F_2'], )
        A_df = pd.DataFrame([[1],[1]], 
                index=['F_1', 'F_2'], columns=['Num_Positions'])
        X_df = pd.DataFrame([[1,0],[0,1]], 
                index=['F_1', 'F_2'], columns=['S_1', 'S_2'])
        X_mip = mip(S_df, O_df, A_df, print_to_screen=False)
        diff_df = X_mip - X_df
        self.assertEqual(0,diff_df.min().min())
        self.assertEqual(0,diff_df.max().max())

    def test_two_by_two_owner_compete(self):
        S_df = pd.DataFrame([[1,2],[2,1]], 
                index=['F_1', 'F_2'], columns=['S_1', 'S_2'])
        O_df = pd.DataFrame([[1,1],[2,2]], 
                index=['S_1', 'S_2'], columns=['F_1', 'F_2'], )
        A_df = pd.DataFrame([[1],[1]], 
                index=['F_1', 'F_2'], columns=['Num_Positions'])
        X_df = pd.DataFrame([[1,0],[0,1]], 
                index=['F_1', 'F_2'], columns=['S_1', 'S_2'])
        X_mip = mip(S_df, O_df, A_df, print_to_screen=False)
        diff_df = X_mip - X_df
        self.assertEqual(0,diff_df.min().min())
        self.assertEqual(0,diff_df.max().max())

    def test_three_by_two_seeker_unmatched(self):
        S_df = pd.DataFrame([[1,2, 1],[2,1,2]], 
                index=['F_1', 'F_2'], columns=['S_1', 'S_2', 'S_3'])
        O_df = pd.DataFrame([[1,1],[2,2], [3,3]], 
                index=['S_1', 'S_2', 'S_3'], columns=['F_1', 'F_2'], )
        A_df = pd.DataFrame([[1],[1]], 
                index=['F_1', 'F_2'], columns=['Num_Positions'])
        X_df = pd.DataFrame([[1,0, 0],[0,1,0]], 
                index=['F_1', 'F_2'], columns=['S_1', 'S_2','S_3'])
        X_mip = mip(S_df, O_df, A_df, print_to_screen=False)
        diff_df = X_mip - X_df
        self.assertEqual(0,diff_df.min().min())
        self.assertEqual(0,diff_df.max().max())

    def test_two_by_three_owner_unmatched(self):
        S_df = pd.DataFrame([[1,2],[2,1],[3,3]], 
                index=['F_1', 'F_2', 'F_3'], columns=['S_1', 'S_2'])
        O_df = pd.DataFrame([[1,1,1],[2,2,2]], 
                index=['S_1', 'S_2'], columns=['F_1', 'F_2', 'F_3'], )
        A_df = pd.DataFrame([[1],[1],[1]], 
                index=['F_1', 'F_2', 'F_3'], columns=['Num_Positions'])
        X_df = pd.DataFrame([[1,0],[0,1],[0,0]], 
                index=['F_1', 'F_2', 'F_3'], columns=['S_1', 'S_2'])
        X_mip = mip(S_df, O_df, A_df, print_to_screen=False)
        diff_df = X_mip - X_df
        self.assertEqual(0,diff_df.min().min())
        self.assertEqual(0,diff_df.max().max())

    def test_three_by_three_owner_unmatched(self):
        S_df = pd.DataFrame([[1,1,2],[2,2,1],[3,3,3]], 
                index=['F_1', 'F_2', 'F_3'], columns=['S_1', 'S_2', 'S_3'])
        O_df = pd.DataFrame([[1,1,1],[2,2,2],[3,3,3]], 
                index=['S_1', 'S_2', 'S_3'], columns=['F_1', 'F_2', 'F_3'], )
        A_df = pd.DataFrame([[2],[1],[1]], 
                index=['F_1', 'F_2', 'F_3'], columns=['Num_Positions'])
        X_df = pd.DataFrame([[1,1,0],[0,0,1],[0,0,0]], 
                index=['F_1', 'F_2', 'F_3'], columns=['S_1', 'S_2', 'S_3'])
        X_mip = mip(S_df, O_df, A_df, print_to_screen=False)
        print(X_mip)
        print(X_df)
        diff_df = X_mip - X_df
        self.assertEqual(0,diff_df.min().min())
        self.assertEqual(0,diff_df.max().max())

class Test_X_Check(unittest.TestCase):

    def test_firm_over_assignment(self):
        X_df = pd.DataFrame([[1,1],[0,0]], 
                index=['F_1', 'F_2'], columns=['S_1', 'S_2'])
        A_df = pd.DataFrame([[1],[1]], 
                index=['F_1', 'F_2'], columns=['Num_Positions'])
        with self.assertRaises(ValueError) as cm:
            X_check(X_df,A_df)

    def test_seeker_multiple_assignment(self):
        X_df = pd.DataFrame([[1,1],[1,0]], 
                index=['F_1', 'F_2'], columns=['S_1', 'S_2'])
        A_df = pd.DataFrame([[2],[1]], 
                index=['F_1', 'F_2'], columns=['Num_Positions'])
        with self.assertRaises(ValueError) as cm:
            X_check(X_df,A_df)

    def test_X_binary(self):
        X_df = pd.DataFrame([[1,-1],[0,1]], 
                index=['F_1', 'F_2'], columns=['S_1', 'S_2'])
        A_df = pd.DataFrame([[1],[1]], 
                index=['F_1', 'F_2'], columns=['Num_Positions'])
        with self.assertRaises(ValueError) as cm:
            X_check(X_df,A_df)

    def test_min_assignment(self):
        X_df = pd.DataFrame([[1,0,0],[0,1,0]], 
                index=['F_1', 'F_2'], columns=['S_1', 'S_2', 'S_3'])
        A_df = pd.DataFrame([[2],[1]], 
                index=['F_1', 'F_2'], columns=['Num_Positions'])
        with self.assertRaises(ValueError) as cm:
            X_check(X_df,A_df)
