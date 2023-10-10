# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 21:36:53 2023

@author: ufukc
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
import os
import itertools
from sklearn.preprocessing import normalize, MinMaxScaler
from statsmodels.api import OLS
import statsmodels.api as sm
from statsmodels.formula.api import ols
from sklearn.linear_model import LinearRegression
from linearmodels import PanelOLS
from fixedeffect.fe import fixedeffect
import scipy

os.chdir('C:\\Users\\ufukc\\Documents')

#%% ANALYSIS

data = pd.read_csv('student dataset.csv')

data.insert(0, 'id', '')
data.id = data.match_name + '_' + data.match_type.astype('str') + '_' + data.match_rbz
data['id'] = data.id.replace(" ", "_", regex=True)
data['id'] = data.id.replace("-", "_", regex=True)

data['g_21_31'] = (data.p_1831 / data.p_1821)**(1/10) - 1
data['g_31_37'] = (data.p_1837 / data.p_1831)**(1/6) - 1
data['g_37_40'] = (data.p_1840 / data.p_1837)**(1/3) - 1
data['g_40_43'] = (data.p_1843 / data.p_1840)**(1/3) - 1
data['g_43_46'] = (data.p_1846 / data.p_1843)**(1/3) - 1
data['g_46_49'] = (data.p_1849 / data.p_1846)**(1/3) - 1
data['g_49_52'] = (data.p_1852 / data.p_1849)**(1/3) - 1
data['g_52_55'] = (data.p_1855 / data.p_1852)**(1/3) - 1
data['g_55_61'] = (data.p_1861 / data.p_1855)**(1/6) - 1
data['g_61_64'] = (data.p_1864 / data.p_1861)**(1/3) - 1
data['g_64_67'] = (data.p_1867 / data.p_1864)**(1/3) - 1
data['g_67_71'] = (data.p_1871 / data.p_1867)**(1/4) - 1
data['g_71_75'] = (data.p_1875 / data.p_1871)**(1/4) - 1
data['g_31_49'] = (data.p_1849 / data.p_1831)**(1/18) - 1
data['g_31_49'] = (data.p_1837 / data.p_1831)**(1/6) - 1
data['g_49_75'] = (data.p_1875 / data.p_1849)**(1/26) - 1

data['percent_deaths_1831'] = data.c_1831 / data.c_1831.sum(axis = 0)
data['percent_deaths_1849'] = data.c_1849 / data.c_1849.sum(axis = 0)
data['percent_deaths_1866'] = data.c_1866 / data.c_1866.sum(axis = 0)
data['percent_deaths_1873'] = data.c_1873 / data.c_1873.sum(axis = 0)

data['percent_rkm_1849'] = data.rkm_1849 / data.rkm_1849.sum(axis = 0)
data['percent_rkm_1866'] = data.rkm_1866 / data.rkm_1866.sum(axis = 0)
data['percent_rkm_1873'] = data.rkm_1873 / data.rkm_1873.sum(axis = 0)

list_p = []

for i in np.arange(0, len(data.columns)):
    string = data.columns[i]
    if string[0:2] in ('p_','id'):
        list_p.append(string)
        

def func(string, series, list_func):
    for i in np.arange(0, len(series), 1):
        list_func.append(string + '_' + str(series[i]))
        
series = np.arange(1821, 1876)
string = 'p'
list_func = []
func(string, series, list_func)

for i in np.arange(0, len(list_p)):
    if list_p[i] in list_func:
        list_func.remove(list_p[i])

for i in np.arange(0, len(list_func)):
    x = list_func[i]
    y = int(x[2:6])
    if   y > 1871 :
        data[list_func[i]] = data['p_1871']*(1 + data['g_71_75'])**(y -1871)
    elif y > 1867 :
        data[list_func[i]] = data['p_1867']*(1 + data['g_67_71'])**(y-1867)
    elif y > 1864 :
        data[list_func[i]] = data['p_1864']*(1 + data['g_64_67'])**(y-1864)
    elif y > 1861 :
        data[list_func[i]] = data['p_1861']*(1 + data['g_61_64'])**(y-1861)
    elif y > 1855 :
        data[list_func[i]] = data['p_1855']*(1 + data['g_55_61'])**(y-1855)
    elif y > 1852 :
        data[list_func[i]] = data['p_1852']*(1 + data['g_52_55'])**(y-1852)
    elif y > 1849 :
        data[list_func[i]] = data['p_1849']*(1 + data['g_49_52'])**(y-1849)
    elif y > 1846 :
        data[list_func[i]] = data['p_1846']*(1 + data['g_46_49'])**(y-1846)
    elif y > 1843 :
        data[list_func[i]] = data['p_1843']*(1 + data['g_43_46'])**(y-1843)
    elif y > 1840 :
        data[list_func[i]] = data['p_1840']*(1 + data['g_40_43'])**(y-1840)
    elif y > 1837 :
        data[list_func[i]] = data['p_1837']*(1 + data['g_37_40'])**(y-1837)
    elif y > 1831 :
        data[list_func[i]] = data['p_1831']*(1 + data['g_31_37'])**(y-1831)
    elif y > 1821 :
        data[list_func[i]] = data['p_1821']*(1 + data['g_21_31'])**(y-1821)
        
list_rkm = []
list_p = []
list_c = []
list_time_vary = []
for i in np.arange(0, len(data.columns)):
    string = data.columns[i]
    if string[0:3] in ('rkm','id'):
        list_rkm.append(string)
    if string[0:2] in ('p_','id'):
        list_p.append(string)
    if string[0:2] in ('c_','id'):
        list_c.append(string)
    if string[0:2] in ('rk', 'c_', 'p_', 'g_'):
        list_time_vary.append(string)
        
for i in np.arange(1, len(list_rkm)):
    x = list_rkm[i]
    y = 'density_' + list_rkm[i] + '_sqr'
    data[y] = data[x]**2 / data['area']
    
for i in np.arange(1, len(list_rkm)):
    x = list_rkm[i]
    y = list_rkm[i] + '_per_pop_density'
    z = 'p_' + x[4:8]
    data[y] = data[x]**2 / data[z]
    
for i in np.arange(1, len(list_c)):
    x = list_c[i]
    y = list_c[i] + '_per_pop'
    z = 'p_' + x[2:6]
    data[y] = data[x] / data[z]
    
data = data.copy()
    
data_time_unvary = data.drop(labels = list_time_vary, axis = 1)

data_rkm = pd.melt(data[list_rkm].set_index('id'), value_vars = data[list_rkm].iloc[:, 1:len(data[list_rkm])].columns, value_name = 'rkm', ignore_index = False)
data_p = pd.melt(data[list_p].set_index('id'), value_vars = data[list_p].iloc[:, 1:len(data[list_p])].columns, value_name = 'pop', ignore_index = False)
data_c = pd.melt(data[list_c].set_index('id'), value_vars = data[list_c].iloc[:, 1:len(data[list_c])].columns, value_name = 'chol_deaths', ignore_index = False)

data_rkm.variable = data_rkm.variable.str[4:8].astype('int')
data_p.variable = data_p.variable.str[2:6].astype('int')
data_c.variable = data_c.variable.str[2:6].astype('int')

data_long = data_rkm.merge(data_p.merge(data_c, how = 'outer', on = ['id', 'variable']), how = 'outer', on = ['id', 'variable'])
data_long.columns = data_long.columns.str.replace('variable', 'Year')
data_panel = data_long.merge(data_time_unvary, how = 'outer', on = 'id')

check = data_panel.id.value_counts() == 55
check.all()

data_panel['rkm'] = data_panel.rkm.replace(np.nan, 0)
data_panel.loc[data_panel.Year == 1848, 'chol_deaths'] = data_panel.loc[data_panel.Year == 1848, 'chol_deaths'].replace(np.nan, 0)
data_panel = data_panel.set_index(['id', 'Year'])
data_panel_all_years = data_panel.copy()
data_panel.dropna(subset = 'chol_deaths', inplace = True)
data_panel.index.get_level_values(1).value_counts()

dist_mat = pd.read_csv('Distance Matrix.csv').iloc[:, 0:6]
dist_mat.insert(0, 'id', '')
dist_mat.id = dist_mat.Test_2_NAME + '_' + dist_mat.Test_2_TYPE.astype('str') + '_' + dist_mat.Test_2_RBZ
dist_mat['id'] = dist_mat.id.replace(" ", "_", regex=True)
dist_mat['id'] = dist_mat.id.replace("-", "_", regex=True)
dist_mat = dist_mat.merge(dist_mat[['InputID', 'id']].groupby('InputID').first().reset_index(), left_on = 'TargetID', right_on = 'InputID', how = 'left')
dist_mat = dist_mat[['id_x', 'id_y', 'Distance']]
dist_mat = pd.concat([dist_mat, pd.DataFrame({'id_x':dist_mat['id_x'].unique(), 'id_y':dist_mat['id_x'].unique(), 'Distance':0}).sort_values('id_x')]).sort_values(['id_x', 'id_y']).reset_index(drop = True)
dist_mat.Distance = dist_mat.Distance / 1000
dist_mat = dist_mat.pivot_table(values = 'Distance', index = dist_mat.id_x, columns = 'id_y', aggfunc = 'first')
data_panel = data_panel.reset_index('Year').merge(dist_mat, left_index = True, right_index = True, how = 'left').rename_axis('id').reset_index().set_index(['id', 'Year'])
data_panel['density'] = data_panel['pop'] / data_panel.area
data_panel['percent_deaths'] = data_panel.chol_deaths / data_panel['pop']
print(data_panel.info(verbose = True))

a = data_panel.reset_index()[['Year', 'id', 'chol_deaths']].pivot_table(values = 'chol_deaths', columns = 'id', aggfunc = 'first', index = data_panel.reset_index()['Year'])
a.columns.name = None
b = [a] * 343
c = pd.concat(b).reset_index().iloc[:, 1:]
d = pd.DataFrame(data_panel.iloc[:, 122:465].sort_values(['id', 'Year'])).reset_index(drop = True)
data_panel = data_panel.sort_values(['id', 'Year'])

data_panel.iloc[:, 122:465] = c.div(d).replace([np.inf, -np.inf, np.nan], 0).values
data_panel.iloc[:, 122:465] = c.div(d).replace([np.inf, -np.inf, np.nan], 0).values
data_panel['Weighted_Avg'] = data_panel.iloc[:, 122:465].sum(axis = 1).div(len(data)-1)
data_panel_no_index = data_panel.reset_index()

high_years = data_panel_no_index.groupby('Year').agg({'chol_deaths':'sum'})[data_panel.groupby('Year').agg({'chol_deaths':'sum'}) >= 1000].dropna().index
too_high_years = data_panel_no_index.groupby('Year').agg({'chol_deaths':'sum'})[data_panel.groupby('Year').agg({'chol_deaths':'sum'}) >= 5000].dropna().index

years = data_panel.index.get_level_values('Year')

list_prv = []
for i in np.arange(len(data_panel)):
    list_prv.append(str(data_panel.index.get_level_values('Year')[i]) + '_' + data_panel.org_prv.values[i])
data_panel['prv_year'] = list_prv

list_type = []
for i in np.arange(len(data_panel)):
    list_type.append(str(data_panel.index.get_level_values('Year')[i]) + '_' + data_panel.org_type.values[i])
data_panel['type_year'] = list_type

data_panel.to_csv('data_to_R.csv')
data_panel_high = data_panel[data_panel.index.get_level_values('Year').isin(high_years)]
data_panel_too_high = data_panel[data_panel.index.get_level_values('Year').isin(too_high_years)]
data_panel_high.to_csv('data_to_R_high.csv')
data_panel_too_high.to_csv('data_to_R_too_high.csv')

unique_prv = data.org_prv.unique()

for i in np.arange(0, len(unique_prv)):
    x = str(unique_prv[i]) + '_rkm_1866'
    y = str(unique_prv[i]) + '_chol_death_1866'
    z = str(unique_prv[i]) + '_rkm_div_area_1866'
    l = []
    for j in np.arange(0, len(data)):
        if data['org_prv'][j] == unique_prv[i]:
           l.append(data['rkm_1866'][j])
        else:
           l.append(np.nan)
    
    l_2 = []
    for j in np.arange(0, len(data)):
        if data['org_prv'][j] == unique_prv[i]:
           l_2.append(data['c_1866'][j])
        else:
           l_2.append(np.nan)
           
    l_3 = []
    for j in np.arange(0, len(data)):
        if data['org_prv'][j] == unique_prv[i]:
           l_3.append(data['rkm_1866'][j] / data['area'][j])
        else:
           l_3.append(np.nan)
    
    data[x] = l
    data[y] = l_2
    data[z] = l_3
    
data.to_csv('data_for_province_map')

list_g = []
census_years = [1837, 1840, 1843, 1846, 1849, 1852, 1855, 1861, 1864, 1867, 1871, 1875]

data_to_pop = data.copy()

for i in np.arange(0, len(data_to_pop.columns)):
    string = data_to_pop.columns[i]
    if string[0:2] in ('g_','id'):
        list_g.append(string)
        
for i in np.arange(1, len(list_g)):
    string = list_g[i]
    data_to_pop[string] = data_to_pop[string] * 100

for i in np.arange(1, len(list_rkm)):
    string = list_rkm[i]
    data_to_pop[string] = data_to_pop[string]/100

data_to_pop.to_csv('data_to_pop.csv')

data_rkm_2 = pd.melt(data_to_pop[list_rkm].set_index('id'), value_vars = data_to_pop[list_rkm].iloc[:, 1:len(data_to_pop[list_rkm])].columns, value_name = 'rkm', ignore_index = False)
data_p_2 = pd.melt(data_to_pop[list_p].set_index('id'), value_vars = data_to_pop[list_p].iloc[:, 1:len(data_to_pop[list_p])].columns, value_name = 'pop', ignore_index = False)
data_g_2 = pd.melt(data_to_pop[list_g].set_index('id'), value_vars = data_to_pop[list_g].iloc[:, 1:len(data_to_pop[list_g])].columns, value_name = 'pop_growth', ignore_index = False)
data_g_2 = data_g_2.sort_values(['id', 'variable'])

(data_g_2.value_counts('id') == 15).all()
(data_g_2.value_counts('variable') == 343).all()


growth_years = [1831, 1837,  1876, 1840, 1843, 1846, 1849, 1852, 1877, 1855, 1861, 1864, 1867, 1871, 1875]
growth_years = growth_years*343
data_g_2['variable']= growth_years

data_rkm_2.variable = data_rkm_2.variable.str[4:8].astype('int')
data_p_2.variable = data_p_2.variable.str[2:6].astype('int')

data_g_2 = data_g_2[data_g_2['variable'].isin(census_years)]
data_rkm_2 = data_rkm_2[data_rkm_2['variable'].isin(census_years)]
data_p_2 = data_p_2[data_p_2['variable'].isin(census_years)]


data_long_2 = data_rkm_2.merge(data_p_2.merge(data_g_2, how = 'outer', on = ['id', 'variable']), how = 'outer', on = ['id', 'variable'])
data_long_2.columns = data_long_2.columns.str.replace('variable', 'Year')
data_long_2 = data_long_2.merge(data_time_unvary, how = 'outer', on = 'id')

list_prv = []
for i in np.arange(len(data_long_2)):
    list_prv.append(str(data_long_2.Year.values[i]) + '_' + data_long_2.org_prv.values[i])
data_long_2['prv_year'] = list_prv

list_rbz = []
for i in np.arange(len(data_long_2)):
    list_rbz.append(str(data_long_2.Year.values[i]) + '_' + data_long_2.org_rbz.values[i])
data_long_2['rbz_year'] = list_rbz

data_long_2.to_csv('data_to_pop_panel.csv')
#%% RKM GROWTH LINE GRAPH

GREY10 = "#1a1a1a"
GREY30 = "#4d4d4d"
GREY40 = "#666666"
GREY50 = "#7f7f7f"
GREY60 = "#999999"
GREY75 = "#bfbfbf"
GREY91 = "#e8e8e8"
GREY98 = "#fafafa"

COLOR_SCALE = [
    "#7F3C8D", # Brandenburg
    "#11A579", # Pommern
    "#3969AC", # Posen
    "#F2B701", # Preussen
    "#E73F74", # Rheinland
    "#80BA5A", # Sachsen
    "#E68310", # Schlesien
    GREY50     # Westfalen
]

data_grouped_vis_prv  =data_panel_all_years.groupby(['Year', 'org_prv']).agg(rkm_mean = ('rkm', 'mean'), rkm_sum = ('rkm', 'sum'))
data_grouped_vis_prv_rkm = data_grouped_vis_prv.iloc[data_grouped_vis_prv.index.get_level_values('Year') >= 1835, :].reset_index()

VLINES = np.arange(1830, 1876, 5)

fig, ax = plt.subplots(figsize = (14, 8.5))

fig.patch.set_facecolor('White')
ax.set_facecolor('White')

for h in VLINES:
    ax.axvline(h, color=GREY91, lw=0.6, zorder=0)

ax.axvline(1838, color=GREY40, ls="dotted")

ax.text(1838.5, 520, "1838", fontname="Montserrat", 
        fontsize=14, fontweight=500, color=GREY40, ha="left")

ax.hlines(y=np.arange(0, 2600, 500), xmin=1830, xmax=1876, color=GREY91, lw=0.6)

ax.hlines(y=0, xmin=1830, xmax=1876, color=GREY60, lw=0.8)

for idx, group in enumerate(data_grouped_vis_prv_rkm["org_prv"].unique()):
    dt = data_grouped_vis_prv_rkm[data_grouped_vis_prv_rkm["org_prv"] == group]
    color = COLOR_SCALE[idx]
    ax.plot(dt.Year, dt.rkm_sum, color=color, lw=1.8)
    
ax.set_xlim(1834, 1884)
ax.set_ylim(-100, 2600)
plt.xticks()

LABEL_Y = [
    data_grouped_vis_prv_rkm[(data_grouped_vis_prv_rkm['Year'] == 1875) & (data_grouped_vis_prv_rkm['org_prv'] == 'Brandenburg')]['rkm_sum'],     # Rheinland
    data_grouped_vis_prv_rkm[(data_grouped_vis_prv_rkm['Year'] == 1875) & (data_grouped_vis_prv_rkm['org_prv'] == 'Pommern')]['rkm_sum'],     # Schlesien
    data_grouped_vis_prv_rkm[(data_grouped_vis_prv_rkm['Year'] == 1875) & (data_grouped_vis_prv_rkm['org_prv'] == 'Posen')]['rkm_sum'],      # Preussen
    data_grouped_vis_prv_rkm[(data_grouped_vis_prv_rkm['Year'] == 1875) & (data_grouped_vis_prv_rkm['org_prv'] == 'Preussen')]['rkm_sum'],       # Sachsen
    data_grouped_vis_prv_rkm[(data_grouped_vis_prv_rkm['Year'] == 1875) & (data_grouped_vis_prv_rkm['org_prv'] == 'Rheinland')]['rkm_sum'],     # Westfalen
    data_grouped_vis_prv_rkm[(data_grouped_vis_prv_rkm['Year'] == 1875) & (data_grouped_vis_prv_rkm['org_prv'] == 'Sachsen')]['rkm_sum'],   # Brandenburg
    data_grouped_vis_prv_rkm[(data_grouped_vis_prv_rkm['Year'] == 1875) & (data_grouped_vis_prv_rkm['org_prv'] == 'Schlesien')]['rkm_sum'],       # Pommern
    data_grouped_vis_prv_rkm[(data_grouped_vis_prv_rkm['Year'] == 1875) & (data_grouped_vis_prv_rkm['org_prv'] == 'Westfalen')]['rkm_sum']          # Posen
]

x_start = 1875
x_end = 1877
PAD = 0.1

for idx, group in enumerate(data_grouped_vis_prv_rkm["org_prv"].unique()):
    df = data_grouped_vis_prv_rkm[(data_grouped_vis_prv_rkm["org_prv"] == group) & (data_grouped_vis_prv_rkm["Year"] == 1875)]
    color = COLOR_SCALE[idx]
    
    text = df["org_prv"].values[0]

    y_start = df["rkm_sum"].values[0]

    y_end = LABEL_Y[idx]

    ax.plot(
        [x_start, (x_start + x_end - PAD) / 2 , x_end - PAD], 
        [y_start, y_end, y_end], 
        color=color, 
        alpha=0.5, 
        ls="dashed"
    )

    ax.text(
        x_end, 
        y_end, 
        text, 
        color=color, 
        fontsize=14, 
        weight="bold", 
        fontfamily="Montserrat", 
        va="center"
    )

ax.set_yticks([y for y in np.arange(0, 2600, 500)])
ax.set_yticklabels(
    [y for y in np.arange(0, 2600, 500)], 
    fontname="Montserrat", 
    fontsize=11,
    weight=500,
    color=GREY40
)

ax.set_xticks([x for x in np.arange(1835, 1876, 5)])
ax.set_xticklabels(
    [x for x in np.arange(1835, 1876, 5)], 
    fontname= "Montserrat", 
    fontsize=13,
    weight=500,
    color=GREY40
)

ax.tick_params(axis="x", length=12, color=GREY91)
ax.tick_params(axis="y", length=8, color=GREY91)

ax.spines["left"].set_color(GREY91)
ax.spines["bottom"].set_color(GREY91)
ax.spines["right"].set_color("none")
ax.spines["top"].set_color("none")

fig.text(
    0.08,
    0.92,
    "Railroad Expansion in Prussia Between 1835-1975",
    color=GREY10,
    fontsize=15,
    fontname="Montserrat",
    weight="bold"
)

fig.text(
    0.08,
    0.92,
    "Railroad Expansion in Prussia Between 1835-1975",
    color=GREY10,
    fontsize=15,
    fontname="Montserrat",
    weight="bold"
)

fig.text(
    0.06,
    0.35,
    "Railroad Length in Km",
    color=GREY10,
    fontsize=15,
    fontname="Montserrat",
    rotation = 90
)

fig.text(
    0.45,
    0.04,
    "Year 1835-1875",
    color=GREY10,
    fontsize=15,
    fontname="Montserrat"
)

#plt.savefig('Plot_1_epidemics_rkm.png', dpi = 300)

plt.show()

#%% RKM - POP GROWTH LINE GRAPH

census_years = [1821, 1831, 1837, 1840, 1843, 1846, 1849, 1852, 1855, 1861, 1864, 1867, 1871, 1875]

data_grouped_type = data_panel_all_years.groupby(['Year', 'org_type']).agg({'pop':'sum', 'rkm':'sum'})
data_grouped_type = data_grouped_type.merge(data_grouped_type.pct_change(periods = 2), left_index = True, right_index = True, how = 'left')
data_grouped_type = data_grouped_type[data_grouped_type.index.get_level_values('Year').isin(census_years)]
data_grouped_type.columns = ['pop', 'rkm', 'pop_change', 'rkm_change']
data_grouped_type = data_grouped_type.reset_index()

COLOR_SCALE_POP = [
    "#3969AC",
    "#E73F74"
]

fig_pop, ax_pop = plt.subplots(figsize = (14, 8.5))

VLINES_pop_rkm = np.arange(0, 0.042, 0.005)

fig_pop.patch.set_facecolor('White')
ax_pop.set_facecolor('White')

for h in VLINES_pop_rkm:
    ax_pop.axvline(h, color=GREY91, lw=0.6, zorder=0)

ax_pop.axvline(1855, color=GREY40, ls="dotted")

ax_pop.text(1855.5, 0.037, "1855", fontname="Montserrat", 
        fontsize=14, fontweight=500, color=GREY40, ha="left")

ax_pop.hlines(y=np.arange(0, 0.042, 0.005), xmin=1830, xmax=1876, color=GREY91, lw=0.6)

ax_pop.hlines(y=0, xmin=1830, xmax=1876, color=GREY60, lw=0.8)


for idx, group in enumerate(data_grouped_type['org_type'].unique()):
    dt = data_grouped_type[data_grouped_type['org_type'] == group]
    color = COLOR_SCALE_POP[idx]
    ax_pop.plot(dt.Year, dt['pop_change'], color=color, lw=1.8)
    
ax_pop.set_xlim(1834, 1884)
ax_pop.set_ylim(-0.0015, 0.042)
plt.xticks()

LABEL_Y_type = [
    data_grouped_type[(data_grouped_type['Year'] == 1875) & (data_grouped_type['org_type'] == 'Landkreis')]['pop_change'],
    data_grouped_type[(data_grouped_type['Year'] == 1875) & (data_grouped_type['org_type'] == 'Stadtkreis')]['pop_change']
    ]

x_start = 1875
x_end = 1877
PAD = 0.1

for idx, group in enumerate(data_grouped_type['org_type'].unique()):
    df = data_grouped_type[(data_grouped_type['org_type'] == group) & (data_grouped_type["Year"] == 1875)]
    color = COLOR_SCALE_POP[idx]
    
    text = df["org_type"].values[0]

    y_start = df["pop_change"].values[0]

    y_end = LABEL_Y_type[idx]

    ax_pop.plot(
        [x_start, (x_start + x_end - PAD) / 2 , x_end - PAD], 
        [y_start, y_end, y_end], 
        color=color, 
        alpha=0.5, 
        ls="dashed"
    )

    ax_pop.text(
        x_end, 
        y_end, 
        text, 
        color=color, 
        fontsize=14, 
        weight="bold", 
        fontfamily="Montserrat", 
        va="center"
    )

ax_pop.set_yticks([y for y in np.arange(0, 0.042, 0.005)])
ax_pop.set_yticklabels(
    [y for y in np.arange(0, 0.042, 0.005)], 
    fontname="Montserrat", 
    fontsize=11,
    weight=500,
    color=GREY40
)

ax_pop.set_xticks([x for x in np.arange(1835, 1876, 5)])
ax_pop.set_xticklabels(
    [x for x in np.arange(1835, 1876, 5)], 
    fontname= "Montserrat", 
    fontsize=13,
    weight=500,
    color=GREY40
)

ax_pop.tick_params(axis="x", length=12, color=GREY91)
ax_pop.tick_params(axis="y", length=8, color=GREY91)

ax_pop.spines["left"].set_color(GREY91)
ax_pop.spines["bottom"].set_color(GREY91)
ax_pop.spines["right"].set_color("none")
ax_pop.spines["top"].set_color("none")

fig_pop.text(
    0.08,
    0.92,
    "Urban and Rural Counties population ",
    color=GREY10,
    fontsize=15,
    fontname="Montserrat",
    weight="bold"
)

fig_pop.text(
    0.06,
    0.35,
    "Annualized Population Growth Rate",
    color=GREY10,
    fontsize=15,
    fontname="Montserrat",
    rotation = 90
)

fig_pop.text(
    0.45,
    0.04,
    "Year 1835-1875",
    color=GREY10,
    fontsize=15,
    fontname="Montserrat"
)


#plt.savefig('Plot_2_epidemics_pop.png', dpi = 300)
plt.show()



#%% RKM - CHOLERA DEATH 1866

data_vis_1866 = data_panel_all_years[(data_panel_all_years.index.get_level_values('Year') == 1866)]
data_vis_1866['rkm_density'] = data_vis_1866['rkm'] / data_vis_1866['area']
data_vis_1866_no_out = data_panel_all_years[(data_panel_all_years.index.get_level_values('Year') == 1866) & (data_panel_all_years['chol_deaths'] <= 3000)]
data_vis_1866_no_out['rkm_density'] = data_vis_1866_no_out['rkm'] / data_vis_1866['area']
 
VLINES_g0 = np.arange(0, 155, 20)

g0 = sns.JointGrid(x='rkm', y="chol_deaths", data=data_vis_1866, xlim = (-5, 155), ylim = (-270, 6303))
g0.plot_joint(sns.scatterplot, s = 30, color = '#3969AC', ax=g0.ax_joint, alpha = .8)
g0.plot_joint(sns.regplot, ci = None, scatter = False, color = 'purple')
g0.plot_marginals(sns.histplot, kde=True, color='#3969AC')

slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x=data_vis_1866['rkm'],y=data_vis_1866['chol_deaths'])

g0.set_axis_labels('Railroad Length in Km in 1866', 'Cholera Deaths in 1866', fontname="Montserrat")

for h in VLINES_g0:
    g0.ax_joint.axvline(h, color=GREY91, lw=0.6, zorder=0)

g0.ax_joint.hlines(y=np.arange(0, 6303, 750), xmin=0, xmax=155, color=GREY91, lw=0.6, zorder=0)

g0.ax_joint.hlines(y=0, xmin=0, xmax=155, color=GREY60, lw=0.8, zorder=0)
g0.ax_joint.set_facecolor(GREY98)
g0.ax_joint.set_yticks([y for y in np.arange(0, 6303, 750)])
g0.ax_joint.set_yticklabels(
    [y for y in np.arange(0, 6303, 750)], 
    fontname="Montserrat", 
    fontsize=11,
    weight=500,
    color=GREY40
)

g0.ax_joint.set_xticks([x for x in np.arange(0, 155, 20)])
g0.ax_joint.set_xticklabels(
    [x for x in np.arange(0, 155, 20)], 
    fontname= "Montserrat", 
    fontsize=13,
    weight=500,
    color=GREY40
)

g0.ax_joint.tick_params(axis="x", length=12, color=GREY91)
g0.ax_joint.tick_params(axis="y", length=8, color=GREY91)

g0.ax_joint.spines["left"].set_color(GREY91)
g0.ax_joint.spines["bottom"].set_color(GREY91)
g0.ax_joint.spines["right"].set_color("none")
g0.ax_joint.spines["top"].set_color("none")

plt.setp(g0.ax_joint, zorder=10, label="")

g0.ax_joint.text(100, 5250, 'slope = {}'.format(round(slope, 2)), fontfamily="Montserrat", fontsize=11, weight=500)
g0.ax_joint.text(11, 4380, 'Breslau', fontfamily="Montserrat", fontsize=11, weight=500)
g0.ax_joint.text(39, 3900, 'Posen', fontfamily="Montserrat", fontsize=11, weight=500)
g0.ax_joint.text(17, 5370, 'Berlin', fontfamily="Montserrat", fontsize=11, weight=500)

#plt.savefig('Subplot_1866_1.png', dpi = 300)

plt.show()

VLINES_g1 = np.arange(0, 155, 20)

g1 = sns.JointGrid(x="rkm", y="chol_deaths", data=data_vis_1866_no_out, xlim = (-5, 155), ylim = (-90, 2101))
g1.plot_joint(sns.scatterplot, s = 30, color = "#3969AC", ax=g1.ax_joint, legend = None, alpha = .8)
g1.plot_joint(sns.regplot, ci = None, scatter = False, color = 'purple')
g1.plot_marginals(sns.histplot, kde=True, color="#3969AC")

slope_no_out, intercept, r_value, p_value, std_err = scipy.stats.linregress(x=data_vis_1866_no_out['rkm'],y=data_vis_1866_no_out['chol_deaths'])

g1.set_axis_labels('Railroad Length in Km in 1866', 'Cholera Deaths in 1866', fontname="Montserrat")

for h in VLINES_g1:
    g1.ax_joint.axvline(h, color=GREY91, lw=0.6, zorder=0)

g1.ax_joint.hlines(y=np.arange(0, 2101, 250), xmin=0, xmax=155, color=GREY91, lw=0.6, zorder=0)
g1.ax_joint.set_facecolor(GREY98)

g1.ax_joint.hlines(y=0, xmin=0, xmax=155, color=GREY60, lw=0.8, zorder=0)

g1.ax_joint.set_yticks([y for y in np.arange(0, 2101, 250)])
g1.ax_joint.set_yticklabels(
    [y for y in np.arange(0, 2101, 250)], 
    fontname="Montserrat", 
    fontsize=11,
    weight=500,
    color=GREY40
)

g1.ax_joint.set_xticks([x for x in np.arange(0, 155, 20)])
g1.ax_joint.set_xticklabels(
    [x for x in np.arange(0, 155, 20)], 
    fontname= "Montserrat", 
    fontsize=13,
    weight=500,
    color=GREY40
)

g1.ax_joint.tick_params(axis="x", length=12, color=GREY91)
g1.ax_joint.tick_params(axis="y", length=8, color=GREY91)


g1.ax_joint.spines["left"].set_color(GREY91)
g1.ax_joint.spines["bottom"].set_color(GREY91)
g1.ax_joint.spines["right"].set_color("none")
g1.ax_joint.spines["top"].set_color("none")

g1.ax_joint.text(100, 1750, 'slope = {}'.format(round(slope_no_out, 2)), fontfamily="Montserrat", fontsize=11, weight=500)

plt.setp(g1.ax_joint, zorder=10, label="")

#plt.savefig('Subplot_1866_2.png', dpi = 300)

plt.show()

#%% 1866 HISTOGRAM CHOLERA DEATHS

data_grouped = data_long.groupby('Year').agg({'rkm':'sum', 'pop':'sum', 'chol_deaths':'sum'})

fig_br2, ax_br2 = plt.subplots(figsize=(12, 7))

ax_br2.bar(data_grouped.chol_deaths[data_grouped.chol_deaths != 0].index.astype('category'), 
           data_grouped.chol_deaths[data_grouped.chol_deaths != 0], color = "#7F3C8D", width = .9, zorder = 1)
plt.xticks(data_grouped.chol_deaths[data_grouped.chol_deaths != 0].index.unique().astype("category"), rotation = 90)

VLINES_hist = data_grouped.chol_deaths[data_grouped.chol_deaths != 0].index.unique()

for h in VLINES_hist:
    ax_br2.axvline(h, color=GREY91, lw=0.6, zorder = 0)

ax_br2.axhline(1000, color=GREY40, ls="dotted")
ax_br2.axhline(5000, color=GREY40, ls="dotted")

ax_br2.text(1842.75, 31000, "5000", fontname="Montserrat", 
        fontsize=14, fontweight=500, color=GREY40, ha="left")
ax_br2.text(1860.7, 21000, "1000", fontname="Montserrat", 
        fontsize=14, fontweight=500, color=GREY40, ha="left")

ax_br2.annotate('', xy=(1844,31000), xytext=(1844,4900), fontsize = 16, arrowprops={'arrowstyle':'->', 'facecolor':GREY40}, horizontalalignment='center')
ax_br2.annotate('', xy=(1862,21000), xytext=(1862,900), fontsize = 16, arrowprops={'arrowstyle':'->'}, horizontalalignment='center')

ax_br2.hlines(y=np.arange(0, 120100, 20000), xmin=0, xmax=120100, color=GREY91, lw=0.6, zorder = 0)

ax_br2.hlines(y=0, xmin=0, xmax=120100, color=GREY60, lw=0.8, zorder = 0)

ax_br2.set_xticks([x for x in VLINES_hist])
ax_br2.set_xticklabels(
    [x for x in VLINES_hist], 
    fontname= "Montserrat", 
    fontsize=11,
    weight=500,
    color=GREY40
)

ax_br2.set_yticks([y for y in np.arange(0, 120100, 20000)])
ax_br2.set_yticklabels(
    [y for y in np.arange(0, 120100, 20000)], 
    fontname="Montserrat", 
    fontsize=11,
    weight=500,
    color=GREY40
)

ax_br2.set_xlim(1828, 1875)
ax_br2.set_ylim(0, 120000)

fig_br2.text(
    0.07,
    0.92,
    "Cholera Deaths in Prussia by Year",
    color=GREY10,
    fontsize=15,
    fontname="Montserrat",
    weight="bold"
)

fig_br2.text(
    0.05,
    0.25,
    "Death Caused by Cholera",
    color=GREY10,
    fontsize=15,
    fontname="Montserrat",
    rotation = 90
)

fig_br2.text(
    0.42,
    0.00,
    "Year 1831-1874",
    color=GREY10,
    fontsize=15,
    fontname="Montserrat"
)

#plt.savefig('hist_chol_deaths_by_year.png', dpi = 300)
plt.show()

#%% HORIZONTAL BAR CHARTS

data_vis_1866_top_5 = data_panel[(data_panel.index.get_level_values('Year') == 1866)].sort_values('density', ascending = False).head(5)
data_vis_1866_bottom_5 = data_panel[(data_panel.index.get_level_values('Year') == 1866)].sort_values('density', ascending = True).head(5)
data_vis_1866_top_bottom_5 = pd.concat([data_vis_1866_top_5.sort_values('density', ascending = True), data_vis_1866_bottom_5], axis = 0)
data_vis_1866_top_bottom_5['rkm_per_area'] = data_vis_1866_top_bottom_5['rkm'] / data_vis_1866_top_bottom_5['area']
data_vis_1866_top_bottom_5['rkm_per_area'] = data_vis_1866_top_bottom_5['rkm'] / data_vis_1866_top_bottom_5['area']

id_1 = ['Breslau', 'Koln', 'Halle', 'Barmen', 'Konigsberg', 'Johannisburg', 'Schlochau', 'Rummelsburg', 'Deutsch Krone', 'Neidenburg']

data_vis_1866_top_bottom_5['ID'] = id_1
data_vis_1866_top_bottom_5 = data_vis_1866_top_bottom_5.sort_values('density')

data_vis_1866_top_5_chol = data_panel[(data_panel.index.get_level_values('Year') == 1866)].sort_values('Weighted_Avg', ascending = False).head(5)
data_vis_1866_bottom_5_chol = data_panel[(data_panel.index.get_level_values('Year') == 1866) & (data_panel['chol_deaths'] >= 100)].sort_values('Weighted_Avg', ascending = True).head(5)
data_vis_1866_top_bottom_5_chol = pd.concat([data_vis_1866_top_5_chol.sort_values('Weighted_Avg', ascending = True), data_vis_1866_bottom_5_chol], axis = 0)
data_vis_1866_top_bottom_5_chol['rkm_per_area'] = data_vis_1866_top_bottom_5_chol['rkm'] / data_vis_1866_top_bottom_5_chol['area']

id_2 = ['Neumarkt', 'Trebnitz', 'Obornik', 'Niederbarnim', 'Breslau', 'Saarlouis', 'Trier', 'Saarburg', 'Bitburg', 'Kreuznach']

data_vis_1866_top_bottom_5_chol['ID'] = id_2
data_vis_1866_top_bottom_5_chol = data_vis_1866_top_bottom_5_chol.sort_values('Weighted_Avg')

fig_bar, ax_bar = plt.subplots(figsize=(16, 7), ncols=2, sharey=True)
fig_bar.tight_layout()

ax_bar[0].invert_xaxis()

VLINES_bar_0 = np.arange(2000, 17550, 2500)
VLINES_bar_1 = np.arange(0, 4212, 600)

for h in VLINES_bar_0:
    ax_bar[0].axvline(h, color=GREY91, lw=0.6, zorder=0)
    
for h in VLINES_bar_1:
    ax_bar[1].axvline(h, color=GREY91, lw=0.6, zorder=0)

ax_bar[0].barh(data_vis_1866_top_bottom_5['ID'], data_vis_1866_top_bottom_5['density'], align='center', color="#E68310", zorder=10)
ax_bar[0].set_title('Population Density', fontsize=18, pad=15, color="#E68310")
ax_bar[1].barh(data_vis_1866_top_bottom_5['ID'], data_vis_1866_top_bottom_5['chol_deaths'], align='center', color="#11A579", zorder=10)
ax_bar[1].set_title('Cholera Deaths', fontsize=18, pad=15, color="#11A579")

ax_bar[1].set_xticks([x for x in np.arange(0, 4212, 600)])
ax_bar[1].set_xticklabels(
    [x for x in np.arange(0, 4212, 600)], 
    fontname= "Montserrat", 
    fontsize=13,
    weight=500,
    color=GREY40
)

ax_bar[0].set_xticks([x for x in np.arange(2000, 17550, 2500)])
ax_bar[0].set_xticklabels(
    [x for x in np.arange(2000, 17550, 2500)], 
    fontname= "Montserrat", 
    fontsize=13,
    weight=500,
    color=GREY40
)

ax_bar[0].set_yticklabels(
    data_vis_1866_top_bottom_5['ID'], 
    fontname="Montserrat", 
    fontsize=15,
    weight=500,
    color=GREY40
)

ax_bar[1].tick_params(axis="x", length=12, color=GREY91)
ax_bar[1].tick_params(axis="y", length=8, color=GREY91)
ax_bar[0].tick_params(axis="x", length=12, color=GREY91)
ax_bar[0].tick_params(axis="y", length=8, color=GREY91)

subtitle_1 = [
    "The chart shows 5 counties with highest population density (Königsberg, Barmen, Halle, Köln, Breslau) and 5 counties with lowest population density" 
    ,"(Neidenburg, Deutsch Krone, Rummelsburg, Schlochau, Johannisburg)."
]

fig_bar.text(
    -0.04,
    -0.10,
    "\n".join(subtitle_1),
    ha="left",
    color='black',
    fontname="Montserrat",
    fontsize=14,
)

plt.subplots_adjust(wspace=0, hspace=0)
#plt.savefig('Density_Death_Bar.png', dpi = 300)
plt.show()


fig_bar_1, ax_bar_1 = plt.subplots(figsize=(16, 7), ncols=2, sharey=True)
fig_bar_1.tight_layout()

ax_bar_1[0].invert_xaxis()

VLINES_bar_1_0 = np.arange(0.5, 3.51, 0.5)
VLINES_bar_1_1 = np.arange(0, 1751, 250)

for h in VLINES_bar_1_0:
    ax_bar_1[0].axvline(h, color=GREY91, lw=0.6, zorder=0)
    
for h in VLINES_bar_1_1:
    ax_bar_1[1].axvline(h, color=GREY91, lw=0.6, zorder=0)

ax_bar_1[0].barh(data_vis_1866_top_bottom_5_chol['ID'], data_vis_1866_top_bottom_5_chol['Weighted_Avg'], align='center', color="#E68310", zorder=10)
ax_bar_1[0].set_title('Cholera Death / Distance', fontsize=18, pad=15, color="#E68310")
ax_bar_1[1].barh(data_vis_1866_top_bottom_5_chol['ID'], data_vis_1866_top_bottom_5_chol['chol_deaths'], align='center', color="#11A579", zorder=10)
ax_bar_1[1].set_title('Cholera Deaths', fontsize=18, pad=15, color="#11A579")

ax_bar_1[1].set_xticks([x for x in np.arange(0, 1751, 250)])
ax_bar_1[1].set_xticklabels(
    [x for x in np.arange(0, 1751, 250)], 
    fontname= "Montserrat", 
    fontsize=13,
    weight=500,
    color=GREY40
)

ax_bar_1[0].set_xticks([x for x in np.arange(0.5, 3.51, 0.5)])
ax_bar_1[0].set_xticklabels(
    [x for x in np.arange(0.5, 3.51, 0.5)], 
    fontname= "Montserrat", 
    fontsize=13,
    weight=500,
    color=GREY40
)

ax_bar_1[0].set_yticklabels(
    data_vis_1866_top_bottom_5_chol['ID'], 
    fontname="Montserrat", 
    fontsize=15,
    weight=500,
    color=GREY40
)

ax_bar_1[1].tick_params(axis="x", length=12, color=GREY91)
ax_bar_1[1].tick_params(axis="y", length=8, color=GREY91)
ax_bar_1[0].tick_params(axis="x", length=12, color=GREY91)
ax_bar_1[0].tick_params(axis="y", length=8, color=GREY91)

subtitle = [
    "The chart shows 5 counties with highest weighted average of neighbor deaths (Breslau, Niederbarnim, Obornik, Trebnitz, Neumarkt) and 5 counties with lowest",
    "weighted average of neighbor deaths (Kreuznach, Bitburg, Saarburg, Trier, Saarlouis)."
]

fig_bar_1.text(
    -0.04,
    -0.10,
    "\n".join(subtitle),
    ha="left",
    color='black',
    fontname="Montserrat",
    fontsize=14,
)


plt.subplots_adjust(wspace=0, hspace=0)
#plt.savefig('WeigAvg_Death_Bar.png', dpi = 300)
plt.show()
