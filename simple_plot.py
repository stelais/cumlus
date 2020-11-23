from bokeh.models import Whisker, ColumnDataSource, Span, BoxAnnotation
from bokeh.plotting import figure, show

#from visualization.data_reader import data_collector


def plotter(x_axis, y_axis, y_error, p, legend_label='', x_label_name='Days', y_label_name='Magnification', color='purple',
            plot_errorbar=False, t0_error_plot=False, t0=None, t0_error=None, type_plot='circle',
            plot_baseline=False, legend_location="bottom_center"):
    """
    Produce plot for the event

    :return: None
    """

    p.xaxis.axis_label = x_label_name
    p.yaxis.axis_label = y_label_name

    if type_plot == 'line':
        p.line(x_axis, y_axis, line_width=2, line_alpha=1.0, legend_label=legend_label, color=color)
    else:
        p.circle(x_axis, y_axis, fill_alpha=0.7, size=5, legend_label=legend_label, color=color)

    if plot_errorbar:
        upper = [x + e for x, e in zip(y_axis, y_error)]
        lower = [x - e for x, e in zip(y_axis, y_error)]
        source = ColumnDataSource(data=dict(groups=x_axis, counts=y_axis, upper=upper, lower=lower))
        whisker_errorbar = Whisker(source=source, base="groups", upper="upper", lower="lower",
                                   line_width=1.0, line_color=color) #level="overlay",
        whisker_errorbar.upper_head.line_color = color
        whisker_errorbar.lower_head.line_color = color
        p.add_layout(whisker_errorbar)
        #p.legend.glyph_height =  20
        #p.legend.glyph_width =  # some int


    if t0_error_plot:
        t0_location = Span(location=t0,
                           dimension='height', line_color='red',
                           line_dash='dashed', line_width=1)
        p.add_layout(t0_location)

        box = BoxAnnotation(left=(t0 - t0_error), right=(t0 + t0_error),
                            line_width=1, line_color='black', line_dash='dashed',
                            fill_alpha=0.2, fill_color='orange')

        p.add_layout(box)

    if plot_baseline:
        horizontal_line = Span(location=0, dimension='width', line_color='grey', line_width=2, line_alpha=0.8)
        p.add_layout(horizontal_line)

    p.legend.background_fill_alpha = 0.0
    p.legend.location = legend_location
    p.legend.label_text_font_size = '8pt'

    return p


if __name__ == '__main__':
    data_filepath = "/Users/sishitan/Documents/Analysis_MOA2020-135/data/KB200579_i_CFHT.dat"
    # times, magnitudes, magnitudes_err = data_collector(data_filepath, 'CFHT')
    p = figure(title="Lightcurve CFHT", plot_width=900, plot_height=300)
    p = plotter(times, magnitudes, magnitudes_err, p, 'CFHT', 'Magnitude')
    show(p)
