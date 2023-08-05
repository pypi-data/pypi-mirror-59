"""
BiFrame for data synthesis.
"""

import logging
import numpy as np
import pandas as pd

from pandas import Index
from sklearn.model_selection import train_test_split

from ds4mllib.dataset import DataSet
from ds4mllib.utils import train_and_predict, normalize_range
from ds4mllib.metrics import jensen_shannon_divergence, relative_error

logger = logging.getLogger(__name__)


class BiFrame(object):
    def __init__(self, first: pd.DataFrame, second: pd.DataFrame):
        """
        BiFrame class that contains two data sets, which currently provides
        kinds of analysis methods from distribution, correlation, and some
        machine learning tasks.
        Especially, if the input data sets are source and synthesized dataset,
        this class can be used to evaluate the utility and privacy of
        synthesized data set.

        Parameters
        ----------
        first : {pandas.DataFrame}
            first data set

        second : {pandas.DataFrame}
            second data set, i.e. synthesized ata
        """
        # distribution
        self._dt = {}

        # To compare two data set, make sure that they have same columns.
        # If not, compare the common part.
        common = set(first.columns) & set(second.columns)
        if len(common) != len(first.columns) or len(common) != len(second.columns):
            logger.info(f"BiFrame constructed on attributes: {common}.")

        # left and right data set (ds)
        self.first = DataSet(first[common])
        self.second = DataSet(second[common])
        self._columns = self.first.columns.sort_values().to_list()

        # Make sure that two dataset have same domain for categorical
        # attributes, and same min, max values for numerical attributes.
        for col in self._columns:
            # If current column is not categorical, will ignore it.
            if not self.first[col].categorical or not self.second[col].categorical:
                continue
            d1, d2 = self.first[col].domain, self.second[col].domain
            if not np.array_equal(d1, d2):
                if self.first[col].categorical:
                    domain = np.unique(np.concatenate((d1, d2)))
                else:
                    domain = [min(d1[0], d2[0]), max(d1[1], d2[1])]
                self.first[col].domain = domain
                self.second[col].domain = domain

    @property
    def columns(self):
        return self._columns

    def err(self):
        """
        Return pairwise err (relative error) of columns' distribution.
        """
        # merge two frequency counts, and calculate relative difference
        df = pd.DataFrame(columns=self._columns, index=['err'])
        df.fillna(0)
        for col in self._columns:
            df.at['err', col] = relative_error(self.first[col].counts(),
                                               self.second[col].counts())
        return df

    def jsd(self):
        """
        Return pairwise JSD (Jensen-Shannon divergence) of columns'distribution.
        """
        df = pd.DataFrame(columns=self._columns, index=['jsd'])
        df.fillna(0)
        for col in self._columns:
            df.at['jsd', col] = jensen_shannon_divergence(
                self.first[col].counts(), self.second[col].counts())
        return df

    def corr(self):
        """
        Return pairwise correlation and dependence measured by mi (mutual
        information).
        """
        return self.first.mi(), self.second.mi()

    def dist(self, column):
        """
        Return frequency distribution of one column.

        Parameters
        ----------
        column : str
            column name, whose distribution will be return
        """
        if len(self._dt) == 0:
            for c in self._columns:
                self._dt[c] = {}
                if self.first[c].categorical:
                    bins = self.first[c].domain
                    counts1 = self.first[c].counts(bins=bins)
                    counts2 = self.second[c].counts(bins=bins)
                else:
                    min_, max_ = self.first[c].domain
                    # the domain from two data set are same;
                    # extend the domain to human-readable range
                    bins = normalize_range(min_, max_ + 1)
                    counts1 = self.first[c].counts(bins=bins)
                    counts2 = self.second[c].counts(bins=bins)
                    # Note: index, value of np.histogram has different length
                    bins = bins[:-1]
                self._dt[c]['bins'] = bins
                # stack arrays vertically
                self._dt[c]['counts'] = np.vstack((counts1, counts2))
        return self._dt[column]['bins'], self._dt[column]['counts']

    def describe(self):
        """
        Give descriptive difference between two data sets, which concluded
        relative errors, and jsd divergence.
        Return a panda.DataFrame, whose columns are two dataset's columns, and
        indexes are a array of metrics, e.g. ['err', 'jsd'].
        """
        df1 = self.err()
        df2 = self.jsd()
        return pd.concat([df1, df2])

    def classify(self, label: str, test: pd.DataFrame = None):
        """
        Train two svm classifiers based on data sets, and predict class labels
        for test data. Return both error rates.

        Parameters
        ----------
        label : str
            classifier feature, key is one column in left data frame.
            It supports two-class and multi-class.

        test : {pandas.DataFrame}
            test frame, is test data for machine learning algorithms. If it is
            not provided, it will split 20% of left data frame as test data.

        Returns
        -------
        a DataFrame, e.g.
                         target                         source     target
                      male female                    male female male female
        source male   1    3        or actual male   1    3      1    2
               female 2    4                  female 2    4      3    4
        """
        if (not self.first[label].categorical or
                not self.second[label].categorical):
            raise ValueError(
                f'Classifier can\'t run on non-categorical column: {label}')
        from sklearn.metrics import confusion_matrix

        def split_feature_label(df: pd.DataFrame):
            # TODO need improve sub_cols
            sub_cols = [attr for attr in df.columns if attr.startswith(label)]
            if len(sub_cols) == 0:
                return df, None
            is_one_class = len(sub_cols) == 2
            if is_one_class:
                # For one class, there are two sorted values.
                # e.g. ['Yes', 'No'] => [[0, 1],
                #                        [1, 0]]
                # Here it should choose second column to represent this attribute.
                label_ = sub_cols[1]
                return df.drop(sub_cols, axis=1), df[label_]
            else:
                try:
                    # merge multiple column into one: [Name_A, Name_B, ..] => Name
                    _y = df[sub_cols].apply(lambda x: Index(x).get_loc(1),
                                            axis=1)
                    return df.drop(sub_cols, axis=1), _y
                except KeyError as e:
                    print(e)
                    print(sub_cols)
                    print(df[sub_cols])

        # If test dataset is not provided, then split 20% of source dataset for testing.
        if test is None:
            lt, test = train_test_split(self.first, test_size=0.2)
            rt, _ = train_test_split(self.second, test_size=0.2)
        else:
            lt = self.first
            rt = self.second
        ts = self.first.encode(data=lt)
        lt_x, lt_y = split_feature_label(ts)
        test_x, test_y = split_feature_label(self.first.encode(data=test))
        rt_x, rt_y = split_feature_label(self.first.encode(data=rt))

        # construct svm classifier, and predict
        lt_yp = train_and_predict(lt_x, lt_y, test_x)
        rt_yp = train_and_predict(rt_x, rt_y, test_x)

        columns = self.first[label].bins
        labels = range(len(columns))
        # If test dataset has class label, return two expected score.
        if label in test:
            lcm = confusion_matrix(test_y, lt_yp, labels=labels)
            rcm = confusion_matrix(test_y, rt_yp, labels=labels)
            # lcm = lcm.astype('float') / lcm.sum(axis=1)
            # rcm = rcm.astype('float') / rcm.sum(axis=1)
            return (pd.DataFrame(lcm, columns=columns, index=columns),
                    pd.DataFrame(rcm, columns=columns, index=columns))
        # If test dataset don't have class label, return their expected values.
        else:
            cm = confusion_matrix(lt_yp, rt_yp, labels=labels)
            return pd.DataFrame(cm, columns=columns, index=columns)

    def to_html(self, buf=None, title='Evaluation Report', info=True,
                distribute=True, correlate=True, classifier=None, labels=None,
                test=None):
        """
        Render the evaluation result of two data set as an HTML file.

        Parameters
        ----------
        buf : optional
            buffer to write to

        title : str
            title of evaluation report

        info : bool, default true
            show basic information of two data set, including relative error,
            and Jensen-Shannon divergence (jsd).

        distribute : bool, default true
            show distribution of each attribute.

        correlate : bool, default true
            show correlation of pair-wise attributes.

        classifier : str
            use classifier to train data set on one or more columns (defined by
            parameter 'label') and show prediction result on the evaluation
            report. Optional classifier: SVM.

        labels : list of column names
            column name, or a list of column names separated by comma, used for
            classification task.

        test : pd.DataFrame
            test data for classification, and other machine learning tasks.
        """
        from ds4mllib.utils import (plot_histogram, plot_heatmap,
                                 plot_confusion_matrix)
        from mako.template import Template
        import os
        old_cwd = os.getcwd()
        os.chdir(os.path.dirname(__file__))
        template = Template(filename='template/report.html')
        os.chdir(old_cwd)

        topics = []
        content = {}
        # format different kinds of evaluation result to unified style
        if info:
            topics.append('basic')
            content['basic'] = [self.describe().to_dict('split')]

        if distribute:
            topics.append('dist')
            content['dist'] = []
            for col in self.columns:
                bins, counts = self.dist(col)
                svg = plot_histogram(bins, counts)
                content['dist'].append({'name': col, 'columns': bins,
                                        'data': counts, 'path': svg})
        if correlate:
            topics.append('corr')
            content['corr'] = []
            source_mi, target_mi = self.corr()
            source_svg = plot_heatmap(source_mi)
            target_svg = plot_heatmap(target_mi)
            content['corr'].append({'matrix': source_mi.to_dict('split'),
                                    'path': source_svg})
            content['corr'].append({'matrix': target_mi.to_dict('split'),
                                    'path': target_svg})

        if labels is not None:
            topics.append('svm')
            content['svm'] = []
            for col in labels:
                in_test = (test is not None and col in test) or (test is None)
                if in_test:
                    # When class label in svm classify test data, try to match
                    # two predicted result with the actual data, and so, there
                    # will be two confusion matrix diagrams.
                    try:
                        source_cm, target_cm = self.classify(col, test=test)
                        vrange = (
                            min(source_cm.values.min(), target_cm.values.min()),
                            max(source_cm.values.max(), target_cm.values.max()))
                        path = (
                            plot_confusion_matrix(source_cm, vrange=vrange,
                                                  xlabel='raw',
                                                  ylabel='actual'),
                            plot_confusion_matrix(target_cm, vrange=vrange,
                                                  xlabel='synth',
                                                  ylabel='actual'))
                        content['svm'].append({'column': col, 'path': path})
                    except ValueError as e:
                        print(e)
                else:
                    # If not, will compare two predicted result.
                    try:
                        cm = self.classify(col, test=test)
                        # make path's type: 1-tuple
                        path = (plot_confusion_matrix(cm, xlabel='synth',
                                                      ylabel='raw'),)
                        content['svm'].append({'column': col, 'path': path})
                    except ValueError as e:
                        print(e)

        svms = content['svm'] if 'svm' in content else []
        if buf:
            with open(buf, 'w+', encoding='utf-8') as file:
                file.write(template.render(title=title,
                                           basics=content['basic'],
                                           dists=content['dist'],
                                           corrs=content['corr'],
                                           svms=svms))
