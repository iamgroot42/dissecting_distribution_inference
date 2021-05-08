import numpy as np
from joblib import load
import os
import utils
import data_utils
from sklearn.neural_network._base import ACTIVATIONS
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 200


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    # Census Income dataset
    base_path = "census_models_mlp"
    paths = ['original', 'income', 'sex', 'race']
    ci = data_utils.CensusIncome()

    def sex_filter(df): return utils.filter(
        df, lambda x: x['sex:Female'] == 1, 0.65)
    def race_filter(df): return utils.filter(
        df, lambda x: x['race:White'] == 0,  1.0)
    def income_filter(df): return utils.filter(
        df, lambda x: x['income'] == 1, 0.5)

    _, (x_te, y_te), cols = ci.load_data()
    cols = list(cols)
    # desired_property = cols.index("sex:Female")
    desired_property = cols.index("race:White")
    # Focus on performance of desired property
    # desired_ids = (y_te == 1)[:,0]
    desired_ids = x_te[:, desired_property] >= 0
    x_te, y_te = x_te[desired_ids], y_te[desired_ids]

    # Get intermediate layer representations
    def layer_output(data, MLP, layer=0):
        L = data.copy()
        for i in range(layer):
            L = ACTIVATIONS['relu'](
                np.matmul(L, MLP.coefs_[i]) + MLP.intercepts_[i])
        return L

    cluster_them = []

    for path_seg in paths:
        plotem = []
        perfs = []
        for path in os.listdir(os.path.join(base_path, path_seg)):
            clf = load(os.path.join(base_path, path_seg, path))

            z = layer_output(x_te, clf, 3)
            cluster_them.append(z)
            break

            perfs.append(clf.predict_proba(x_te)[:, 0])
            for sc in clf.predict_proba(x_te)[:, 0]:
                plotem.append(sc)
            # perfs.append(clf.score(x_te, y_te.ravel()))
        bins = np.linspace(0, 1, 100)
        # plt.hist(plotem, bins, alpha=0.5, label=path_seg)
        print("%s : %.4f +- %.4f" %
              (path_seg, np.mean(perfs), np.std(perfs)))

    # plt.legend(loc='upper right')
    # plt.savefig("../visualize/score_dists.png")

    kmeans = KMeans(n_clusters=4, random_state=0)
    kmeans.fit(np.concatenate(cluster_them, 0))	

    colors = ['indianred', 'limegreen', 'blue', 'orange']
    markers = ['o', 'x', '^', 'd']

    # For visualization
    pca = PCA(n_components=2).fit(np.concatenate(cluster_them))
    pca.fit(np.concatenate(cluster_them, 0))
    transformed = []
    for j, ct in enumerate(cluster_them):
        np.random.shuffle(ct)
        lab, cou = np.unique(kmeans.predict(ct), return_counts=True)
        print(lab, cou)
        labels = kmeans.predict(ct[:2000])
        transformed = pca.transform(ct[:2000])
        for x, l in zip(transformed, labels):
            plt.scatter(x[0], x[1], s=10, c=colors[l], marker=markers[j])
        # for x, l in zip(transformed, labels): plt.scatter(x[0], x[1], s=10, c=colors[j], marker=markers[l])

    plt.savefig("../visualize/cluster_show.png")
