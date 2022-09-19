import torch
import torch.nn as nn
import time
import argparse

parser = argparse.ArgumentParser(description='Hello world, but for clusters')
parser.add_argument('--cuda', action='store_true', default=False, help='Load models and tensors onto cuda. Uses cpu by default.')
parser.add_argument('--wait-time', type=int, default=5, help='Time to sleep before exiting program (in seconds)')
args = parser.parse_args()


def create_model(input_size, n_classes):
    stem = nn.Conv2d(in_channels=input_size[0], out_channels=10, kernel_size=(3, 3), padding=(1, 1))
    convs = [nn.Conv2d(in_channels=10, out_channels=10, kernel_size=(3, 3), padding=(1, 1)) for _ in range(3)]
    flatten = nn.Flatten()
    linear = nn.Linear(10*input_size[1]**2, n_classes)

    model = nn.Sequential(stem, *convs, flatten, linear)

    return model

def main(args):
    device = torch.device('cuda') if args.cuda == True else torch.device('cpu')
    input_shape = (3, 32, 32)
    n_classes = 10
    model = create_model(input_shape, n_classes).to(device)

    x = torch.randn(8, *input_shape).to(device)
    out = model(x)

    print(f'Device is {device}')
    print(f'results: {out}')
    print(f'Waiting for {args.wait_time} seconds to terminate the program...')

    time.sleep(args.wait_time)

    print('Done.')

if __name__ == '__main__':
    main(args)
