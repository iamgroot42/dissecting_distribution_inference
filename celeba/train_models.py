from model_utils import create_model, save_model
from data_utils import SUPPORTED_PROPERTIES, CelebaWrapper
from utils import flash_utils, train, extract_adv_params


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True,
                        help='filename (prefix) to save model')
    parser.add_argument('--epochs', type=int, default=10,
                        help='number of epochs to train model for')
    parser.add_argument('--filter', help='alter ratio for this attribute',
                        required=True, choices=SUPPORTED_PROPERTIES)
    parser.add_argument('--ratio', type=float, required=True,
                        help='desired ratio for attribute')
    parser.add_argument('--split', choices=['victim', 'adv'], required=True)
    parser.add_argument('--bs', type=int, default=128, help='batch size')
    parser.add_argument('--lr', type=float, default=1e-4, help='learning rate')
    parser.add_argument('--augment', action="store_true",
                        help='use data augmentations when training models?')
    parser.add_argument('--adv_train', action="store_true",
                        help='use adversarial training?')
    parser.add_argument('--task', default="Smiling",
                        choices=SUPPORTED_PROPERTIES,
                        help='task to focus on')
    parser.add_argument('--parallel', action="store_true",
                        help='use multiple GPUs to train?')
    parser.add_argument('--verbose', action="store_true",
                        help='print out epoch-wise statistics?')
    args = parser.parse_args()
    flash_utils(args)

    # CelebA dataset
    ds = CelebaWrapper(args.filter, args.ratio,
                       args.split, augment=args.augment,
                       classify=args.task)

    # Get loaders
    train_loader, test_loader = ds.get_loaders(args.bs)

    # Get adv params
    adv_params = False
    if args.adv_train:
        eps = 2.0
        nb_iter = 20
        adv_params = extract_adv_params(
            eps=eps, eps_iter=(2.5 * eps / nb_iter), nb_iter=nb_iter,
            norm=2, random_restarts=5,
            clip_min=-1, clip_max=1)

    # Create model
    model = create_model(parallel=args.parallel)

    # Train model
    model, (vloss, vacc) = train(model, (train_loader, test_loader),
                                 lr=args.lr, epoch_num=args.epochs,
                                 weight_decay=1e-3, verbose=args.verbose,
                                 get_best=True, adv_train=adv_params)

    if args.adv_train:
        save_name = args.name + "_" + str(vacc[0]) + "_" + str(vloss[0])
        save_name += "_adv" + str(vacc[1]) + "_adv" + str(vloss[1])
    else:
        save_name = args.name + "_" + str(vacc) + "_" + str(vloss)

    # Save model
    save_name = save_name + ".pth"
    save_model(model, args.split, args.filter, str(
        args.ratio), save_name, dataparallel=args.parallel)
