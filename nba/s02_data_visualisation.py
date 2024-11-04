from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Optional

def time_series_plot(**kwargs) -> None:
    """
    Function to plot a time series plot with customizable arguments passed as kwargs.
    Args:
        data (pd.DataFrame): The data to plot.
        x (str): The column name to use for the x-axis.
        y (str): The column name to use for the y-axis.
        se_min (Optional[str]): The column name for the lower bound of error shading (optional).
        se_max (Optional[str]): The column name for the upper bound of error shading (optional).
        regression (Optional[bool]): Whether to include a regression line (default is False).
        title (str): The title of the plot.
        xlabel (str): Label for the x-axis.
        ylabel (str): Label for the y-axis.
        linecolor (str): The color of the main line plot.
    Returns:
        plt.Figure: The function returns the figure for further customization.
    """
    # Can you ensure that "data" is a DataFrame and "x" and "y" are strings?
    if not isinstance(kwargs.get("data"), pd.DataFrame):
        raise ValueError("The 'data' argument must be a pandas DataFrame.")
    data = kwargs.get("data")
    x = kwargs.get("x")
    y = kwargs.get("y")
    se_min = kwargs.get("se_min")
    se_max = kwargs.get("se_max")
    regression = kwargs.get("regression", False)
    title = kwargs.get("title", "")
    xlabel = kwargs.get("xlabel", x)
    ylabel = kwargs.get("ylabel", y)
    linecolor = kwargs.get("linecolor", "#1D428A")

    # Setting a dark style for the entire plot, including outer space
    sns.set_theme(style="darkgrid", rc={"axes.facecolor": "#222222", "grid.color": "#444444"})

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(14, 8), dpi=150, facecolor='#222222')

    # Customizing the font and resolution
    sns.set_context("talk")

    # Main line plot with specified color
    sns.lineplot(
        data=data,
        x=x,
        y=y,
        color=linecolor,
        linewidth=2,
        ax=ax
    )

    # Adding shaded error bands if available
    if se_min and se_max:
        ax.fill_between(
            data[x],
            data[se_min],
            data[se_max],
            color=linecolor,
            alpha=0.2
        )

    # Adding a regression line if specified
    if regression:
        sns.regplot(
            data=data,
            x=x,
            y=y,
            scatter=False,
            line_kws={"color": "grey", "linestyle": "dotted", "linewidth": 1.5},
            ax=ax
        )

    # Enhancing labels and title
    ax.set_xlabel(xlabel, fontsize=14, color='white', labelpad=10)
    ax.set_ylabel(ylabel, fontsize=14, color='white', labelpad=10)
    ax.set_title(title, fontsize=20, weight='bold', color='white', pad=20)

    # Make axis ticks and labels white for readability on a dark background
    ax.tick_params(colors='white')

    # Increase space around elements
    fig.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9)
    fig.show()
    return None
