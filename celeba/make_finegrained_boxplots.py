import seaborn as sns
import matplotlib.pyplot as plt
import argparse
from utils import flash_utils
from data_utils import SUPPORTED_PROPERTIES
import numpy as np
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 200


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--darkplot', action="store_true",
                        help='Use dark background for plotting results')
    parser.add_argument('--filter', choices=SUPPORTED_PROPERTIES,
                        default="Male",
                        help='name for subfolder to save/load data from')
    args = parser.parse_args()
    flash_utils(args)

    # Set font size
    plt.rcParams.update({'font.size': 6})

    if args.darkplot:
        # Set dark background
        plt.style.use('dark_background')

    targets = ["0.0", "0.1", "0.2", "0.3", "0.4",
               "0.5", "0.6", "0.7", "0.8", "0.9", "1.0"]

    fill_data = np.zeros((len(targets), len(targets)))
    mask = np.ones((len(targets), len(targets)), dtype=bool)
    annot_data = [[None] * len(targets) for _ in range(len(targets))]
    if args.filter == "Male":
        raw_data = [
            [
                [50.87456271864068, 55.82208895552224, 54.622688655672164, 54.922538730634685, 50.324837581209394],
                [64.24986056887897, 60.23424428332404, 53.09537088678193, 63.63636363636363, 65.03067484662577],
                [74.01299350324838, 77.71114442778611, 54.57271364317841, 72.16391804097951, 65.5672163918041],
                [86.52373660030628, 77.7947932618683, 88.41245533435426, 84.89025012761613, 71.05666156202145],
                [92.81, 91.56, 88.87, 84.37, 80.72],
                [88.17092235539343, 94.78895257946847, 92.44398124022929, 91.66232412714956, 92.02709744658677],
                [77.71114442778611, 96.55172413793103, 91.75412293853073, 96.85157421289355, 96.95152423788106],
                [86.28899835796388, 94.90968801313629, 96.05911330049261, 91.54351395730706, 93.43185550082102],
                [98.05097451274362, 97.10144927536231, 92.70364817591205, 95.60219890054972, 97.15142428785607],
                [93.7031484257871, 95.55222388805598, 91.904047976012, 84.90754622688655, 98.20089955022489]
            ],
            [
                [52.176339285714285, 51.283482142857146, 53.683035714285715, 46.763392857142854, 49.832589285714285],
                [59.85, 56.4, 60.15, 57.5, 52.45],
                [74.61695607763023, 71.0929519918284, 62.461695607763026, 72.62512768130746, 58.88661899897855],
                [78.86, 72.76, 74.51, 75.81, 86.81],
                [89.67674661105318, 87.5912408759124, 85.24504692387904, 88.42544316996872, 84.98435870698644],
                [87.5, 90.6, 93.25, 94.2, 89.85],
                [96.38455217748562, 98.02793755135579, 97.20624486442071, 94.16598192276089, 89.31799506984387],
                [98.0, 94.75, 92.6, 97.3, 94.15],
                [95.55, 95.8, 92.3, 90.65, 98.15]
            ],
            [
                [52.622767857142854, 56.361607142857146, 55.357142857142854, 54.74330357142857, 48.716517857142854],
                [60.17142857142857, 58.4, 59.65714285714286, 56.91428571428571, 59.371428571428574],
                [55.38, 66.10, 70.38, 57.28, 68.88],
                [67.48538011695906, 72.39766081871345, 75.73099415204679, 81.75438596491227, 80.64327485380117],
                [69.140625, 78.29241071428571, 80.74776785714286, 89.34151785714286, 91.96428571428571],
                [93.45887016848364, 94.64816650148661, 94.15262636273538, 91.67492566897918, 85.92666005946482],
                [90.95982142857143, 86.49553571428571, 87.83482142857143, 93.91741071428571, 91.90848214285714],
                [97.99107142857143, 91.57366071428571, 93.86160714285714, 88.83928571428571, 88.16964285714286]
            ],
            [
                [48.92747701736466, 52.96220633299285, 51.327885597548516, 53.06435137895812, 53.88151174668029],
                [56.42, 56.72, 56.52, 57.57, 53.42],
                [72.1584984358707, 64.65067778936393, 69.44734098018769, 64.44212721584984, 74.19186652763295],
                [74.0, 72.75, 75.25, 77.2, 81.15],
                [93.59079704190633, 85.20953163516845, 91.78307313064914, 78.47165160230074, 84.05916187345933],
                [92.6, 93.15, 95.55, 91.9, 89.25],
                [95.95, 94.2, 96.4, 93.35, 91.95]
            ],
            [
                [51.15, 48.75, 49.97, 51.45, 52.58],
                [55.75692963752665, 59.11513859275053, 60.82089552238806, 61.140724946695094, 57.40938166311301],
                [59.703779366700715, 65.57711950970378, 68.69254341164454, 58.88661899897855, 65.37282941777323],
                [69.53191489361703, 83.06382978723404, 81.70212765957447, 88.51063829787235, 83.57446808510639],
                [89.42798774259448, 85.03575076608784, 77.52808988764045, 79.21348314606742, 88.35546475995915],
                [93.41164453524004, 91.72625127681307, 96.47599591419817, 91.87946884576098, 87.89581205311542]
            ],
            [
                [53.88, 47.84, 52.16, 49.92, 54.56],
                [63.17, 64.27, 56.12, 51.67, 58.77],
                [77.01, 82.18, 81.77, 73.15, 73.32],
                [84.16, 81.46, 80.01, 78.41, 82.36],
                [80.1, 92.45, 93.65, 85.26, 89.26]
            ],
            [
                [48.488008342022944, 47.86235662148071, 50.62565172054223, 50.886339937434826, 51.668404588112615],
                [33.30396475770925, 77.26872246696036, 72.15859030837004, 68.72246696035242, 49.11894273127753],
                [75.49530761209593, 70.85505735140772, 72.47132429614182, 72.31491136600626, 69.39520333680917],
                [80.60479666319083, 68.14389989572472, 63.86861313868613, 64.18143899895725, 59.74973931178311],
            ],
            [
                [66.557107641742, 37.830731306491373, 64.50287592440428, 48.31552999178307, 48.72637633525061],
                [68.6, 69.7, 50.3, 52.65, 51.25],
                [79.35, 56.7, 75.0, 79.6, 66.95]
            ],
            [
                [45.60, 71.41, 54.31, 60.15, 41.08],
                [50.123253903040265, 55.46425636811832, 62.366474938373045, 42.07066557107642, 76.66]
            ],
            [
                [56.25, 46.95, 47.4, 56.0, 56.15]
            ]
        ]

    # Loss
    # 0 v/s 0.1: 53.105
    # 0 v/s 0.2: 53.15
    # 0 v/s 0.3: 52.13
    # 0 v/s 0.4: 51.44
    # 0 v/s 0.6: 52.92
    # 0 v/s 0.7: 50.86

        raw_data_threshold = [
            [
                [50.68, 50.03, 51.24],
                [53.89, 54.91, 52.67],
                [55.56, 52.84, 55.20],
                [56.25, 57.01, 61.31],
                [54.2, 56.9, 58.05],
                [59.09, 60.98, 61.03],
                [67.37, 61.94, 63.95],
                [],
                [],
                []
            ],
            [
                [],
                [],
                [],
                [50.48, 55.57, 53.66],
                [],
                [],
                [],
                [],
                []
            ]
        ]

    for i in range(len(targets)):
        for j in range(len(targets)-(i+1)):
            m, s = np.mean(raw_data[i][j]), np.std(raw_data[i][j])
            fill_data[i][j+i+1] = m
            mask[i][j+i+1] = False
            annot_data[i][j+i+1] = r'%d $\pm$ %d' % (m, s)

    sns_plot = sns.heatmap(fill_data, xticklabels=targets, yticklabels=targets,
                           annot=annot_data, mask=mask, fmt="^")
    sns_plot.set(xlabel=r'$\alpha_0$', ylabel=r'$\alpha_1$')
    sns_plot.figure.savefig("./meta_heatmap.png")
