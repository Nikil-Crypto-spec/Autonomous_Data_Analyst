"""
visualizer.py
---------------------------------------
Interactive Data Visualization Module
"""

import plotly.express as px
import plotly.graph_objects as go


class Visualizer:
    def __init__(self, dataframe):
        self.df = dataframe.copy()

    # ------------------------------------
    # Histogram
    # ------------------------------------
    def histogram(self, x, color=None, nbins=None):

        return px.histogram(
            self.df,
            x=x,
            color=color,
            nbins=nbins,
            template="plotly_white",
            title=f"Histogram of {x}",
        )

    # ------------------------------------
    # Bar Chart
    # ------------------------------------
    def bar_chart(self, x, y, color=None):

        return px.bar(
            self.df,
            x=x,
            y=y,
            color=color,
            template="plotly_white",
            title=f"{y} vs {x}",
        )

    # ------------------------------------
    # Line Chart
    # ------------------------------------
    def line_chart(self, x, y, color=None):

        return px.line(
            self.df,
            x=x,
            y=y,
            color=color,
            template="plotly_white",
            title=f"{y} vs {x}",
        )

    # ------------------------------------
    # Scatter Plot
    # ------------------------------------
    def scatter_plot(self, x, y, color=None, size=None):

        return px.scatter(
            self.df,
            x=x,
            y=y,
            color=color,
            size=size,
            template="plotly_white",
            title=f"{y} vs {x}",
        )

    # ------------------------------------
    # Box Plot
    # ------------------------------------
    def box_plot(self, x, color=None):

        return px.box(
            self.df,
            x=x,
            color=color,
            template="plotly_white",
            title=f"Box Plot of {x}",
        )

    # ------------------------------------
    # Violin Plot
    # ------------------------------------
    def violin_plot(self, x, color=None):

        return px.violin(
            self.df,
            x=x,
            color=color,
            box=True,
            points="all",
            template="plotly_white",
            title=f"Violin Plot of {x}",
        )

    # ------------------------------------
    # Pie Chart
    # ------------------------------------
    def pie_chart(self, names, values=None):

        if values is None:
            counts = self.df[names].value_counts()

            return px.pie(
                names=counts.index,
                values=counts.values,
                title=f"{names} Distribution",
            )

        return px.pie(
            self.df,
            names=names,
            values=values,
            title=f"{names} Distribution",
        )

    # ------------------------------------
    # Area Chart
    # ------------------------------------
    def area_chart(self, x, y, color=None):

        return px.area(
            self.df,
            x=x,
            y=y,
            color=color,
            template="plotly_white",
            title=f"{y} vs {x}",
        )

    # ------------------------------------
    # Correlation Heatmap
    # ------------------------------------
    def heatmap(self):

        corr = self.df.corr(numeric_only=True)

        fig = go.Figure(
            data=go.Heatmap(
                z=corr.values,
                x=corr.columns,
                y=corr.columns,
                colorscale="RdBu",
                zmin=-1,
                zmax=1,
                colorbar=dict(title="Correlation"),
            )
        )

        fig.update_layout(
            title="Correlation Heatmap",
            template="plotly_white",
        )

        return fig

    # ------------------------------------
    # Bubble Chart
    # ------------------------------------
    def bubble_chart(self, x, y, size=None, color=None):

        return px.scatter(
            self.df,
            x=x,
            y=y,
            size=size,
            color=color,
            template="plotly_white",
            title=f"Bubble Chart ({x} vs {y})",
        )

    # ------------------------------------
    # Density Heatmap
    # ------------------------------------
    def density_heatmap(self, x, y):

        return px.density_heatmap(
            self.df,
            x=x,
            y=y,
            template="plotly_white",
            title=f"Density Heatmap ({x} vs {y})",
        )

    # ------------------------------------
    # Sunburst
    # ------------------------------------
    def sunburst(self, path):

        if isinstance(path, str):
            path = [path]

        return px.sunburst(
            self.df,
            path=path,
        )

    # ------------------------------------
    # Treemap
    # ------------------------------------
    def treemap(self, path):

        if isinstance(path, str):
            path = [path]

        return px.treemap(
            self.df,
            path=path,
        )

    # ------------------------------------
    # Scatter Matrix
    # ------------------------------------
    def scatter_matrix(self, dimensions, color=None):

        return px.scatter_matrix(
            self.df,
            dimensions=dimensions,
            color=color,
        )

    # ------------------------------------
    # Parallel Coordinates
    # ------------------------------------
    def parallel_coordinates(self, color):

        return px.parallel_coordinates(
            self.df,
            color=color,
        )

    # ------------------------------------
    # Save HTML
    # ------------------------------------
    @staticmethod
    def save_html(fig, filename):

        fig.write_html(filename)