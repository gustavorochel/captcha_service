import base64
import argparse


def generate_base64(path: str) -> None:
    with open(path, "rb") as image_file:
        print(base64.b64encode(image_file.read()).decode('utf-8'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', '--path',
        type=str,
        required=True,
        help='image path to be converted'
    )

    FLAGS, unparsed = parser.parse_known_args()

    generate_base64(FLAGS.path)
