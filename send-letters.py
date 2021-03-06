#!/usr/bin/env python3
import argparse
import config
import random
import smtplib
import validator


def is_compatible(santas_lst):
    for k in range(len(santas_lst)):
        one = k % len(santas_lst)
        two = (k + 1) % len(santas_lst)

        x, y = santas_lst[one].name, santas_lst[two].name
        if tuple((x,y)) in config.incompatibles or tuple((y,x)) in config.incompatibles:
            return False

    return True


def send_letter(santa, is_test):
    letter = config.letter.text(santa, is_test)

    with open(config.record_file, 'a') as f:
        f.write(letter)

    if is_test:
        print(letter, end='')
    else:
        config.letter.send(santa)


def set_recipients(santas):

    for k in range(len(santas) - 1):
        santas[k].set_recipient(santas[k+1])

    santas[-1].set_recipient(santas[0])


def parse_arguments():
    parser = argparse.ArgumentParser(
              description='Auto-send Secret Santa letters!')

    parser.add_argument('--official',
        dest='official',
        action='store_true',
        help='Actually send email (and not dump to output)')

    return parser.parse_args()


def main():
    args = parse_arguments()

    is_test = True if not args.official else False

    santas = config.santas

    for s in santas:
        validator.validate_email(s.email)

    # Clear contents of the file
    open(config.record_file, 'w').close()

    while True:
        random.shuffle(santas)

        if is_compatible(santas):
            break

    set_recipients(santas)

    for k in santas:
        send_letter(k, is_test)

    print('\nFinished!\n')
    print('Mail record saved to: {}'.format(config.record_file))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('Uh oh, something failed: {}'.format(e))
