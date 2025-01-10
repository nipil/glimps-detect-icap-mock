#!/usr/bin/env python3

import argparse
import json
import os
import subprocess
import tarfile
from pathlib import Path
from tempfile import TemporaryDirectory

DEFAULT_DEBS = ['curl', 'ca-certificates', 'c-icap', 'skopeo']
DEFAULT_IMAGE = 'glimpsre/icap-detect'
DEFAULT_TARGET = '/'


def install_deb(debs: list[str]) -> None:
    env = os.environ.copy()
    env['DEBIAN_FRONTEND'] = 'noninteractive'
    print(f'Installing packages {debs}')
    subprocess.run(['apt-get', 'update'], check=True, env=env)
    subprocess.run(['apt-get', 'install', '-y', '--no-install-recommends'] + debs, check=True, env=env)


def load_json(path: Path) -> dict:
    with open(path, 'rb') as fp:
        return json.load(fp)


def get_target_blob_path(src: Path, sha256: str) -> Path:
    return src / 'blobs' / 'sha256' / sha256


def load_target_blob_json(src: Path, sha256: str) -> dict:
    return load_json(get_target_blob_path(src, sha256))


def extract_entrypoint(src: Path, target_dir: Path) -> None:
    index = load_json(src / 'index.json')
    manifest_digest = index['manifests'][0]['digest'].split(':')[1]
    manifest_data = load_target_blob_json(src, manifest_digest)
    config_digest = manifest_data['config']['digest'].split(':')[1]
    entrypoint = load_target_blob_json(src, config_digest)['config']['Entrypoint'][0].lstrip('/')
    for layer in manifest_data['layers']:
        if layer['mediaType'] != 'application/vnd.oci.image.layer.v1.tar+gzip':
            continue
        layer_digest = layer['digest'].split(':')[1]
        with tarfile.open(get_target_blob_path(src, layer_digest)) as tf:
            try:
                tf.extract(entrypoint, target_dir)
                print(f'{entrypoint} extracted to {target_dir}')
            except KeyError:
                continue


def install_entrypoint(image: str, version: str, target: Path) -> None:
    print(f'Installing {image} version {version} entrypoint')
    with TemporaryDirectory(prefix='skopeo-') as tmp:
        print(f'Extracting image into {tmp}')
        subprocess.run(['skopeo', 'copy', f'docker://{image}:{version}', f'oci:{tmp}'], check=True)
        extract_entrypoint(Path(tmp), target)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target-dir', default=DEFAULT_TARGET)
    parser.add_argument('--debs', nargs='*', default=DEFAULT_DEBS)
    parser.add_argument('--image', default=DEFAULT_IMAGE)
    parser.add_argument('icap_detect_version')
    args = parser.parse_args()
    install_deb(args.debs)
    install_entrypoint(args.image, args.icap_detect_version, Path(args.target_dir))
    print('Done.')


if __name__ == '__main__':
    main()
