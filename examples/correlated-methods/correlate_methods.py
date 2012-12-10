# -*- coding: utf-8 -*
from __future__ import division
from brightway2 import *
from bw2calc import *
from candidates import CANDIDATES
from scipy import sparse, stats
import cPickle as pickle
import itertools
import matplotlib.pyplot as plt
import numpy as np
import os
import progressbar


class MethodCorrelator(object):
    def __init__(self):
        self.output_dir = config.request_dir("big")

    def correlate(self, candidates=CANDIDATES):
        print "Correlating LCIA results"
        ei = Database("ecoinvent 2.2")
        ei_data = ei.load()
        candidates = sorted(candidates)
        num_methods = len(candidates)
        num_processes = len(ei_data)

        output = np.zeros((num_processes, num_methods), dtype=np.float32)

        widgets = ['Calculations: ', progressbar.Percentage(), ' ',
            progressbar.Bar(marker=progressbar.RotatingMarker()), ' ',
            progressbar.ETA()]
        pbar = progressbar.ProgressBar(widgets=widgets,
            maxval=num_processes
            ).start()

        lca = LCA({ei_data.keys()[0]: 1}, method=candidates[0])
        lca.lci(factorize=True)
        lca_methods = dict([(key, self.build_ia_matrix(key, lca)
            ) for key in candidates])
        for row, key in enumerate(sorted(ei_data.keys())):
            if mapping[key] not in lca.technosphere_dict:
                continue
            lca.build_demand_array({key: 1})
            vector = lca.biosphere_matrix.data * lca.solve_linear_system()
            for col, key in enumerate(candidates):
                output[row, col] = (lca_methods[key] * vector).sum()

            pbar.update(row)

        pbar.finish()
        return output, \
            dict((y, x) for x, y in enumerate(candidates)), \
            dict((y, x) for x, y in enumerate(sorted(ei_data.keys())))

    def build_ia_matrix(self, key, lca):
        lca.method = key
        lca.load_method()
        count = len(lca.biosphere_dict)
        return sparse.coo_matrix(
            (lca.cf_params['amount'],
            (np.zeros(lca.cf_params['index'].shape[0],),
            lca.cf_params['index'])),
            (count, count)).tocsr()

    def create_correlation_matrix(self, output):
        print "Creating correlation matrix"
        num_methods = output.shape[1]
        results = np.zeros((num_methods, num_methods))
        count = itertools.count()
        count.next()

        widgets = ['Correlations: ', progressbar.Percentage(), ' ',
            progressbar.Bar(marker=progressbar.RotatingMarker()), ' ',
            progressbar.ETA()]
        pbar = progressbar.ProgressBar(widgets=widgets,
            maxval=num_methods * (num_methods + 1) / 2
            ).start()

        for row in range(num_methods):
            for col in range(num_methods):
                if col <= row:
                    continue
                data1 = output[:, row]
                data2 = output[:, col]
                pbar.update(count.next())
                mask = (data1 != 0) * (data2 != 0)
                if mask.sum() == 0:
                    continue
                results[row, col] = stats.spearmanr(data1[mask], data2[mask]
                    )[0]

        pbar.finish()

        results = results + results.T
        results[results == 0] = 1
        return np.abs(results)

    def choose_methods(self, corrs):
        choice = list(np.unravel_index(corrs.argmin(), corrs.shape))
        for x in range(4):
            summed = corrs[:, choice].sum(axis=1)
            sortee = np.argsort(summed)
            for x in sortee:
                if int(x) in choice:
                    continue
                else:
                    choice.append(int(x))
                    break
        return choice

    def graph_correlation(self, data, names):
        """Makes a scatterplot matrix:
        Inputs:
          data - a list of data [dataX, dataY,dataZ,...];
                 all elements must have same length

          names - a list of descriptions of the data;
                      len(data) should be equal to len(data_name)

        Output:
          fig - matplotlib.figure.Figure Object

        http://www.kenjisato.jp/blog/2011/03/28/scatterplot-matrix-with-matplotlib/
        """
        plt.clf()
        N = len(data)
        fig = plt.figure()

        for i in range(N):
            for j in range(N):
                if j < i:
                    continue

                ax = fig.add_subplot(N, N, i * N + j + 1)

                if j == i:
                    ax.hist(data[i],
                        bins=30,
                        histtype="step"
                    )
                    ax.set_xticks([])
                    ax.set_yticks([])
                    ax.text(0.05, 0.95,
                        "\n".join(names[i]),
                        horizontalalignment='left',
                        verticalalignment='top',
                        transform=ax.transAxes,
                        size=5,
                    )
                else:
                    d1, d2 = data[i], data[j]
                    mask = (d1 != 0) * (d2 != 0)
                    ax.plot(d1[mask], d2[mask],
                        marker=".",
                        linestyle="None",
                        alpha=0.05,
                        markersize=2,
                        mfc="g",
                        mec="None"
                    )
                    ax.set_xticks([])
                    ax.set_yticks([])
        return fig


if __name__ == "__main__":
    mc = MethodCorrelator()
    d = mc.correlate()
    r = mc.create_correlation_matrix(d[0])
    c = mc.choose_methods(r)

    def _(x):
        pm = x > 0
        nm = x < 0
        x[pm] = np.log(x[pm])
        x[nm] = -1 * np.log(-1 * x[nm])
        return x
    rev_m = dict([(y, x) for x, y in d[1].iteritems()])
    data = [_(d[0][:, x]) for x in c]
    fig = mc.graph_correlation(
        data,
        [rev_m[x] for x in c]
    )
    fig.savefig("correlation.png", dpi=600)
    fig = mc.graph_correlation(
        data[:3],
        [rev_m[x] for x in c[:3]]
    )
    fig.savefig("correlation-small.png", dpi=300)
    # with open(os.path.join(mc.output_dir, "big.pickle"), "wb") as f:
    #     pickle.dump(mc.correlate(), f, protocol=pickle.HIGHEST_PROTOCOL)
