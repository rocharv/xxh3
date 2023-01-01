#!/usr/bin/env python3
import argparse
from os import path
from os import walk
from pathlib import Path
from re import search
from xxhash import xxh64


def xxh3(file_name: str) -> str:
    if path.exists(file_name):
        hash_object = xxh64()
        with open(file_name, "rb") as f:
            for chunk in iter(lambda: f.read(1024), b""):
                hash_object.update(chunk)
        return hash_object.hexdigest()
    else:
        print(f"!the target path doesn't exist: {file_name}")
        return "hash_error"


def read_arguments():
    arg_parser = argparse.ArgumentParser(
        prog="xxh3",
        description=("Print or verify a file or a directory checksums using "
                     "fast non-cryptographic algorithm xxHash."),
        epilog="written by Rodrigo Viana Rocha"
    )

    arg_parser.add_argument(
        "TARGET_PATH",
        help="can be a path to a single file or a single directory"
    )

    arg_parser.add_argument(
        "-c",
        "--check_file",
        action="store_true",
        help=("use one plain text file (provided as TARGET_PATH) as source "
              "for file checksums and verify if each of them match with the "
              "actual files. Each line in the check file must have a xxh3 "
              "checksum and its respective full file path, similar to this: "
              "cafc7706cee4572b '/path/to/file'")
    )

    arg_parser.add_argument(
        "-d",
        "--duplicates",
        action="store_true",
        help=("only works when a directory is provided as TARGET_PATH. In "
              "this case, its show duplicated files (with the same hash) at "
              "the end beginning with = symbol.")
    )

    arg_parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help=("only works when a directory is provided as TARGET_PATH. In "
              "this case, recursively compute the checksum for all files in "
              "the TARGET_PATH and its subdirectories")
    )

    args = arg_parser.parse_args()
    return args


def load_check_file(check_file: str) -> dict[str, str]:
    check_file_dict: dict[str, str] = {}

    full_file_path = Path(check_file)
    file_object = open(full_file_path, "rt")
    for line in file_object:
        match = search("([a-f0-9]{16})[ \t]+'?([^'\n]+)'?", line)
        if match:
            check_file_dict[path.abspath(match.group(2))] = match.group(1)
        else:
            print(
                (f"xxh3: the check file ({check_file}) doesn't comply with "
                    "format requirements")
            )
            raise SystemExit(1)

    return check_file_dict


def get_hash_dict(args) -> dict[str, list[str]]:
    result_dict: dict[str, list[str]] = {}

    for current_directory, _, file_names in walk(args.TARGET_PATH):
        for file_name in file_names:
            file_full_path = path.abspath(
                path.join(current_directory, file_name))

            hash = xxh3(file_full_path)
            print(f"{hash} '{file_full_path}'")

            if hash in result_dict:
                result_dict[hash].append(file_full_path)
            else:
                result_dict[hash] = [file_full_path]

        if not args.recursive:
            return result_dict

    return result_dict


def print_check_file_match(args) -> None:
    dict_check_file: dict[str, str] = load_check_file(args.TARGET_PATH)
    all_hash_verified: bool = True

    for file in dict_check_file:
        hash = xxh3(file)
        if hash != dict_check_file[file]:
            all_hash_verified = False
            print(f"{hash} '{path.abspath(args.TARGET_PATH)}'")

    if all_hash_verified:
        print("All files and their xxh3 hashes mentioned in "
              f"'{args.TARGET_PATH}' verify")
    else:
        raise SystemExit(1)


def print_file_hash(args) -> None:
    hash: str = xxh3(args.TARGET_PATH)
    print(f"{hash} '{path.abspath(args.TARGET_PATH)}'")


def print_directory_hash(args) -> None:
    dict_path: dict[str, list[str]] = get_hash_dict(args)

    if args.duplicates:
        for key in dict_path:
            if len(dict_path[key]) > 1:
                for i in range(1, len(dict_path[key])):
                    print(f"={key} '{dict_path[key][i]}'")


def main(args=None) -> None:
    if not args:
        args = read_arguments()

    if path.isfile(args.TARGET_PATH):
        if args.duplicates or args.recursive:
            if args.duplicates:
                print("xxh3: invalid option -d or --duplicates. The target "
                      f"path '{args.TARGET_PATH}' is a file")
            if args.recursive:
                print("xxh3: invalid option -r or --recursive. The target "
                      f"path '{args.TARGET_PATH}' is a file")
            raise SystemExit(1)

        if args.check_file:
            print_check_file_match(args)
        else:
            print_file_hash(args)

    elif path.isdir(args.TARGET_PATH):
        print_directory_hash(args)

    elif not path.exists(args.TARGET_PATH):
        print(f"xxh3: the path '{args.TARGET_PATH}' doesn't exist")
        raise SystemExit(1)


if __name__ == '__main__':
    main()
