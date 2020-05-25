"""
This module provides functionality to plot survey data.

This module is called by survey analysis scripts and is a helper module
which processes `pandas` data-frames as input and transforms them into
informative plots.
The actual plotting is done by utilizing a separate plotting library called
`matplotlib`.

.. currentmodule:: survey_analysis.plot
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""
import logging
from inspect import FrameInfo, getmodulename, stack
from pathlib import Path

from matplotlib import pyplot, rcParams
from pandas import DataFrame

from survey_analysis.globals import settings
from survey_analysis.settings import OutputFormat


def output_pyplot_image(output_file_stem: str = "") -> None:
    """
    Shorthand function to render pyplot images depending on output settings.

    Use this after construction a pyplot plot to display the plot or render it
    into an image depending on the application settings.
    (Basically instead of pyplot.show() or pyplot.savefig())


    Args:
        output_file_stem:   The stem of the desired filename
                            (without extension).
                            Defaults to an empty string which will prompt the
                            automatic generation of a file name from the date
                            of the run and the module producing the image.
    """
    if settings.output_format == OutputFormat.SCREEN:
        pyplot.show()
        pyplot.close()
        return

    if not output_file_stem:
        # Auto-generate the file stem

        # Get the calling module's name, assuming this function is called from
        # a survey evaluation script
        # Keep in mind that
        # * FrameInfo is a named tuple in which the second entry is the
        #   fully qualified module name
        # * The first element on the stack is this function, the caller is the
        #   second frame
        calling_module_frame: FrameInfo = stack()[1]
        calling_module_name: str = getmodulename(calling_module_frame[1])

        output_file_stem: str = f"{calling_module_name}"

    file_ending: str = settings.output_format.name.lower()
    file_name: str = f"{output_file_stem}.{file_ending}"
    output_subfolder: Path = settings.output_folder/settings.run_timestamp
    output_path: Path = output_subfolder/file_name

    if not output_subfolder.exists():
        output_subfolder.mkdir(parents=True)

    if output_path.exists():
        logging.warning(f"Overriding existing output file {output_path}")

    pyplot.savefig(f"{output_path}")
    pyplot.close()


def plot_bar_chart(data_frame: DataFrame,
                   plot_file_name: str = "",
                   **kwargs):
    """
    Plot given data-frame as a (stacked) bar chart.

    A pandas DataFrame is used as input data from which a (stacked) bar chart
    is generated. This DataFrame need be structured in a particular way.
    The actual data values are taken column by column and plotted as bars
    for each index entry.
    In case of a normal bar chart this means each sequence of bars / column
    is put next to each other while each sequence is grouped by the
    series / rows and labeled accordingly in the legend.
    By contrast in case of a stacked bar chart each sequence of bars / column
    is stacked on top of the previous instead of put next to each other and
    labeled accordingly in the legend.
    The index names are used to label the ticks along the x-axis, while the
    column names are used as labels in the legend.

    Args:
        data_frame(DataFrame): All data needed for this function to plot
            a stacked bar chart is encapsulated in this DataFrame.
        plot_file_name(str): Optional file name which is used to store the
            plot to a file. If this argument is an empty string which is the
            default for this argument, a suitable file name is auto-generated.
        **kwargs: All other arguments are passed as optional **kwargs.
            These optional parameters may contain a flag "stacked"
            to create a stacked bar chart, strings specifying the labels
            "plot_title", "x_axis_label", "y_axis_label" and data to
            position the legend with "legend_location" and "legend_anchor".
    """
    rcParams.update({'figure.autolayout': True})

    data_frame.plot(kind="bar", stacked=kwargs.get("stacked", False))

    ax = pyplot.gca()

    ax.set_title(kwargs.get("plot_title", ""))
    ax.set_xlabel(kwargs.get("x_axis_label", ""))
    ax.set_ylabel(kwargs.get("y_axis_label", ""))
    ax.set_xticklabels(data_frame.index.values,
                       rotation=45,
                       ha="right")

    ax.legend(data_frame.columns.values,
              loc=kwargs.get("legend_location", "best"),
              bbox_to_anchor=kwargs.get("legend_anchor", None))

    output_pyplot_image(plot_file_name)
