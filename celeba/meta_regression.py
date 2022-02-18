import torch as ch
import numpy as np
import os
import argparse
import utils
from data_utils import SUPPORTED_PROPERTIES, SUPPORTED_RATIOS
from model_utils import get_model_features, BASE_MODELS_DIR


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Celeb-A')
    parser.add_argument('--batch_size', type=int, default=150)
    parser.add_argument('--train_sample', type=int, default=700)
    parser.add_argument('--val_sample', type=int, default=50)
    parser.add_argument('--testing', action="store_true", help="Testing mode")
    parser.add_argument('--filter', help='alter ratio for this attribute',
                        default="Male", choices=SUPPORTED_PROPERTIES)
    parser.add_argument('--epochs', type=int, default=100)
    parser.add_argument('--lr', type=float, default=1e-3)
    parser.add_argument('--focus', choices=["fc", "conv", "combined"],
                        required=True, help="Which layer paramters to use")
    args = parser.parse_args()
    utils.flash_utils(args)

    if args.testing:
        num_train, num_val = 3, 2
        n_models = 5
        SUPPORTED_RATIOS = SUPPORTED_RATIOS[:3]
    else:
        num_train, num_val = args.train_sample, args.val_sample
        n_models = 1000

    X_train, X_test = [], []
    X_val, Y_val = [], []
    Y_train, Y_test = [], []
    for ratio in SUPPORTED_RATIOS:
        train_dir = os.path.join(
            BASE_MODELS_DIR, "adv/%s/%s/" % (args.filter, ratio))
        test_dir = os.path.join(
            BASE_MODELS_DIR, "victim/%s/%s/" % (args.filter, ratio))

        # Load models, convert to features
        dims, vecs_train_and_val = get_model_features(
            train_dir, max_read=n_models,
            focus=args.focus,
            shift_to_gpu=False)
        _, vecs_test = get_model_features(
            test_dir, max_read=n_models,
            focus=args.focus,
            shift_to_gpu=False)

        vecs_train_and_val = np.array(vecs_train_and_val, dtype='object')
        vecs_test = np.array(vecs_test, dtype='object')

        # Shuffle and divide train data into train and val
        shuffled = np.random.permutation(len(vecs_train_and_val))
        vecs_train = vecs_train_and_val[shuffled[:num_train]]
        vecs_val = vecs_train_and_val[shuffled[num_train:num_train+num_val]]

        # Keep collecting data...
        X_train.append(vecs_train)
        X_val.append(vecs_val)
        X_test.append(vecs_test)

        # ...and labels
        Y_train += [float(ratio)] * len(vecs_train)
        Y_val += [float(ratio)] * len(vecs_val)
        Y_test += [float(ratio)] * len(vecs_test)

    # Prepare for PIM
    X_train = np.concatenate(X_train)
    X_val = np.concatenate(X_val)
    X_test = np.concatenate(X_test)

    Y_train = ch.from_numpy(np.array(Y_train)).float()
    Y_val = ch.from_numpy(np.array(Y_val)).float()
    Y_test = ch.from_numpy(np.array(Y_test)).float()

    # Batch layer-wise inputs
    print("Batching data: hold on")
    X_train = utils.prepare_batched_data(X_train)
    X_val = utils.prepare_batched_data(X_val)
    X_test = utils.prepare_batched_data(X_test)

    # Train meta-classifier model
    if args.focus == "conv":
        dim_channels, dim_kernels = dims
        metamodel = utils.PermInvConvModel(
            dim_channels, dim_kernels)
    elif args.focus == "fc":
        metamodel = utils.PermInvModel(dims)
    else:
        dims_conv, dims_fc = dims
        dim_channels, dim_kernels, middle_dim = dims_conv
        metamodel = utils.FullPermInvModel(
            dims_fc, middle_dim, dim_channels, dim_kernels,)
    metamodel = metamodel.cuda()

    # Train PIM
    batch_size = 10 if args.testing else args.batch_size
    _, tloss = utils.train_meta_model(
        metamodel,
        (X_train, Y_train), (X_test, Y_test),
        epochs=args.epochs,
        binary=True, lr=args.lr,
        regression=True,
        batch_size=batch_size,
        val_data=(X_val, Y_val), combined=True,
        eval_every=10, gpu=True)
    print("Test loss %.4f" % (tloss))

    # Save meta-model
    ch.save(metamodel.state_dict(), "./metamodel_%s_%.3f.pth" %
            (args.filter, tloss))

    # Male
    # All
    # Train: 0.00092, 0.00062, 0.00055, 0.00063, 0.00048
    # Test: 0.66619, 0.42054, 0.39416, 0.41067, 0.45654
    # Conv
    # Train: 0.00059, 0.00045, 0.00049, 0.00058, 0.00051
    # Test: 0.47972, 0.39712, 0.32094, 0.37900, 0.26586

    # Young
    # All
    # Train: 0.00074, 0.00067, 0.00104, 0.00068
    # Test: 0.5301, 0.50441, 0.64415, 0.51595
    # FC
    # Train: 0.00070, 0.00059, 0.00098, 0.00106, 0.00068
    # Test:  0.52710, 0.51089, 0.49209, 0.54871, 0.48593