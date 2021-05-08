import utils
import data_utils
import model_utils
import seaborn as sns
import pandas as pd

import numpy as np
from tqdm import tqdm
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 200


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--path1', type=str, default='',
                        help='path to first folder of models')
    parser.add_argument('--path2', type=str, default='',
                        help='path to second folder of models')
    parser.add_argument('--sample', type=int, default=0,
                        help='how many models to use for meta-classifier')
    parser.add_argument('--example_mode', type=bool, default=False,
                        help='use examples (True) or model weights (True)')
    parser.add_argument('--multimode', type=bool, default=False,
                        help='experiment for multiple samples?')
    parser.add_argument('--ntimes', type=int, default=5,
                        help='number of repetitions for multimode')
    parser.add_argument('--test_path1', type=str, default=None,
                        help='path to first folder of models (to test)')
    parser.add_argument('--test_path2', type=str, default=None,
                        help='path to second folder of models (to test)')
    parser.add_argument('--plot_title', type=str, default="",
                        help='desired title for plot, sep by _')
    args = parser.parse_args()
    utils.flash_utils(args)

    if (not args.multimode) and args.sample < 1:
        raise ValueError("At least one model must be used!")

    ci = data_utils.CensusIncome()

    example_mode = None
    if args.example_mode:
        _, (example_mode, _), _ = ci.load_data(None,
                                               first=False,
                                               test_ratio=0.5)

    (X_train, _), y_train = model_utils.extract_model_features(
                                [args.path1, args.path2],
                                example_mode,
                                args.multimode,
                                args.sample)

    (X_test, _), y_test = model_utils.extract_model_features(
                                [args.test_path1, args.test_path2],
                                example_mode,
                                args.multimode,
                                args.sample)

    if args.multimode:
        columns = [
            "Size of train-set for meta-classifier",
            "Accuracy on unseen models"
        ]
        data = []
        trainSetSizes = [
            4, 6, 10, 25,
            50, 100, 150, 200,
            300, 350
        ]
        for tss in tqdm(trainSetSizes):
            x_tr, unused, y_tr, unused = train_test_split(
                X_train, y_train, train_size=tss)
            for j in range(args.ntimes):
                # Train meta-classifier
                clf = MLPClassifier(hidden_layer_sizes=(30, 30),
                                    max_iter=1000)
                clf.fit(x_tr, y_tr)
                data.append([tss, clf.score(X_test, y_test)])

        # Plot performance with size of training set
        # For meta-classifier
        df = pd.DataFrame(data, columns=columns)
        sns_plot = sns.boxplot(x="Size of train-set for meta-classifier",
                               y="Accuracy on unseen models",
                               data=df)
        plt.ylim(0.45, 1.0)
        plt.title(" ".join(args.plot_title.split('_')))
        sns_plot.figure.savefig("../visualize/census_meta_scores_unseen.png")

    else:
        if args.multimode:
            clf = MLPClassifier(hidden_layer_sizes=(30, 30), max_iter=500)
        else:
            clf = MLPClassifier(hidden_layer_sizes=(30, 30), max_iter=500)
        print("Training meta-classifier")
        clf.fit(X_train, y_train)
        print("Meta-classifier performance on train data: %.2f" %
              clf.score(X_train, y_train))
        print("Meta-classifier performance on test data: %.2f" %
              clf.score(X_test, y_test))

        # Plot score distributions on test data
        labels = ['Trained on $D_0$', 'Trained on $D_1$']
        params = {'mathtext.default': 'regular'}
        plt.rcParams.update(params)

        zeros = np.nonzero(y_test == 0)[0]
        ones = np.nonzero(y_test == 1)[0]

        score_distrs = clf.predict_proba(X_test)[:, 1]

        plt.hist(score_distrs[zeros], 20, label=labels[0], alpha=0.7)
        plt.hist(score_distrs[ones], 20, label=labels[1], alpha=0.7)

        plt.title("Metal-classifier score prediction distributions for unseen models")
        plt.xlabel("Meta-classifier $Pr$[trained on $D_1$]")
        plt.ylabel("Number of models")
        plt.legend()

    plt.savefig("../visualize/census_meta_scores_unseen.png")
