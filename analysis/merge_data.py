# CI analysis minimal example
# Step 1: Merge data from demographics and health data
# creating new data frame saved to data/alldata.csv

import os
import pandas as pd


def load_data(datadir):
    """
    Load data from file
    """
    primary_datadir = os.path.join(datadir, 'primary_data')
    demogdata = pd.read_csv(os.path.join(primary_datadir, 'demographic_health.csv'))
    taskdata = pd.read_csv(os.path.join(primary_datadir, 'meaningful_variables_clean.csv'))
    return demogdata, taskdata


def merge_data(demogdata, taskdata, datadir):
    """
    Merge data from demographics and health data
    """
    merged_data = pd.merge(demogdata, taskdata, on='participant_id')
    merged_data.to_csv(os.path.join(datadir, 'alldata.csv'), index=False)


if __name__ == "__main__":
    datadir = '../data'
    demogdata, taskdata = load_data(datadir)
    merge_data(demogdata, taskdata, datadir)
    print('Data merged and saved to data/alldata.csv')
