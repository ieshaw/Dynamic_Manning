import numpy as np
import pandas as pd
import unittest

from check import X_check
from mip import mip
from post_match import mu_metrics,top_perc

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

class Test_Post_Match(unittest.TestCase):

    def setUp(self):
        self.O_dict = {'O_1':2, 'O_2':1, 'O_3':1, 'O_4':1,'O_5':1, 'O_6':1}
        self.S_list = ['S_{}'.format(i) for i in range(1,7)]
        self.X_df = pd.DataFrame([[1,1,0,0,0,0],
                                    [0,0,1,0,0,0],
                                    [0,0,0,1,0,0],
                                    [0,0,0,0,1,0],
                                    [0,0,0,0,0,1],
                                    [0,0,0,0,0,0]], index=list(self.O_dict.keys()),
                                    columns = self.S_list)
        pref = np.ones((6,6),dtype=int)
        for i in range(1,6):
            pref[i,:] += i
        self.S_df = pd.DataFrame(pref, index=list(self.O_dict.keys()),
                                    columns = self.S_list)
        self.O_df = pd.DataFrame(pref, index= self.S_list,
                        columns=list(self.O_dict.keys()))
        self.A_df = pd.DataFrame.from_dict(self.O_dict, orient='index', 
                columns=['Num_Positions'])
        self.A_df.index.name='Job'

    def test_s_top_perc(self):
        top_dict = top_perc(self.S_df,'s',self.X_df)
        test_dict = {'s_participants': 6, 
                's_matched_count': 6.0, 
                's_matched_ratio': 1,
                's_unmatched_count': 0, 
                's_unmatched_ratio': 0, 
                '1_s_count': 2,
                '1_s_ratio': round(float(2)/float(6),4),
                '5_s_count': 6, 
                '5_s_ratio': 1,
                '10_s_count': 6,
                '10_s_ratio': 1}
        for key in test_dict:
            self.assertEqual(top_dict[key],test_dict[key])

    def test_o_top_perc(self):
        top_dict = top_perc(self.O_df,'o',self.X_df,self.A_df)
        test_dict = {'o_participants': 7, 
                'o_matched_count': 6.0, 
                'o_matched_ratio': round(float(6)/float(7),4),
                'o_unmatched_count': 1, 
                'o_unmatched_ratio': round(float(1)/float(7),4), 
                '1_o_count': 1,
                '1_o_ratio': round(float(1)/float(7),4),
                '5_o_count': 5, 
                '5_o_ratio': round(float(5)/float(7),4),
                '10_o_count': 6,
                '10_o_ratio': round(float(6)/float(7),4),}
        for key in test_dict:
            self.assertEqual(top_dict[key],test_dict[key])

    def test_mu_metrics(self):
        mu_s,mu_o = mu_metrics(self.S_df,self.O_df,self.X_df)
        self.assertEqual(mu_s,round(float(16)/float(6),4))
        self.assertEqual(mu_o,round(float(21)/float(6),4))
