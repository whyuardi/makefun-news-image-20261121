#!/usr/bin/env python3
"""Entry program for news-image-20261121.

Copies the bundled front-page image to /output/entry.png.
Deterministic, no network, no randomness.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"), "/output/entry.png")


if __name__ == "__main__":
    main()
