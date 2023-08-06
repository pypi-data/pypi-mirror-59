# -*- coding: utf-8 -*-
"""
This script creates samples using a lating Hypercube sample of 5 variables of interest.
then runs the demand calculation of CEA for all the samples. It delivers a json file storing
the results of cv_rmse and rmse for each sample.
"""

from __future__ import division
import pandas as pd
import cea
import numpy as np
from cea.demand import demand_main
from cea.demand.calibration import latin_sampler
from geopandas import GeoDataFrame as Gdf

import pickle
import json

import cea.demand.calibration.settings
import cea.inputlocator as inputlocator

__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2017, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Jimeno A. Fonseca"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"



def sampling_main(locator, config):
    """
    This script creates samples using a lating Hypercube sample of 5 variables of interest.
    then runs the demand calculation of CEA for all the samples. It delivers a json file storing
    the results of cv_rmse and rmse for each sample.

    For more details on the work behind this please check:
    Rysanek A., Fonseca A., Schlueter, A. Bayesian calibration of Dyanmic building Energy Models. Applied Energy 2017.

    :param locator: pointer to location of CEA files
    :param variables: input variables of CEA to sample. They must be 6!
    :param building_name: name of building to calibrate
    :param building_load: name of building load to calibrate
    :return:

        1. a file storing values of cv_rmse and rmse for all samples. the file is stored in
        file(locator.get_calibration_cvrmse_file(building_name)

        2 a file storing information about variables, the building_load and the probability distributions used in the
        exercise. the file is stored in locator.get_calibration_problem(building_name)

    :rtype: .json and .pkl
    """

    # Local variables

    number_samples = config.single_calibration.samples
    variables = config.single_calibration.variables
    building_name = config.single_calibration.building
    building_load = config.single_calibration.load
    override_file = Gdf.from_file(locator.get_zone_geometry()).set_index('Name')
    override_file = pd.DataFrame(index=override_file.index)

    # Generate latin hypercube samples
    latin_samples, latin_samples_norm, distributions = latin_sampler.latin_sampler(locator, number_samples, variables)

    # Run demand calulation for every latin sample
    cv_rmse_list = []
    rmse_list = []
    for i in range(number_samples):

        #create list of tuples with variables and sample
        sample = zip(variables,latin_samples[i,:])

        #create overrides and return pointer to files
        apply_sample_parameters(locator, sample, override_file)

        # run cea demand and calculate cv_rmse
        simulation = simulate_demand_sample(locator, building_name, building_load, config)

        #calculate cv_rmse
        measured = pd.read_csv(locator.get_demand_measured_file(building_name))[building_load+"_kWh"].values
        cv_rmse, rmse = calc_cv_rmse(simulation, measured)

        cv_rmse_list.append(cv_rmse)
        rmse_list.append(rmse)
        print("The cv_rmse for this iteration is:", cv_rmse)

    # Save results into json
    # Create problem and save to disk as a pickle
    problem = {'variables':variables, 'building_load':building_load, 'probabiltiy_vars':distributions,
               'samples':latin_samples, 'samples_norm':latin_samples_norm, 'cv_rmse':cv_rmse_list, 'rmse':rmse_list}
    pickle.dump(problem, open(locator.get_calibration_problem(building_name, building_load), 'w'))

def simulate_demand_sample(locator, building_name, building_load, config):
    """
    This script runs the cea demand tool in series and returns a single value of cvrmse and rmse.

    :param locator: pointer to location of files in CEA
    :param building_name: name of building
    :param output_parameters: building load to consider in the anlysis
    :return:
    """

    # force simulation to be sequential, for only one building and to override variables
    config.demand.override_variables = True # true so it reads the overrides file created
    config.multiprocessing = False
    config.demand.buildings = [building_name]
    config.demand.resolution_output = "hourly"
    config.demand.loads_output = [building_load]
    config.demand.massflows_output = ["mcphs_sys"] # give one entry so it doe snot plot all ( it saves memory)
    config.demand.temperatures_output = ["Tww_sys_sup"] # give one entry so it doe snot plot all ( it saves memory)
    config.demand.format_output = "csv"

    _ , time_series = demand_main.demand_calculation(locator, config)
    return time_series[0][building_load+"_kWh"].values

def calc_cv_rmse(prediction, target):
    """
    This function calculates the covariance of the root square mean error between two vectors.
    :param prediction: vector of predicted/simulated data
    :param target: vector of target/measured data
    :return:

        - CVrmse: float
        - rmse: float

    """

    delta = (prediction - target)**2
    sum_delta = delta.sum()
    if sum_delta > 0:
        mean = target.mean()
        n = len(prediction)
        rmse = np.sqrt((sum_delta/n))
        CVrmse = rmse/mean
    else:
        rmse = 0
        CVrmse = 0
    return round(CVrmse,3), round(rmse,3) #keep only 3 significant digits


def apply_sample_parameters(locator, sample, override_file):
    """
    This script structures samples in a format that can be read by a case study in cea.

    :param locator: pointer to location of CEA files
    :param sample: array with values of m variables to modify in the input databases of CEA
    :return: file with variables to overwrite in cea and stored in locator.get_building_overrides()
    """

    # make overides
    for (variable, value) in sample:
        print("Setting prop_overrides['%s'] to %s" % (variable, value))
        override_file[variable] = value
    override_file.to_csv(locator.get_building_overrides())

def main(config):

    locator = cea.inputlocator.InputLocator(scenario=config.scenario)
    print('Running single building sampler for scenario %s' % config.scenario)
    print('Running single building sampler with dynamic infiltration=%s' %
          config.demand.use_dynamic_infiltration_calculation)
    print('Running single building sampler with multiprocessing=%s' % config.multiprocessing)
    print('Running single building sampler for the next input variables =%s' % config.single_calibration.variables)
    print('Running single building sampler for the next building =%s' % config.single_calibration.building)
    print('Running single building sampler for the next output variable=%s' % config.single_calibration.load)

    sampling_main(locator=locator, config=config)

if __name__ == '__main__':
    main(cea.config.Configuration())