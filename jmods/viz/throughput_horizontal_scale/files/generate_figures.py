import pandas as pd
import plotly.express as px
import os
import sys
from datetime import datetime
import time
import gzip
import plotly
import shutil
import plotly.graph_objects as go

# class GroupBucket(list):

JANUS_HOME = "/Users/dporter/projects/janus"


def get_py(py):
    """helper function that returns name of df column name for particular percentile (py) of latency"""
    p_col_name = {
        50: "P50_latency(ms)",
        90: 'P90_latency(ms)',
        95: 'P95_latency(ms)',
        99: 'P99_latency(ms)',
        "QPS": "QPS"
    }
    return p_col_name[py]


def get_trunk(py):
    """helper function that returns name of df column name for particular percentile (py) of latency"""
    p_col_name = {
        "P50_latency(ms)": "P50ms",
        'P90_latency(ms)': "P90ms",
        'P95_latency(ms)': "P95ms",
        'P99_latency(ms)': "P99ms"
    }
    return p_col_name[py]


def get_title(p_col_name):
    """ returns paper-ready y axis name """

    y_axis_title = {
        "P50_latency(ms)": "50th Percentile Query Latency (ms)",
        "P90_latency(ms)": "90th Percentile Query Latency (ms)",
        "P95_latency(ms)": "95th Percentile Query Latency (ms)",
        "P99_latency(ms)": "99th Percentile Query Latency (ms)",
        "QPS": "QPS"
    }
    return y_axis_title[p_col_name]


def getXtitle(input):
    """ returns paper-ready y axis name """

    x_axis_title = {
        "parallel_requests": "Concurrent Connections",
        "QPS": "QPS"
    }
    return x_axis_title[input]


class LineData():
    color_matrix = {
        "solr": plotly.colors.sequential.Reds[6],
        "elastic": plotly.colors.sequential.Greens[6],
        "ideal": plotly.colors.sequential.Greys[6]
    }
    symbol_matrix = {

        0: {11: "circle", 12: "circle-open", 21: "square", 22: "square-open", "2x": "asterisk", "1x": "asterisk"},
        2: {11: "circle", 12: "circle-open", 21: "square", 22: "square-open"},
        4: {11: "circle", 12: "circle-open", 21: "square", 22: "square-open"},
        8: {11: "circle", 12: "circle-open", 21: "square", 22: "square-open"}
    }

    def __repr__(self):
        return str(self.__dict__)

    # input_x == cluster sizes list
    #  input_y == average QPS for each cluster size for a given GROUP
    #  GROUPNAME == the config for that exp. ee.g. rf_multiple == 4 and Shard == 2 ; GROUP =(4 2)
    #  north error == the max QPS for theat cluster for given GROUP
    #  south_error == the min QPS for that GROUP and Cluster

    def __init__(self, gn, csize=0, load=0, engine=0):

        self.csize = csize
        self.input_x = []
        self.input_y = []
        self.GROUPNAME = gn
        self.north_error = []
        self.south_error = []
        self.load = load
        self.name = ''
        self.engine = engine

    def getGn(self):
        return self.GROUPNAME

    #  just gonna save some time and append since this is done in sorted order anyway, so values match across lists
    def setInputX(self, x):
        self.input_x.append(x)

    def setInputY(self, y):
        self.input_y.append(y)

    def setInputNe(self, ne):
        self.north_error.append(ne)

    def setInputSe(self, se):
        self.south_error.append(se)

    def setName(self, gn, engine=''):
        the_load = ''
        the_clustersize = ''
        if self.load > 0:
            the_load = " load=" + str(self.load) + ' '
        if self.csize > 0:
            the_clustersize = ' clustersize=' + str(self.csize)
        self.name = the_load +'engine='+ str(self.engine) + the_clustersize + ' shards=' + str(gn)[0] + " replicas=" + str(gn)[1]

    def setLine(self):
        # clustersize = df.filter(like)
        south = [i - j for i, j in zip(self.input_y, self.south_error)]
        north = [i - j for i, j in zip(self.north_error, self.input_y)]
        max_y = [sum(x) for x in zip(north, self.input_y)]
        # if self.GROUPNAME == "1x" or self.GROUPNAME == "2x":
        #     line_color=dict(color=plotly.colors.sequential.Purples[8])
        #     marker_symbol=dict(symbol=0)
        # else:
        line_color = dict(color=LineData.color_matrix[self.engine])
        marker_symbol = dict(symbol=LineData.symbol_matrix[self.csize][self.GROUPNAME], size=11)

        data = go.Scatter(
            x=self.input_x,
            y=max_y,
            name=self.name,
            line=line_color,
            mode='lines+markers',
            marker=marker_symbol
        )
        return data

    def setLineErrorBars(self):
        # clustersize = df.filter(like)
        south = [i - j for i, j in zip(self.input_y, self.south_error)]
        north = [i - j for i, j in zip(self.north_error, self.input_y)]
        line_color = dict(color=LineData.color_matrix[self.engine])
        marker_symbol = dict(symbol=LineData.symbol_matrix[self.csize][self.GROUPNAME], size=11)
        data = go.Scatter(
            x=self.input_x,
            y=self.input_y,
            error_y=dict(
                type='data',
                symmetric=False,
                array=north,
                arrayminus=south),
            name=self.name)

        return data

    def setTailLine(self):
        # clustersize = df.filter(like)
        # color_index
        # YlGn
        # Reds
        # Blues
        line_color = dict(color=LineData.color_matrix[self.engine])
        marker_symbol = dict(symbol=LineData.symbol_matrix[self.csize][self.GROUPNAME], size=11)
        data = go.Scatter(
            x=self.input_x,
            y=self.input_y,
            name=self.name,
            line=line_color,
            mode='lines+markers',
            marker=marker_symbol,
        )
        return data


# REMEMBER lineList is a List full of line objects with  with just the length of the x axis (clustersize.size) and
# groupname attached to each object
def fillClustersizeLine(lineList, df, col, axis_x):
    """ this function will fill out each CLUSTERSIZE && GROUPNAME linelist object with a list for each  x = axis_x
    and   y = col """

    # pandas complains about the parens
    p_trunk = get_trunk(col)
    df.rename(columns={col: p_trunk}, inplace=True)
    for ld in lineList:
        gn = ld.getGn()
        ld.setName(gn)
        df_engine = df.loc[df['engine'] == ld.engine]
        gn_line_df = df_engine.loc[df_engine['GROUP'] == gn]
        gn_csize_df = gn_line_df.loc[gn_line_df["clustersize"] == ld.csize]
        # gn_csize_df is a df for a single line... just need to populte ld now by iterating over the
        # parallel_requests (x) and setting latency as y
        if axis_x == "QPS":
            x_set = gn_csize_df.QPS.unique()
        else:
            x_set = gn_csize_df.parallel_requests.unique()

        x_set.sort()
        for i in x_set:
            ld.setInputX(i)
            yinput = gn_csize_df.query(axis_x + " == %s" % str(i))
            ld.setInputY(yinput.iloc[0][p_trunk])


def fillClustersizeLineQPS(lineList, df, col):
    for ld in lineList:
        gn = ld.getGn()
        ld.setName(gn)
        df_engine = df.loc[df['engine'] == ld.engine]
        gn_line_df = df_engine.loc[df_engine['GROUP'] == gn]
        gn_csize_df = gn_line_df.loc[df["clustersize"] == ld.csize]
        _df = gn_csize_df.loc[df["engine"] == ld.engine]
        # gn_csize_df is a df for a single line... just need to populte ld now by iterating over the
        # parallel_requests (x_set) and setting latency as y
        x_set = _df.parallel_requests.unique()
        x_set.sort()
        for i in x_set:
            ld.setInputX(i)
            yinput = gn_csize_df.query("parallel_requests == %s" % str(i))
            ld.setInputY(yinput.iloc[0]['QPS'])


def fillLineList(lineList, df, c):
    # this loop fills the data structure the plotting library needs to project the results
    for ld in lineList:
        gn = ld.getGn()
        df.sort_values("clustersize")
        _df = df.loc[df['engine'] == ld.engine]
        _df_ = _df.loc[_df['GROUP'] == gn]

        # for each point on the line's x axis
        for x_point in _df_.clustersize.unique():
            cluster_spec_data_for_gn = _df_.loc[_df_['clustersize'] == x_point]
            ld.setName(gn, engine=ld.engine)
            ld.setInputX(x_point)
            # these two lines remove the warm cache line
            cluster_spec_data_for_gn.sort_values("QPS", inplace=True)
            # cluster_spec_data_for_gn = cluster_spec_data_for_gn.drop(cluster_spec_data_for_gn.index[0])
            # these set the value for a single error bar on the line
            ld.setInputY(cluster_spec_data_for_gn[c].mean())
            ld.setInputNe(cluster_spec_data_for_gn[c].max())
            ld.setInputSe(cluster_spec_data_for_gn[c].min())
                # print(str(ld))


def cdfFillLineList(lineList, df):
    # this loop fills the data structure the plotting library needs to project the results
    seconds_to_millis_factor = 1000

    for ld in lineList:
        gn = ld.getGn()
        ld.setName(gn)
        _df = df.loc[df['engine'] == ld.engine]
        gn_line_df = _df.loc[_df['GROUP'] == gn]
        l_row = gn_line_df.loc[gn_line_df['clustersize'] == ld.csize]
        line_row = l_row.loc[l_row['parallel_requests'] == ld.load]
        fct_values = line_row.iloc[0]["fcts"].split("--")
        # print(fct_values)
        percentile_count = 0
        for i in fct_values:
            ld.setInputX(float(i) * seconds_to_millis_factor)
            ld.setInputY(percentile_count)
            percentile_count = percentile_count + 5


def Py_max_throughput(query, codename, py, axis_x):
    """Py_max_throughput(query, codename, py, axis_x) -> produces a html plot of y=P(py), x=axis_x for the
    experiments """

    lat_fig_title = ""
    lat_fig_title = "SolrCloud Tail Latency (Round Robin)" if query == "direct" else "SolrCloud Tail Latency (SolrJ)"
    p_col_name = get_py(py)
    total_scale_file = JANUS_HOME + '/chart/scaling_exp_csvs/total_' + codename + '.csv'
    df = pd.read_csv(total_scale_file)
    df = df.sort_values("clustersize")
    # <class 'numpy.ndarray'>
    engineList = df.engine.unique()
    clustersizeList = df.clustersize.unique()
    group_array = df.GROUP.unique()
    #  this creates a list of line objects for each groupname/clusersize combo
    latLineList = []
    for e in engineList:
        for csize in clustersizeList:
            for gn in group_array:
                latLineList.append(LineData(gn, csize, engine=e))

    if py == "QPS":
        fillClustersizeLineQPS(latLineList, df, p_col_name)
        # name dirs
        static_dir = JANUS_HOME + '/chart/exp_html_out/figs/' + codename + "/figs/" + "y-QPS_x-load/"
        html_dir = JANUS_HOME + '/chart/exp_html_out/' + codename + "/figs/" + "y-QPS_x-load/"
    else:
        fillClustersizeLine(latLineList, df, p_col_name, axis_x)
        static_dir = JANUS_HOME + '/chart/exp_html_out/figs/' + codename + "/figs/" + "y-percentileTails_x-throughput/"
        html_dir = JANUS_HOME + '/chart/exp_html_out/' + codename + "/figs/" + "y-percentileTails_x-throughput/"

    y_title = get_title(p_col_name)
    x_title = getXtitle(axis_x)

    # this creates the line data the lib needs and packs into a list
    lat_data_list = [x.setTailLine() for x in latLineList]
    fig_lat = go.Figure(lat_data_list)
    x_font = dict(
        size=20,
        color="#7f7f7f"
    )

    fig_lat.update_layout(
        paper_bgcolor='rgba(255,255,255,255)',
        plot_bgcolor='rgba(255,255,255,255)',
        # title=lat_fig_title,
        xaxis_title=x_title,
        showlegend=True,
        xaxis=dict(
            showgrid=True,
            gridcolor="LightGrey",
            title={"font": x_font},
            mirror=True,
            ticks='outside',
            showline=True,
            linewidth=2,
            linecolor="black"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="LightGrey",
            title=y_title,
            mirror=True,
            ticks='outside',
            showline=True,
            linewidth=2,
            linecolor="black"
        )
    )
    try:
        os.makedirs(static_dir)
    except FileExistsError:
        print("file" + static_dir + "exists\n\n\n")
    # directory already exists
    try:
        os.makedirs(html_dir)
    except FileExistsError:
        print("file" + html_dir + "exists\n\n\n")

    plotly.offline.plot(fig_lat, filename=html_dir + query + "_P" + str(py) + "_" + axis_x + '.html')
    fig_lat.write_image(static_dir + query + "_P" + str(py) + "_" + axis_x + ".png")


def display_chart_scaling_errorbar(query, codename):
    qps_fig_title = ""
    qps_fig_title = "SolrCloud Query Throughput (Round Robin)" if query == "roundrobin" else "SolrCloud Query Throughput (SolrJ)"
    lat_fig_title = ""
    lat_fig_title = "SolrCloud Tail Latency (Round Robin)" if query == "roundrobin" else "SolrCloud Tail Latency (SolrJ)"

    total_scale_file = JANUS_HOME + '/chart/scaling_exp_csvs/total_' + codename + '.csv'

    ideal_path = JANUS_HOME + '/chart/scaling_exp_csvs/ideal_line_direct.csv'
    if query == "client":
        ideal_path = JANUS_HOME + '/chart/scaling_exp_csvs/ideal_line.csv'

    df = pd.read_csv(total_scale_file)
    ideal_df = pd.read_csv(ideal_path)
    df_QPS = df.append(ideal_df)
    df_QPS = df_QPS.sort_values("clustersize")
    engineList = df_QPS.engine.unique()
    qpsLineList = []
    for e in engineList:
        df_engine = df_QPS.loc[df_QPS['engine'] == e]
        group_array_QPS = df_engine.GROUP.unique()
        for gn in group_array_QPS:
            qpsLineList.append(LineData(gn, engine=e))
    # latLineList = [LineData(x) for x in group_array_TAIL]
    fillLineList(qpsLineList, df_QPS, "QPS")

    for i in qpsLineList:
        print(i)
    # fillLineList(latLineList, df, "P95_latency(ms)")

    # this creates the line data the lib needs and packs into a list
    qps_data_list = [x.setLine() for x in qpsLineList]
    # lat_data_list = [ x.setLine() for x in latLineList]

    fig_qps = go.Figure(qps_data_list)
    # fig_lat = go.Figure(lat_data_list)

    x_font = dict(
        size=20,
        color="#7f7f7f"
    )
    axis_x = "clustersize"
    y_title = "QPS"
    fig_qps.update_layout(
        paper_bgcolor='rgba(255,255,255,255)',
        plot_bgcolor='rgba(255,255,255,255)',
        # title=lat_fig_title,
        xaxis_title="Cluster Size",
        showlegend=True,
        xaxis=dict(
            showgrid=True,
            gridcolor="LightGrey",
            title={"font": x_font},
            mirror=True,
            ticks='outside',
            showline=True,
            linewidth=2,
            linecolor="black"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="LightGrey",
            title=y_title,
            mirror=True,
            ticks='outside',
            showline=True,
            linewidth=2,
            linecolor="black"
        )
    )

    # fig_qps.show()
    # fig_lat.show()
    static_dir = JANUS_HOME + '/chart/exp_html_out/figs/' + codename + "/figs/scaling/"
    html_dir = JANUS_HOME + '/chart/exp_html_out/' + codename + "/figs/scaling/"

    try:
        os.makedirs(static_dir)
    except FileExistsError:
        print("file" + static_dir + "exists\n\n\n")
    # directory already exists
    try:
        os.makedirs(html_dir)
    except FileExistsError:
        print("file" + html_dir + "exists\n\n\n")

    plotly.offline.plot(fig_qps, filename=html_dir + query + "_" + y_title + "_" + axis_x + '.html')
    fig_qps.write_image(static_dir + query + "_" + y_title + "_" + axis_x + ".png")


def cdf_TAIL(query, codename):
    cdf_fig_title = ""

    total_scale_file = JANUS_HOME + '/chart/scaling_exp_csvs/total_' + codename + '.csv'
    df = pd.read_csv(total_scale_file)
    df = df.sort_values("parallel_requests")
    pr_unique = df.parallel_requests.unique()
    for chart in pr_unique:
        cdf_fig_title = "SolrCloud LOAD=" + str(
            chart) + " TAIL CDF (Round Robin)" if query == "direct" else "SolrCloud " + str(chart) + " TAIL CDF (SolrJ)"

        cdfLineList = []
        df_pr = df.loc[df['parallel_requests'] == chart]
        for index, row in df_pr.iterrows():
            #  there will be a line for each row in the csv
            #     def __init__(self, gn, csize=0, load=0):
            gn = row["GROUP"]
            load = row["parallel_requests"]
            csize = row["clustersize"]
            engine = row["engine"]
            cdfLineList.append(LineData(gn, csize, load, engine))

        cdfFillLineList(cdfLineList, df_pr)

        cdf_data_list = [x.setTailLine() for x in cdfLineList]

        fig_cdf = go.Figure(cdf_data_list)

        # latLineList = [LineData(gn) for gn in group_array]
        yaxis_title = "CDF(x) at LOAD = " + str(chart) + "connections"
        xaxis_title = "Latency (ms)"

        x_font = dict(
            size=20,
            color="#7f7f7f"
        )

        fig_cdf.update_layout(
            paper_bgcolor='rgba(255,255,255,255)',
            plot_bgcolor='rgba(255,255,255,255)',
            # title=lat_fig_title,
            xaxis_title=xaxis_title,
            showlegend=True,
            xaxis=dict(
                showgrid=True,
                gridcolor="LightGrey",
                title={"font": x_font},
                mirror=True,
                ticks='outside',
                showline=True,
                linewidth=2,
                linecolor="black"
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="LightGrey",
                title=yaxis_title,
                mirror=True,
                ticks='outside',
                showline=True,
                linewidth=2,
                linecolor="black"
            )
        )

        static_dir = JANUS_HOME + '/chart/exp_html_out/figs/' + codename + "/figs/cdfs/"
        html_dir = JANUS_HOME + '/chart/exp_html_out/' + codename + "/figs/cdfs/"
        try:
            os.makedirs(static_dir)
        except FileExistsError:
            print("file" + static_dir + "exists\n\n\n")
        # directory already exists
        try:
            os.makedirs(html_dir)
        except FileExistsError:
            print("file" + html_dir + "exists\n\n\n")
        plotly.offline.plot(fig_cdf, filename=html_dir + query + "_" + str(chart) + '.html')
        fig_cdf.write_image(static_dir + query + "_" + str(chart) + ".png")


if __name__ == "__main__":
    print(" ***** FINAL STEP: PLOTTING CHART IN BROWSER ******")
    if len(sys.argv) == 2:
        _query = "roundrobin"
        _chartname = sys.argv[1]

        display_chart_scaling_errorbar(_query, _chartname)
        Py_max_throughput(_query, _chartname, 50, "QPS")
        Py_max_throughput(_query, _chartname, 90, "QPS")
        Py_max_throughput(_query, _chartname, 95, "QPS")
        Py_max_throughput(_query, _chartname, 99, "QPS")
        Py_max_throughput(_query, _chartname, 50, "parallel_requests")
        Py_max_throughput(_query, _chartname, 90, "parallel_requests")
        Py_max_throughput(_query, _chartname, 95, "parallel_requests")
        Py_max_throughput(_query, _chartname, 99, "parallel_requests")
        Py_max_throughput(_query, _chartname, "QPS", "parallel_requests")
        cdf_TAIL(_query, _chartname)

    else:
        print("arg length incorrect")

    print(" ***** FINAL STEP COMPLETE ******")

    sys.exit()
