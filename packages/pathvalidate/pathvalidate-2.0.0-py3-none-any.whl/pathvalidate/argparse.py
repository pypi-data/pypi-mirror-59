"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from argparse import ArgumentTypeError

from ._common import PathType
from ._file import sanitize_filename, sanitize_filepath, validate_filename, validate_filepath
from .error import ValidationError


def validate_filename_arg(value: str) -> str:
    if not value:
        return ""

    try:
        validate_filename(value)
    except ValidationError as e:
        raise ArgumentTypeError(e)

    return value


def validate_filepath_arg(value: str) -> str:
    if not value:
        return ""

    try:
        validate_filepath(value)
    except ValidationError as e:
        raise ArgumentTypeError(e)

    return value


def sanitize_filename_arg(value: str) -> PathType:
    if not value:
        return ""

    return sanitize_filename(value)


def sanitize_filepath_arg(value: str) -> PathType:
    if not value:
        return ""

    return sanitize_filepath(value)


def filename(value: PathType) -> PathType:  # pragma: no cover
    # Deprecated
    try:
        validate_filename(value)
    except ValidationError as e:
        raise ArgumentTypeError(e)

    return sanitize_filename(value)


def filepath(value: PathType) -> PathType:  # pragma: no cover
    # Deprecated
    try:
        validate_filepath(value)
    except ValidationError as e:
        raise ArgumentTypeError(e)

    return sanitize_filepath(value)
