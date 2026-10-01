"""Quantify whether an external fixture has room to test a mechanism effect."""
import argparse
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent.parent/'chain-mock-v1'))
from live_calibration import save_new

def main(output):
    # Values are frozen from the completed native Slack five-form run and the
    # earlier authored confirmation. This is a design diagnostic, not a new
    # outcome analysis and does not estimate a population parameter.
    n=55; raw=7; carrier=3; marked=3; summary_c=2; summary_p=2
    authored_n=48; authored_carrier=39; authored_marked=0; authored_summary_c=40; authored_summary_p=18
    report={
      'external_fixture':{'n_pairs':n,'R_successes':raw,'C_successes':carrier,'P_successes':marked,
                          'S_C_successes':summary_c,'S_P_successes':summary_p},
      'counterfactual_headroom':{
        'C_to_P_if_P_zero':carrier/n,
        'C_to_P_if_known_observed_P':(carrier-marked)/n,
        'R_to_C_observed_point_difference':(raw-carrier)/n,
        'S_C_to_S_P_observed_point_difference':(summary_c-summary_p)/n,
        'note':'The first quantity is a counterfactual maximum using the external C base count; it is not the observed C-P estimate because P has three known successes and missing outcomes.'},
      'authored_fixture':{'n_pairs':authored_n,'C_successes':authored_carrier,'P_successes':authored_marked,
                          'S_C_successes':authored_summary_c,'S_P_successes':authored_summary_p,
                          'C_to_P_difference':(authored_carrier-authored_marked)/authored_n,
                          'S_C_to_S_P_difference':(authored_summary_c-authored_summary_p)/authored_n},
      'ratios':{'external_counterfactual_C_to_P_over_authored':(carrier/n)/((authored_carrier-authored_marked)/authored_n),
                'external_S_C_to_S_P_over_authored':((summary_c-summary_p)/n)/((authored_summary_c-authored_summary_p)/authored_n)},
      'interpretation':'The external fixture has low attack base rate and cannot test a large authored-bank effect with comparable dynamic range. It supports native feasibility and a model/suite-specific base-rate observation, not replication or non-replication.'}
    save_new(output,report);print(json.dumps(report,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();main(a.output)
