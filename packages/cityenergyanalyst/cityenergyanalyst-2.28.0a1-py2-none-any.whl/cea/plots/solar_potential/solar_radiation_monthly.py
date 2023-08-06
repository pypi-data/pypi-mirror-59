from __future__ import division
from __future__ import print_function

import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot
import cea.plots.solar_potential
from cea.plots.variable_naming import LOGO, COLOR

__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2018, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Jimeno A. Fonseca"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"


class SolarRadiationMonthly(cea.plots.solar_potential.SolarPotentialPlotBase):
    """Implements the solar-radiation-per-month plot"""
    name = "Solar radiation per month"

    @property
    def layout(self):
        return go.Layout(barmode='stack',
                         yaxis=dict(title='Solar radiation [MWh/month]'))

    def calc_graph(self):
        # calculate graph
        data_frame = self.input_data_aggregated_kW
        analysis_fields = self.analysis_fields
        graph = []
        new_data_frame = (data_frame.set_index("DATE").resample("M").sum() / 1000).round(2)  # to MW
        new_data_frame["month"] = new_data_frame.index.strftime("%B")
        new_data_frame['total'] = new_data_frame[analysis_fields].sum(axis=1)
        for field in analysis_fields:
            y = new_data_frame[field]
            total_perc = (y / new_data_frame['total'] * 100).round(2).values
            total_perc_txt = ["(" + str(x) + " %)" for x in total_perc]
            trace = go.Bar(x=new_data_frame["month"], y=y, name=field, text=total_perc_txt,
                           marker=dict(color=COLOR[field]))
            graph.append(trace)

        return graph

    def calc_table(self):
        data_frame = self.input_data_aggregated_kW
        analysis_fields = self.analysis_fields
        total = (data_frame[analysis_fields].sum(axis=0) / 1000).round(2).tolist()  # to MW
        total_perc = [str(x) + " (" + str(round(x / sum(total) * 100, 1)) + " %)" for x in total]

        new_data_frame = (data_frame.set_index("DATE").resample("M").sum() / 1000).round(2)  # to MW
        new_data_frame["month"] = new_data_frame.index.strftime("%B")
        new_data_frame.set_index("month", inplace=True)
        # calculate graph
        anchors = []
        for field in analysis_fields:
            anchors.append(', '.join(calc_top_three_anchor_loads(new_data_frame, field)))
        column_names = ['Surface', 'Total [MWh/yr]', 'Top 3 most irradiated months']
        column_data = [analysis_fields, total_perc, anchors]
        table_df = pd.DataFrame({cn: cd for cn, cd in zip(column_names, column_data)}, columns=column_names)
        return table_df


def solar_radiation_district_monthly(data_frame, analysis_fields, title, output_path):
    # CALCULATE GRAPH
    traces_graph = calc_graph(analysis_fields, data_frame)

    # CALCULATE TABLE
    traces_table = calc_table(analysis_fields, data_frame)

    # PLOT GRAPH
    traces_graph.append(traces_table)
    layout = go.Layout(images=LOGO, title=title, barmode='stack', yaxis=dict(title='Solar radiation [MWh/month]',
                                                                             domain=[0.35, 1]))
    fig = go.Figure(data=traces_graph, layout=layout)
    plot(fig, auto_open=False, filename=output_path)

    return {'data': traces_graph, 'layout': layout}


def calc_graph(analysis_fields, data_frame):
    # calculate graph
    graph = []
    new_data_frame = (data_frame.set_index("DATE").resample("M").sum() / 1000).round(2)  # to MW
    new_data_frame["month"] = new_data_frame.index.strftime("%B")
    new_data_frame['total'] = new_data_frame[analysis_fields].sum(axis=1)
    for field in analysis_fields:
        y = new_data_frame[field]
        total_perc = (y / new_data_frame['total'] * 100).round(2).values
        total_perc_txt = ["(" + str(x) + " %)" for x in total_perc]
        trace = go.Bar(x=new_data_frame["month"], y=y, name=field, text=total_perc_txt,
                       marker=dict(color=COLOR[field]))
        graph.append(trace)

    return graph


def calc_table(analysis_fields, data_frame):
    total = (data_frame[analysis_fields].sum(axis=0) / 1000).round(2).tolist()  # to MW
    total_perc = [str(x) + " (" + str(round(x / sum(total) * 100, 1)) + " %)" for x in total]

    new_data_frame = (data_frame.set_index("DATE").resample("M").sum() / 1000).round(2)  # to MW
    new_data_frame["month"] = new_data_frame.index.strftime("%B")
    new_data_frame.set_index("month", inplace=True)
    # calculate graph
    anchors = []
    for field in analysis_fields:
        anchors.append(calc_top_three_anchor_loads(new_data_frame, field))
    table = go.Table(domain=dict(x=[0, 1], y=[0.0, 0.2]),
                     header=dict(values=['Surface', 'Total [MWh/yr]', 'Top 3 most irradiated months']),
                     cells=dict(values=[analysis_fields, total_perc, anchors]))

    return table


def calc_top_three_anchor_loads(data_frame, field):
    data_frame = data_frame.sort_values(by=field, ascending=False)
    anchor_list = data_frame[:3].index.values
    return anchor_list


def main():
    """Test this plot"""
    import cea.config
    import cea.inputlocator
    import cea.plots.cache
    config = cea.config.Configuration()
    locator = cea.inputlocator.InputLocator(config.scenario)
    cache = cea.plots.cache.PlotCache(config.project)
    # cache = cea.plots.cache.NullPlotCache()
    weather_path = locator.get_weather_file()
    SolarRadiationMonthly(config.project, {'buildings': None,
                                           'scenario-name': config.scenario_name,
                                           'weather': weather_path},
                          cache).plot(auto_open=True)
    SolarRadiationMonthly(config.project, {'buildings': locator.get_zone_building_names()[0:2],
                                           'scenario-name': config.scenario_name,
                                           'weather': weather_path},
                          cache).plot(auto_open=True)
    SolarRadiationMonthly(config.project, {'buildings': [locator.get_zone_building_names()[0]],
                                           'scenario-name': config.scenario_name,
                                           'weather': weather_path},
                          cache).plot(auto_open=True)


if __name__ == '__main__':
    main()