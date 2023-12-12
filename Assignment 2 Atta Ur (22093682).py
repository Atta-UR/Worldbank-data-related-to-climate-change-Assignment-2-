import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def lineplot(x, y, xlabel, ylabel, title, labels):
    """ Funtion to Create Lineplot. Arguments:
        list of values for xaxis
        list of values for yaxis
        xlabel, ylabel and titel value
        color name
        label value
    """
    plt.style.use('tableau-colorblind10')
    plt.figure(figsize=(7, 5))
    for index in range(len(y)):
        plt.plot(x, y[index], label=labels[index], linestyle='--')
    plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=6))
    plt.xticks(rotation=90)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.savefig('Line_plot.jpg', dpi=500)
    plt.show()
    return


def barplot(dataframe, xlabel, ylabel, title):
    """
    Draw a bar plot.
    Parameters
    ----------
    dataframe : Pandas Dataframe
        Data for the Bar Graph.
    xlabel : String
        To show what is on xaxis in our case years.
    ylabel : String
        to show what is on x-axis.
    title : String
        to show what graph is about.

    """
    dataframe.plot(kind='bar', figsize=(10, 6))
    # Set plot labels and title
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig('barplot.jpg', dpi=500)
    plt.show()
    return


def draw_scatter_plot(x, y, title='Scatter Plot', xlabel='X-Axis',
                      ylabel='Y-Axis', color='blue', marker='o', label=None):
    """
    Draw a scatter plot using Matplotlib.

    Parameters:
        x (list): X-axis data points.
        y (list): Y-axis data points.
        title (str): Title of the scatter plot.
        xlabel (str): Label for the X-axis.
        ylabel (str): Label for the Y-axis.
        color (str): Color of the markers.
        marker (str): Marker style.
        label (str): Label for the legend.
    """
    plt.scatter(x, y, color=color, marker=marker, label=label)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    if label is not None:
        plt.legend()
    plt.show()


def make_corr_heat_map(df, title, cmap='viridis'):
    """
    Make a Heatmap to show correlation among Features
    Parameters
    ----------
    df : Pandas Dataframe
        DESCRIPTION.
    title : String
        to show the title.
    cmap : String, optional
        DESCRIPTION. The default is 'viridis'. its for choosing colours

    """
    correlation_matrix = df.corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    heatmap = ax.pcolormesh(correlation_matrix, cmap=cmap)
    cbar = plt.colorbar(heatmap)
    for i in range(len(correlation_matrix.columns)):
        for j in range(len(correlation_matrix.columns)):
            ax.text(j + 0.5, i + 0.5, f'{correlation_matrix.iloc[i, j]:.2f}',
                    ha='center', va='center', color='white')
    ax.set_xticks(range(len(correlation_matrix.columns)))
    ax.set_yticks(range(len(correlation_matrix.columns)))
    ax.set_xticklabels(correlation_matrix.columns, rotation=90)
    ax.set_yticklabels(correlation_matrix.columns)
    plt.title(title)
    plt.savefig('Heatmap_plot.jpg', dpi=500)
    plt.show()


def get_refine_data(df, countries, start_year, up_to_year):
    """
    Get Data for the given Countries.
    Parameters
    ----------
    df : Pandas Dataframe
        DESCRIPTION.
    countries : list of countries
        to get the data for related coutries only.
    start_year : String
        from which year we start to extract data.
    up_to_year : string
        up to the year we want to get data.

    Returns
    -------
    selected_data : data frame

    """
    df = df.T
    df = df.drop(['Country Code', 'Indicator Name', 'Indicator Code'])
    df.columns = df.iloc[0]
    df = df.drop(['Country Name'])
    df = df.reset_index()
    df['Years'] = df['index']
    df = df.drop('index', axis=1)
    df = df[(df['Years'] >= start_year) & (df['Years'] <= up_to_year)]
    selected_data = df[countries]
    selected_data = selected_data.fillna(selected_data.iloc[:, :-1].mean())
    return selected_data


def get_data_for_specific_country(data_frame_list, country_name, names,
                                  start_year, end_year):
    """
    Get Data for Specific Countries.
    Parameters
    ----------
    dataframe_list : Pandas Dataframes
        Data Frames of different informations.
    countriescountry_name : String
        to get the data for specific counytry only.
    names : string
        names of the datasets.
    start_year : String
        from which year we start to extract data.
    up_to_year : string
        up to the year we want to get data.

    Returns
    -------
    country_data:Specified Country's data frame
    """
    country_data = []
    for i, data in enumerate(data_frame_list):
        data = get_refine_data(data, country_name, start_year, end_year)
        data = data.rename(columns={country_name[0]: names[i]})
        country_data.append(data)
    country_data = pd.concat(country_data, axis=1)
    country_data = country_data.T.drop_duplicates().T
    country_data = country_data.drop('Years', axis=1)
    return country_data


def get_lists(df, cols):
    """
    Get Lists of Dataframe
    Parameters
    ----------
    df : Pnadas DataFrame
        Data frame to convert into lists.
    cols : list of coloumns.
        Coloumns to Convert to lists.
    Returns
    -------
    column_lists : Lists
        Lists to Return.

    """
    column_lists = [df[col].tolist() for col in cols[:-1]]
    return column_lists


def data_for_bar(df, years):
    """
    Get Data for given years.country_data

    Parameters
    ----------
    df : Pandas Data Frame
    years : list of years
    Returns
    -------
    df : Data Frame of Specified years data

    """
    df = df[df['Years'].isin(years)]
    df = df.set_index('Years')
    return df


total_population = pd.read_csv('total_population.csv', skiprows=4)
Urban_population = pd.read_csv('Urban_population.csv', skiprows=4)
cols = ['Indonesia', 'Nigeria', 'Brazil', 'Pakistan', 'Philippines', 'Years']
start_year = '1970'
end_year = '2021'
lineplot(list(get_refine_data(total_population, cols, start_year, end_year)
              ['Years']), get_lists(get_refine_data(total_population, cols,
                                                    start_year, end_year), cols), 'Years',
         'Population', 'Total Population', cols[:-1])
lineplot(list(get_refine_data(Urban_population,
                              cols,
                              start_year,
                              end_year)['Years']),
         get_lists(get_refine_data(Urban_population,
                                   cols,
                                   start_year,
                                   end_year),
                   cols),
         'Years',
         "Urban Population",
         'Urban Population',
         cols[:-1])
Manufacturing_value_added_USD = pd.read_csv(
    'Manufacturing_value_added_USD.csv', skiprows=4)
CO2_emissions = pd.read_csv('CO2_emissions.csv', skiprows=4)
years = ['1995', '2000', '2005', '2010', '2015', '2020']
barplot(
    data_for_bar(
        get_refine_data(
            Manufacturing_value_added_USD,
            cols,
            start_year,
            end_year),
        years),
    'Years',
    'Manufacturing value added GDP',
    'Manufacturing value added USD')
barplot(
    data_for_bar(
        get_refine_data(
            CO2_emissions,
            cols,
            start_year,
            end_year),
        years),
    'Years',
    "CO2 Emissions",
    "CO2 Emissions (kt)")
Forest_area = pd.read_csv('Forest_area.csv', skiprows=4)
Electric_power_consumption = pd.read_csv(
    'Electric_power_consumption.csv', skiprows=4)
Agricultural_land = pd.read_csv('Agricultural_land.csv', skiprows=4)
names = [
    'Agricultural_land',
    'Urban_population',
    'Manufacturing_GDP',
    'CO2_emissions',
    'total_population',
    'Electric_power_consumption',
    'Forest_area']
data_frames = [
    Agricultural_land,
    Urban_population,
    Manufacturing_value_added_USD,
    CO2_emissions,
    total_population,
    Electric_power_consumption,
    Forest_area]
country_name = ['Nigeria', 'Years']
make_corr_heat_map(
    get_data_for_specific_country(
        data_frames,
        country_name,
        names,
        '1990',
        '2020'),
    'Nigeria',
    'Dark2')
country_name = ['Philippines', 'Years']
make_corr_heat_map(
    get_data_for_specific_country(
        data_frames,
        country_name,
        names,
        '1990',
        '2020'),
    'Philippines',
    'nipy_spectral')
country_name = ['Pakistan', 'Years']
make_corr_heat_map(
    get_data_for_specific_country(
        data_frames,
        country_name,
        names,
        '1990',
        '2020'),
    'Pakistan',
    'rainbow')
pak_data = get_data_for_specific_country(
    data_frames, country_name, names, '1990', '2020')
draw_scatter_plot(
    pak_data['Manufacturing_GDP'],
    pak_data['Urban_population'],
    'Urban Population vs Manufacturing GDP in Pakistan',
    'Urban Population',
    'Manufacturing GDP',
    color='blue',
    marker='o',
    label='Scatter Points')
