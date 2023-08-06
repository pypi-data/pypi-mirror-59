from __future__ import division
from __future__ import print_function

import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot
import cea.plots.thermal_networks
from cea.plots.variable_naming import NAMING, LOGO, COLOR

__author__ = "Lennart Rogenhofer"
__copyright__ = "Copyright 2018, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Lennart Rogenhofer"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"


class EnergyLossBarPlot(cea.plots.thermal_networks.ThermalNetworksPlotBase):
    """Implement the Thermal losses and pumping requirements per pipe plot"""
    name = "Thermal losses and pumping requirements per pipe"

    def __init__(self, project, parameters, cache):
        super(EnergyLossBarPlot, self).__init__(project, parameters, cache)
        self.network_args = [self.network_type, self.network_name]
        self.input_files = [(self.locator.get_thermal_network_layout_ploss_system_edges_file, self.network_args),
                            (self.locator.get_thermal_network_qloss_system_file, self.network_args)]

    @property
    def layout(self):
        return go.Layout(barmode='stack',
                         yaxis=dict(title='Energy [kWh/yr]'),
                         xaxis=dict(title='Name'))

    def calc_graph(self):
        # calculate graph
        graph = []
        # format demand values
        P_loss_kWh = self.P_loss_kWh.fillna(value=0)
        P_loss_kWh = pd.DataFrame(P_loss_kWh.sum(axis=0), columns=['P_loss_kWh'])
        Q_loss_kWh = abs(self.Q_loss_kWh.fillna(value=0))
        Q_loss_kWh = pd.DataFrame(Q_loss_kWh.sum(axis=0), columns=['Q_loss_kWh'])
        # calculate total_df
        total_df = pd.DataFrame(P_loss_kWh.values + Q_loss_kWh.values, index=Q_loss_kWh.index, columns=['total'])
        # join dataframes
        merged_df = P_loss_kWh.join(Q_loss_kWh).join(total_df)
        merged_df = merged_df.sort_values(by='total',
                                          ascending=False)  # this will get the maximum value to the left

        # iterate through P_loss_kWh to plot
        for field in ['P_loss_kWh', 'Q_loss_kWh']:
            total_percent = (merged_df[field] / merged_df['total'] * 100).round(2)
            total_percent_txt = ["(" + str(x) + " %)" for x in total_percent]
            trace = go.Bar(x=merged_df.index, y=merged_df[field].values, name=NAMING[field],
                           text=total_percent_txt,
                           orientation='v',
                           marker=dict(color=COLOR[field]))
            graph.append(trace)
        return graph

    def calc_table(self):
        P_loss_kWh = self.P_loss_kWh.fillna(value=0)
        P_loss_kWh = pd.DataFrame(P_loss_kWh.sum(axis=0), columns=['P_loss_kWh'])  # format individual loss data
        Q_loss_kWh = abs(self.Q_loss_kWh).fillna(value=0)
        Q_loss_kWh = pd.DataFrame(Q_loss_kWh.sum(axis=0), columns=['Q_loss_kWh'])  # format individual loss data
        total_df = pd.DataFrame(P_loss_kWh.values + Q_loss_kWh.values, index=Q_loss_kWh.index,
                             columns=['total'])  # calculate total loss
        merged_df = P_loss_kWh.join(Q_loss_kWh).join(total_df)
        anchors = []
        load_names = []
        median = []
        peak = []
        total_perc = []
        for field in ['P_loss_kWh', 'Q_loss_kWh']:
            # calculate graph
            anchors.append(', '.join(calc_top_three_anchor_loads(merged_df, field)))
            load_names.append(NAMING[field])  # get correct name
            median.append(round(merged_df[field].median(), 2))  # calculate median
            peak.append(round(merged_df[field].abs().max(), 2))  # calculate peak value
            local_total = round(merged_df[field].sum(), 2)  # calculate total for this building
            total_perc.append(str(local_total) + " (" + str(
                min(round(local_total / total_df.sum().values * 100, 1),
                    100.0)) + " %)")  # transform value to percentage
        column_names = ['Loss Name', 'Total [kWh/yr]', 'Peak [kWh/yr]', 'Median [kWh/yr]', 'Highest 3 Losses']
        column_values = [load_names, total_perc, peak, median, anchors]
        table_df = pd.DataFrame({cn: cv for cn, cv in zip(column_names, column_values)}, columns=column_names)
        return table_df


class EnergyLossBarSubstationPlot(EnergyLossBarPlot):
    """Implement the heat and pressure losses plot"""
    name = "Pumping requirements per building substation"

    def __init__(self, project, parameters, cache):
        super(EnergyLossBarSubstationPlot, self).__init__(project, parameters, cache)
        self.network_args = [self.network_type, self.network_name]
        self.input_files = [(self.locator.get_thermal_network_layout_ploss_system_edges_file, self.network_args),
                            (self.locator.get_thermal_network_qloss_system_file, self.network_args)]

    def calc_graph(self):
        graph = []
        # format demand values
        P_loss_substation_kWh = self.P_loss_substation_kWh.fillna(value=0)
        analysis_field = 'P_loss_kWh'
        P_loss_substation_kWh = pd.DataFrame(P_loss_substation_kWh.sum(axis=0), columns=[analysis_field])
        P_loss_substation_kWh = P_loss_substation_kWh.sort_values(by=analysis_field, ascending=False)
        # iterate through data to plot
        trace = go.Bar(x=P_loss_substation_kWh.index, y=P_loss_substation_kWh[analysis_field].values,
                       name=NAMING[analysis_field],
                       orientation='v',
                       marker=dict(color=COLOR[analysis_field]))
        graph.append(trace)

        return graph

    def calc_table(self):
        analysis_field = 'P_loss_kWh'
        P_loss_substation_kWh = self.P_loss_substation_kWh.fillna(value=0)
        P_loss_substation_kWh = pd.DataFrame(P_loss_substation_kWh.sum(axis=0), columns=[analysis_field])  # format individual loss data
        anchors = []
        load_names = []
        median = []
        peak = []
        total_perc = []
        anchors.append(', '.join(calc_top_three_anchor_loads(P_loss_substation_kWh, analysis_field)))
        load_names.append(NAMING[analysis_field])  # get correct name
        median.append(round(P_loss_substation_kWh[analysis_field].median(), 2))  # calculate median
        peak.append(round(P_loss_substation_kWh[analysis_field].abs().max(), 2))  # calculate peak value
        total = round(P_loss_substation_kWh[analysis_field].sum(), 2)  # calculate total for this building
        column_names = ['Loss Name', 'Total [kWh/yr]', 'Peak [kW]', 'Median [kWh]', 'Highest 3 Losses']
        column_values = [load_names, total, peak, median, anchors]
        table_df = pd.DataFrame({cn: cv for cn, cv in zip(column_names, column_values)}, columns=column_names)
        return table_df


def energy_loss_bar_plot(data_frame, analysis_fields, title, output_path):
    if 'substation' in output_path:
        substation_plot_flag = True
    else:
        substation_plot_flag = False

    # CALCULATE GRAPH
    traces_graph = calc_graph(analysis_fields, data_frame, substation_plot_flag)

    # CALCULATE TABLE
    traces_table = calc_table(analysis_fields, data_frame, substation_plot_flag)

    # PLOT GRAPH
    traces_graph.append(traces_table)
    layout = go.Layout(images=LOGO, title=title, barmode='stack',
                       yaxis=dict(title='Energy [kWh/yr]', domain=[0.35, 1]),
                       xaxis=dict(title='Name'))
    fig = go.Figure(data=traces_graph, layout=layout)
    plot(fig, auto_open=False, filename=output_path)

    return {'data': traces_graph, 'layout': layout}


def calc_table(analysis_fields, data_frame, substation_plot_flag):
    data = data_frame[0].fillna(value=0)
    data = pd.DataFrame(data.sum(axis=0), columns=[analysis_fields[0]])  # format individual loss data
    if not substation_plot_flag:
        data1 = data_frame[1].fillna(value=0)
        data1 = pd.DataFrame(data1.sum(axis=0), columns=[analysis_fields[1]])  # format individual loss data
        total = pd.DataFrame(data.values + data1.values, index=data1.index, columns=['total'])  # calculate total loss
        data = data.join(data1)
    else:
        total = pd.DataFrame(data, columns=['total'])
    data_frame = data.join(total)  # join dataframes
    anchors = []
    load_names = []
    median = []
    peak = []
    total_perc = []
    for field in analysis_fields:
        # calculate graph
        anchors.append(calc_top_three_anchor_loads(data_frame, field))
        load_names.append(NAMING[field])  # get correct name
        median.append(round(data_frame[field].median(), 2))  # calculate median
        peak.append(round(data_frame[field].abs().max(), 2))  # calculate peak value
        local_total = round(data_frame[field].sum(), 2)  # calculate total for this building
        if not substation_plot_flag:
            total_perc.append(str(local_total) + " (" + str(
                min(round(local_total / total.sum().values * 100, 1), 100.0)) + " %)")  # transform value to percentage
        else:
            total_perc.append(str(local_total))
    if not substation_plot_flag:
        table = go.Table(domain=dict(x=[0, 1.0], y=[0, 0.2]),
                         header=dict(
                             values=['Loss Name', 'Total [kWh/yr]', 'Peak [kWh/yr]', 'Median [kWh/yr]',
                                     'Highest 3 Losses']),
                         cells=dict(values=[load_names, total_perc, peak, median, anchors]))
    else:
        table = go.Table(domain=dict(x=[0, 1.0], y=[0, 0.2]),
                         header=dict(
                             values=['Loss Name', 'Total [kWh/yr]', 'Peak [kW]', 'Median [kWh]', 'Highest 3 Losses']),
                         cells=dict(values=[load_names, total_perc, peak, median, anchors]))
    return table


def calc_graph(analysis_fields, data_frame, substation_plot_flag):
    # calculate graph
    graph = []
    # format demand values
    data = data_frame[0].fillna(value=0)
    data = pd.DataFrame(data.sum(axis=0), columns=[analysis_fields[0]])
    if not substation_plot_flag:
        data1 = data_frame[1].fillna(value=0)
        data1 = pd.DataFrame(data1.sum(axis=0), columns=[analysis_fields[1]])
        # calculate total
        total = pd.DataFrame(data.values + data1.values, index=data1.index, columns=['total'])
        # join dataframes
        data = data.join(data1)
        data_frame = data.join(total)
        data_frame = data_frame.sort_values(by='total', ascending=False)  # this will get the maximum value to the left
    else:
        data_frame = data.sort_values(by=analysis_fields[0], ascending=False)
    # iterate through data to plot
    for field in analysis_fields:
        if not substation_plot_flag:
            total_perc = \
            (data_frame[field].values.reshape(1, len(total.index)) / data_frame['total'].values.reshape(1, len(
                total.index)) * 100).round(2)[0]
            total_perc_txt = ["(" + str(x) + " %)" for x in total_perc]
            trace = go.Bar(x=data_frame.index, y=data_frame[field].values, name=NAMING[field],
                           text=total_perc_txt,
                           orientation='v',
                           marker=dict(color=COLOR[field]))
        else:
            trace = go.Bar(x=data_frame.index, y=data_frame[field].values, name=NAMING[field],
                           orientation='v',
                           marker=dict(color=COLOR[field]))
        graph.append(trace)

    return graph


def calc_top_three_anchor_loads(data_frame, field):
    # returns list of top three pipes causing losses
    data_frame = data_frame.sort_values(by=field, ascending=False)
    anchor_list = data_frame[:3].index.values
    return anchor_list


def main():
    """Test this plot"""
    import cea.config
    import cea.plots.cache
    config = cea.config.Configuration()
    cache = cea.plots.cache.PlotCache(config.project)
    cache = cea.plots.cache.NullPlotCache()
    EnergyLossBarPlot(config.project, {'network-type': config.plots.network_type,
                                       'scenario-name': config.scenario_name,
                                       'network-name': config.plots.network_name},
                      cache).plot(auto_open=True)
    EnergyLossBarSubstationPlot(config.project, {'network-type': config.plots.network_type,
                                                 'scenario-name': config.scenario_name,
                                                 'network-name': config.plots.network_name},
                                cache).plot(auto_open=True)


if __name__ == '__main__':
    main()
