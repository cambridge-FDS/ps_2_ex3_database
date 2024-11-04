import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 1. Timeseries Visualisation ___________
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional

def validate_and_extract_args(kwargs):
    """Validate that 'data' is a DataFrame and 'x' and 'y' are strings."""
    if not isinstance(kwargs.get("data"), pd.DataFrame):
        raise ValueError("The 'data' argument must be a pandas DataFrame.")
    data = kwargs["data"]
    x = kwargs["x"]
    y = kwargs["y"]
    se_min = kwargs.get("se_min")
    se_max = kwargs.get("se_max")
    regression = kwargs.get("regression", False)
    title = kwargs.get("title", "")
    xlabel = kwargs.get("xlabel", x)
    ylabel = kwargs.get("ylabel", y)
    linecolor = kwargs.get("linecolor", "#1D428A")
    return data, x, y, se_min, se_max, regression, title, xlabel, ylabel, linecolor

def setup_plot_style():
    """Set up dark grid style for the plot."""
    sns.set_theme(style="darkgrid", rc={"axes.facecolor": "#222222", "grid.color": "#444444"})
    sns.set_context("talk")

def create_figure():
    """Create a matplotlib figure and axis."""
    fig, ax = plt.subplots(figsize=(14, 8), dpi=150, facecolor='#222222')
    return fig, ax

def plot_main_line(data, x, y, linecolor, ax):
    """Plot the main time series line with the specified color."""
    sns.lineplot(data=data, x=x, y=y, color=linecolor, linewidth=2, ax=ax)

def add_error_bands(data, x, se_min, se_max, linecolor, ax):
    """Add shaded error bands if available."""
    if se_min and se_max:
        ax.fill_between(data[x], data[se_min], data[se_max], color=linecolor, alpha=0.2)

def add_regression_line(data, x, y, ax):
    """Add a regression line to the plot if specified."""
    sns.regplot(data=data, x=x, y=y, scatter=False,
                line_kws={"color": "grey", "linestyle": "dotted", "linewidth": 1.5}, ax=ax)

def enhance_labels(ax, xlabel, ylabel, title):
    """Add labels and title to the plot."""
    ax.set_xlabel(xlabel, fontsize=14, color='white', labelpad=10)
    ax.set_ylabel(ylabel, fontsize=14, color='white', labelpad=10)
    ax.set_title(title, fontsize=20, weight='bold', color='white', pad=20)

def adjust_layout(fig):
    """Adjust layout to add space around elements."""
    fig.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9)

def time_series_plot(**kwargs) -> None:
    """
    Main function to plot a time series with options for error bands, labels, and styling.
    Calls helper functions to build the plot step-by-step.
    """
    # Validate and extract arguments
    data, x, y, se_min, se_max, regression, title, xlabel, ylabel, linecolor = validate_and_extract_args(kwargs)

    # Setup and create plot
    setup_plot_style()
    fig, ax = create_figure()
    plot_main_line(data, x, y, linecolor, ax)
    ax.tick_params(colors='white')
    add_error_bands(data, x, se_min, se_max, linecolor, ax)

    # Optionally add regression line
    if regression:
        add_regression_line(data, x, y, ax)

    enhance_labels(ax, xlabel, ylabel, title)
    adjust_layout(fig)
    plt.show()



# 2. Multi-Team Visualisation ___________
def validate_data(kwargs):
    """Validate and extract data from kwargs."""
    if not isinstance(kwargs.get("data"), pd.DataFrame):
        raise ValueError("The 'data' argument must be a pandas DataFrame.")
    return kwargs.get("data"), kwargs.get("x"), kwargs.get("y"), kwargs.get("group_by")

def setup_plot_style():
    """Set up the plot style and figure background."""
    sns.set_theme(style="darkgrid", rc={"axes.facecolor": "#222222", "grid.color": "#444444"})
    sns.set_context("talk")

def create_figure():
    """Create a matplotlib figure and axis."""
    fig, ax = plt.subplots(figsize=(14, 8), dpi=150, facecolor='#222222')
    return fig, ax

def plot_team_lines(data, x, y, main_team, linecolor, ax):
    """Plot each team's line with specified colors."""
    # Generate a desaturated color palette for non-main teams
    palette = sns.color_palette("crest", n_colors=data['team_name'].nunique())
    palette = [sns.desaturate(color, 0.3) for color in palette]

    # Loop through each team and plot
    for i, (team_name, team_data) in enumerate(data.groupby("team_name")):
        color = linecolor if team_name == main_team else palette[i]
        sns.lineplot(data=team_data, x=x, y=y, label=team_name, linewidth=2, ax=ax, color=color)

def add_labels(ax, xlabel, ylabel, title):
    """Add labels and title to the plot."""
    ax.set_xlabel(xlabel, fontsize=14, color='white', labelpad=10)
    ax.set_ylabel(ylabel, fontsize=14, color='white', labelpad=10)
    ax.set_title(title, fontsize=20, weight='bold', color='white', pad=20)
    ax.tick_params(colors='white')

def style_legend(ax, main_team):
    """Style the legend and highlight the main team."""
    handles, labels = ax.get_legend_handles_labels()
    sorted_handles_labels = sorted(zip(labels, handles), key=lambda x: (x[0] != main_team, x[0]))
    sorted_labels, sorted_handles = zip(*sorted_handles_labels)

    legend = ax.legend(sorted_handles, sorted_labels, loc='upper left', fontsize=12, frameon=True,
                       handlelength=2, borderpad=1.5, labelspacing=1.2)

    for text in legend.get_texts():
        team_name = text.get_text()
        text.set_color('white' if team_name == main_team else '#888888')

    legend.set_title(None)
    legend.get_frame().set_facecolor('#111111')
    legend.get_frame().set_alpha(0.9)
    legend.get_frame().set_edgecolor('#111111')
    legend.get_frame().set_linewidth(0)

def highlight_championship_years(ax, championship_years, main_team, linecolor):
    """Highlight championship years with shading and text annotation."""
    for i, (start_year, end_year) in enumerate(championship_years):
        start_date = pd.to_datetime(f'{start_year}-01-01')
        end_date = pd.to_datetime(f'{end_year}-12-31')
        ax.axvspan(start_date, end_date, color=linecolor, alpha=0.2)

        if i == 0:
            ax.text(start_date + pd.Timedelta(days=200), 0.97, f'{main_team} Western Conference Champions',
                    fontsize=11, color=linecolor, ha='left', va='top', transform=ax.get_xaxis_transform())

def adjust_layout(fig):
    """Adjust layout for better spacing around elements."""
    fig.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9)

def multi_team_visualisation(**kwargs) -> None:
    """
    Main function to visualize the moving average of a time series.
    Calls helper functions to build the plot step-by-step.
    """
    # Extract arguments
    data, x, y, group_by = validate_data(kwargs)
    title = kwargs.get("title", "")
    xlabel = kwargs.get("xlabel", x)
    ylabel = kwargs.get("ylabel", y)
    main_team = kwargs.get("main_team")
    linecolor = kwargs.get("linecolor", "#FFC72C")
    championship_years = kwargs.get("championship_years", [])

    # Setup and create plot
    setup_plot_style()
    fig, ax = create_figure()
    plot_team_lines(data, x, y, main_team, linecolor, ax)
    add_labels(ax, xlabel, ylabel, title)
    style_legend(ax, main_team)
    highlight_championship_years(ax, championship_years, main_team, linecolor)
    adjust_layout(fig)
    plt.show()
