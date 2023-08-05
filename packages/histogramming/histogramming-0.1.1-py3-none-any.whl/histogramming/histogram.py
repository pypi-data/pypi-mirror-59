import pandas as pd
import numpy as np
import pickle


def from_pickle(path):
    return pickle.load(path)


class Histogram:
    """Histogram object.
    A histogram is has two basic properties: bins and counts. Additionally, it might carry information about the
    uncertainties (and a link to the original data).
    This library was created mostly to handle histogram operations: summing, diving and fitting. Using fill methods is
    considerably slow in comparison to other alternatives (e.g. Boost Histogram or ROOT). It is advisible to use it
    only to perform final data treatment.

    By default, errors are calculated as the square root of the sum of the square of the weights. The Sum of the squared
    weights is kept in each bin to allow for .

    Attributes
    ----------
    title: str
        Title of the Histogram
    data : pd.DataFrame
        Data of the histogram. It has three columns: 'Content', 'SumWeightSquare' and 'Error'.
        The index represents the axis of the histogram.
    range: pd.DataFrame
        This holds a view of data taking into consideration the ranges requested by the user.
        This range is used only for projections, all other operations (sum, multiplication etc) take place in data.
        #TODO: Methods to implement the range selection
    """

    def __init__(self, df=None, title='', axis_and_bins=None, axis=None):
        """" Default constructor.

        This is used mostly internally or as a copy constructor. Use from_dataframe in case you would like to create
        from a DataFrame that was already binned or from_dataframe_cut if it is not binned.

        Parameters
        ----------
        df : Histogram or pd.DataFrame or None
            DataFrame with the values which will be used to calculate the histogram.
        title: str
            title of the histogram
        """
        self.title = title
        if isinstance(df, Histogram):
            self.data = df.data.copy()
            if title == '':
                self.title = df.title
        elif df is None:
            self.data = pd.DataFrame(None, columns=['Content', 'SumWeightSquare', 'Error'])
        elif isinstance(df, pd.DataFrame):
            self.data = df.copy()  # copies to ensure that the new Histogram does not share the same DataFrame
        else:
            raise TypeError('The DataFrame should be pd.DataFrame, Histogram or None.')

        # Check if the content of the histogram is consistent
        if 'Content' not in self.data.columns or 'SumWeightSquare' not in self.data.columns:
            raise ValueError('The DataFrame passed does not have the Content, SumWeightSquare or Error')

        if 'Error' not in self.data.columns:
            self.data['Error'] = np.sqrt(self.data['SumWeightSquare'])

        cols_to_drop = [x for x in self.data.columns if x not in ['Content', 'Error', 'SumWeightSquare']]
        self.data.drop(labels=cols_to_drop, axis='columns', inplace=True)

        self.range = self.data  # range should be just a view of self.data

    @staticmethod
    def from_dataframe(df, axis, title=''):
        """Create a n-dimensional histogram from df. The dataframe df should have been binned before passing
        it to this class. Each value passed in axis will be grouped by and it should be binned.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame with the values which will be used to calculate the histogram.

        axis: str, tuple or list
            The features which will aggregated in the histogram (which one is a different 'axis'). The features should
            have been binned before passing df to this function

        title: str
            the title of the histogram

        Returns
        -------
        Histogram
            A new histogram with df
        """

        if isinstance(axis, str):
            axis = [axis]

        if not isinstance(df, pd.DataFrame):
            raise TypeError('df should be a DataFrame')

        df_local = df.copy()

        if 'Weight' not in df_local.columns:
            df_local['Weight'] = 1.0

        df_local['WeightSquare'] = df_local['Weight'] ** 2

        grouped = df_local.groupby(by=axis).sum().fillna(0.)

        # Counts are the sum of the Weights
        counts = pd.DataFrame(grouped['Weight'])

        counts.columns = ['Content']
        # Sums the WeightSquare to keep the information used for the error calculation
        counts['SumWeightSquare'] = grouped['WeightSquare']
        # Creates a error columns to make it easier to read
        counts['Error'] = np.sqrt(counts["SumWeightSquare"])

        return Histogram(counts, title)

    @staticmethod
    def from_dataframe_cut(df, axis_and_bins, title=''):
        """Create a n-dimensional histogram from df. The dataframe df will be cut using the information from
        axis_and_bins.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame with the values which will be used to calculate the histogram.

        axis_and_bins: dict
            dict with the axis names and its bins. Example: {'x' : [0, 1., 3.,], 'y': 50)
            The values will be passed to pd.cut, any type accepted by pd.cut can be used here.
        title:
            the title of the histogram

        Returns
        -------
        Histogram
            This histogram (a new histogram object)
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError('df should be a DataFrame')

        df_local = df.copy()

        for key, values in axis_and_bins.items():
            df_local[key] = pd.cut(df[key], bins=values)

        return Histogram.from_dataframe(df_local, axis_and_bins.keys(), title)

    @staticmethod
    def from_root(root_hist):
        # TODO: finish implementation
        try:
            import ROOT
        except ModuleNotFoundError:
            raise (ModuleNotFoundError, 'ROOT is needed to use from_root. Please be sure that it can be imported.')

        if not isinstance(root_hist, ROOT.TH1):
            raise (TypeError, 'ROOT histogram should be derive from TH1. Please check the histogram passed.')

        axis = (root_hist.GetXaxis())
        if isinstance(root_hist, ROOT.TH2):
            axis.append(root_hist.GetYaxis())
        elif isinstance(root_hist, ROOT.TH3):
            axis.append(root_hist.GetYaxis(), root_hist.GetZaxis())

        axis_names = list()
        axis_bins = list()
        axis_counts = list()
        axis_errors = list()

        for ax, i in zip(axis, range(len(axis))):
            if ax.GetTitle() == '':  # Add the number of the axis in case no title is available
                axis_names.append(str(i))
            else:
                axis_names.append(ax.GetTitle())

            bins = [ax.GetBinLowEdge(i) for i in range(ax.GetNbins())]
            bins.append(ax.GetBinUpEdge(ax.GetNbins()))
            axis_bins.append(bins)

    def from_range(self):
        """Create a new n-dimensional histogram from the current histogram using the range defined by the user using
        the function set_range. The dimension of the new histogram is the same of the current histogram.

        Returns
        -------
        range_histogram : pd.DataFrame
            A new histogram in the requested range.
        """
        return Histogram(self.range)

    def get_axis_names(self):
        return list(self.data.index.names)

    def get_bins(self, axis):
        """Returns the bins for axis

         Parameters
        ----------
        axis: str
            The axis which the bins will be calculated

        Returns
        -------
        bins : list
            bins of axis.

        """
        try:
            left_side = list(self.data.index.get_level_values(axis).categories.values.left)
            right_side = self.data.index.get_level_values(axis).categories.values.right
        except AttributeError:
            left_side = list(self.data.index.get_level_values(axis).left)
            right_side = self.data.index.get_level_values(axis).right

        bins = left_side + [right_side[-1]]
        bins = [float(x) for x in bins]
        return bins

    def get_n_bins(self, axis):
        """Returns the number of bins for axis

         Parameters
        ----------
        axis: str
            The axis which the bins will be calculated

        Returns
        -------
        bins : list
            bins of axis.

        """
        return len(self.get_bins(axis)) - 1

    def get_bin_categories(self, axis):
        """Returns the bin intervals for axis in the form a series of pd.Interval
        Useful to operate in the bins
         Parameters
        ----------
        axis: str
            The axis which the bins will be calculated

        Returns
        -------
        bins : list
            bins of axis.

        """
        return pd.Series(self.data.index.get_level_values(axis).categories)

    def get_bin_center(self, axis):
        """Returns the central value for each bin in axis.

         Parameters
        ----------
        axis: str
            The axis which the bins will be calculated

        Returns
        -------
        center : list
            center of the bins of axis.
        """
        try:
            center = list(self.data.index.get_level_values(axis).categories.values.mid)
        except AttributeError:
            center = list(self.data.index.get_level_values(axis).mid)
        center = [float(x) for x in center]
        return center

    def get_bin_width(self, axis):
        """Returns the central value for each bin in axis.

         Parameters
        ----------
        axis: str
            The axis which the bins will be calculated

        Returns
        -------
        width : list
            the length of the bins on the axis
        """
        try:
            width = list(self.data.index.get_level_values(axis).categories.values.length)
        except AttributeError:
            width = list(self.data.index.get_level_values(axis).length)
        width = [float(x) for x in width]
        return width

    def project(self, axis):
        """ Project the histogram to the axis listed in axis (multiple axis are supported). Uses ranges specified with
        set_range.

        Parameters
        ----------
        axis: str or list-like
            axis which the histogram will be projected

        Returns
        -------
        projection : Histogram
            A new Histogram that represents the histogram in the dimensions specified in axis
        """
        if isinstance(axis, str):
            axis = [axis]
        projection = self.range.reset_index().groupby(by=list(axis))['Content', 'SumWeightSquare'].sum()
        projection['Error'] = np.sqrt(projection["SumWeightSquare"])
        projection = Histogram(projection)

        return projection

    def __add__(self, other):
        if not isinstance(other, Histogram):
            raise ValueError('The + operator is only defined between two histograms.')

        # Check if the two histograms have the same dimensions
        if not self.data.index.equals(other.data.index):
            print(self.data.index)
            print(other.data.index)
            raise ValueError("The axis of the histograms do not match.")

        # Adds the  contents of the two histogram by summing ['Content', 'SumWeightSquare', 'Error']
        # This is correct for both Content and SumWeightSquare, but the error needs to be recalculated
        new_df = self.data + other.data
        # Recalculate the errors as the square root of the sum of the square of the weights
        new_df['Error'] = np.sqrt(new_df["SumWeightSquare"])

        return Histogram(new_df)

    def __sub__(self, other):
        if not isinstance(other, Histogram):
            raise ValueError('The - operator is only defined between two histograms.')

        # Check if the two histograms have the same dimensions
        if not self.data.index.equals(other.data.index):
            raise ValueError("The axis of the histograms do not match.")

        # Subtracts the contents of the two histogram
        new_df = self.data.copy()
        # The content is subtracted
        new_df['Content'] = self.data['Content'] - other.data['Content']
        # The errors are summed
        new_df['SumWeightSquare'] = self.data['SumWeightSquare'] + other.data['SumWeightSquare']
        # Recalculate the errors as the square root of the sum of the square of the weights
        new_df['Error'] = np.sqrt(new_df["SumWeightSquare"])

        return Histogram(new_df)

    def __mul__(self, other):

        if not isinstance(other, (int, float)) and not isinstance(other, Histogram):
            raise ValueError("Multiplication is defined only for histogram times scalar or other histogram.")

        if isinstance(other, (int, float)):
            new_df = self.data.copy()

            # Multiplication: content * value, error * value, w2 * (value**2)
            new_df['Content'] = self.data['Content'] * other

            new_df['SumWeightSquare'] = self.data['SumWeightSquare'] * (other ** 2.)
            new_df['Error'] = self.data['Error'] * other

            return Histogram(new_df)

        if isinstance(other, Histogram):
            if not self.data.index.equals(other.data.index):
                raise ValueError("The axis of the histograms do not match. You can create a range if necessary.")

            new_df = self.data.copy()

            # Multiplication value by value
            new_df['Content'] = self.data['Content'] * other.data['Content']

            # Errors are a bit more complicated. e = new_df * sqrt( (error_1)^2/content^2 + (error_1)^2/content^2) )
            new_df['Error'] = new_df['Content'] * np.sqrt(self.data['SumWeightSquare'] / (self.data['Content'] ** 2) +
                                                          other.data['SumWeightSquare'] / (other.data['Content'] ** 2))

            new_df['SumWeightSquare'] = new_df['Error'] ** 2

            return Histogram(new_df)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if not isinstance(other, (int, float)) and not isinstance(other, Histogram):
            raise ValueError("Division is defined only for histogram/scalar or other histogram/histogram.")

        # Check if histogram is divided by a float
        if isinstance(other, (int, float)):
            # In this case, return the multiplication by the inverse of other
            if other == 0.:
                raise ZeroDivisionError('It is not possible to divide by zero.')
            return self * (1.0 / other)

        if isinstance(other, Histogram):
            if not self.data.index.equals(other.data.index):
                raise ValueError("The axis of the histograms do not match.")

            new_df = self.data.copy()

            # Division value by value
            new_df['Content'] = self.data['Content'] / other.data['Content']

            # Errors are a bit more complicated. e = new_df * sqrt( (error_1)^2/content^2 + (error_1)^2/content^2) )
            new_df['Error'] = new_df['Content'] * np.sqrt(self.data['SumWeightSquare'] / (self.data['Content'] ** 2) +
                                                          other.data['SumWeightSquare'] / (other.data['Content'] ** 2))

            new_df['SumWeightSquare'] = new_df['Error'] ** 2

            return Histogram(new_df)

    def multi_plot1d(self, axis, **kwargs):
        groups_to_groupby = self.get_axis_names()
        groups_to_groupby.remove(axis)
        return self.data.groupby(groups_to_groupby).apply(lambda x: Histogram(x).plot1d(axis, **kwargs))

    def decompose_in_single_histograms(self, axis):
        groups_to_groupby = self.get_axis_names()
        groups_to_groupby.remove(axis)
        return self.data.groupby(groups_to_groupby).apply(lambda x: Histogram(x))

    def plot1d(self, axis, ax=None, plot_type='error_bar', label='', norm_hist=False, **kwargs):
        """ Plot the histogram in one dimension. Uses matplotlib errorbar or bar or bar.

        Parameters
        ----------
        axis: str
            axis which the histogram will be plotted.
        ax: plt.axes
            Axes used to plot the histogram. A new object is created if ax=None.
        plot_type: str
            Type of the plot. It can be error_bar (show errors in y) or bar.
        norm_hist: bool
            If True, the contents is divided by the sum of contents. The errors are properly scaled, but do not take
            error of the sum.
        label: str
            Label of the plot.

        Returns
        -------
        ax : plt.axes
            Axes with the histogram plotted.

        """
        import matplotlib.pyplot as plt

        if ax is None:
            fig, ax = plt.subplots()

        x = np.array(self.get_bin_center(axis))
        y = np.array(self.range['Content'])
        y_err = np.array(self.range['Error'])
        x_err = np.array(self.get_bin_width(axis)) / 2

        if norm_hist:
            y = y / y.sum()
            y_err = y_err / y.sum()

        y = list(y)
        x = list(x)
        y_err = list(y_err)
        x_err = list(x_err)

        kwargs.update({'label': label})

        if plot_type == 'error_bar':
            ax.errorbar(x, y, yerr=y_err, xerr=x_err, fmt='o', **kwargs)
        elif plot_type == 'bar':
            ax.bar(x, y, width=2. * np.array(x_err), **kwargs)
        else:
            raise AttributeError('Plot not defined')

        return ax

    def plot2d(self, axis, ax=None, plot_type='error_bar', label='', **kwargs):
        """ Plot the histogram in one dimension. Uses matplotlib errorbar or bar or bar.

        Parameters
        ----------
        axis: str
            axis which the histogram will be plotted.
        ax: plt.axes
            Axes used to plot the histogram. A new object is created if ax=None.
        plot_type: str
            Type of the plot. It can be error_bar (show errors in y) or bar.
        norm_hist: bool
            If True, the contents is divided by the sum of contents. The errors are properly scaled, but do not take
            error of the sum.
        label: str
            Label of the plot.

        Returns
        -------
        ax : plt.axes
            Axes with the histogram plotted.

        """
        import matplotlib.pyplot as plt

        if ax is None:
            fig, ax = plt.subplots()

        data_local = self.data.reset_index()

        x = list(data_local[axis[0]].categories.values.mid)
        y = list(data_local[axis[1]].categories.values.mid)
        weights = list(data_local['Content'])

        bins_x = self.get_bins(axis[0])
        bins_y = self.get_bins(axis[1])

        ax.hist2d(x, y, [bins_x, bins_y], weights=weights)

        return ax

    def normalize(self, inplace=False):
        """ Normalize the current histogram by the sum of the contents.

        Parameters
        ----------
        inplace: bool
            If true, the current histogram is modified.

        Returns
        -------
        self : Histogram
            the current histogram
        """

        if inplace:
            self.data['Content'] = self.data['Content'] / self.data['Content'].sum()
            self.data['Error'] = self.data['Error'] / self.data['Content'].sum()
            self.data['SumWeightSquare'] = self.data['Error'] * self.data['Error']
            return self
        else:
            return Histogram((self / self.data['Content'].sum()).data)

    def cumsum(self, axis=None, reverse_order=False, inplace=False):
        """ Calculate the cumulative sum of the bin contents. The uncertainties are propagated using the the cumulative
        sum of the sum of the squared weight

        Parameters
        ----------
        axis: str or NOne
            Name of the axis that will be summed. If none,
        reverse_order: bool
            If true, the cumulative sum is performed from the last to the first bin
        inplace: bool
            If true, the current histogram is modified. If there are axis is provided, inplace is ignored


        Returns
        -------
        self : Histogram
            the current histogram or the new histogram (i
        """
        if axis is not None:
            if not isinstance(axis, str):
                raise TypeError('Cumsum is only possible in one axis.')
        elif isinstance(axis, str):
            return self.project(axis).cumsum(axis=None, reverse_order=reverse_order, inplace=True)

        if inplace:
            if reverse_order:
                self.data['Content'] = np.cumsum(self.data['Content'].values[::-1])[::-1]
                self.data['SumWeightSquare'] = np.cumsum(self.data['SumWeightSquare'].values[::-1])[::-1]

            else:
                self.data['Content'] = self.data['Content'].cumsum()
                self.data['SumWeightSquare'] = self.data['SumWeightSquare'].cumsum()

            self.data['Error'] = np.sqrt(self.data['SumWeightSquare'])

            return self
        else:
            return Histogram(self).cumsum(reverse_order=reverse_order, inplace=True)

    def to_pickle(self, path):
        pickle.dump(self, path)

