# run functions for merge
import os
from merge_data import load_data, merge_data
from arrest_analysis import model_arrest, load_alldata, select_variables, save_output


def test_merge():
    datadir = 'data'
    demogdata, taskdata = load_data(datadir)
    merge_data(demogdata, taskdata, datadir)
    assert os.path.exists(os.path.join(datadir, 'alldata.csv'))


def test_analysis():
    datadir = 'data'
    resultsdir= 'results'
    alldata = load_alldata(datadir)
    arrestdata = select_variables(alldata)

    log_reg, log_reg_baseline = model_arrest(arrestdata)

    assert log_reg is not None
    assert log_reg_baseline is not None
    
    save_output(log_reg, log_reg_baseline, resultsdir)
