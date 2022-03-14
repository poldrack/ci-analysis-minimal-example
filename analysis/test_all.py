# run functions for merge
import os
import pytest
from merge_data import load_data, merge_data
from arrest_analysis import model_arrest, load_alldata, select_variables, save_output

@pytest.fixture
def alldata():
    datadir = 'data'
    demogdata, taskdata = load_data(datadir)
    alldata = merge_data(demogdata, taskdata, datadir)
    return alldata


def test_analysis(alldata):
    resultsdir = 'results'
    if not os.path.exists(resultsdir):
        os.mkdir(resultsdir)
    
    arrestdata = select_variables(alldata)

    log_reg, log_reg_baseline = model_arrest(arrestdata)

    assert log_reg is not None
    assert log_reg_baseline is not None

    save_output(log_reg, log_reg_baseline, resultsdir)
