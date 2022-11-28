import logging
import os
import pytz
from datetime import datetime
from pathlib import Path
from typing import List
from threading import Thread

from aiobotocore.session import AioSession
from s3fs import S3FileSystem

import config

logger = logging.getLogger("uvicorn.error")

settings = config.get_settings()


def init_new_client():
    """Initiate a S3FS connection"""
    session = AioSession()

    return S3FileSystem(
        session=session,
        key=settings.AWS_KEY,
        secret=settings.AWS_SECRET,
        default_block_size=55 * 1024 * 1024,  # Max file size: 55 MB
    )


def download_file(
    aws_path: str,
    out_path: Path,
    client: S3FileSystem = init_new_client(),
):
    """
    Synchronously download an AWS file.

    Args:
        - `aws_path`: File path on AWS
    """
    download_destination = f"{out_path}/{os.path.basename(aws_path)}"

    client.download(aws_path, download_destination)

    logger.info(f"{os.path.basename(aws_path)} - downloaded")


def download_file_list(
    aws_paths: List[str],
    out_path: Path,
    client: S3FileSystem = init_new_client(),
):
    """
    Synchronously download a list of AWS files.

    Args:
        - `files`: File paths on AWS
        - `path`: Download path
    """
    threads: List[Thread] = []

    for index, file in enumerate(aws_paths):
        thread = Thread(
            target=download_file, args=(file,), kwargs={"client": client}
        )
        threads.append(thread)
        threads[index].start()

    for thread in threads:
        thread.join()

    downloaded = list(out_path.iterdir())

    return downloaded, out_path


def download_by_date_modified(
    start_date: datetime,
    stop_date: datetime,
    files: List[str],
    out_path: Path,
    client: S3FileSystem = init_new_client(),
):
    """
    Download files on AWS directory by their modified dates

    Args:
        - `start_date`: Start date for processing
        - `stop_date`: End date for processing
        - `files`: File paths on AWS
    """
    threads: List[Thread] = []

    def check_modified_date_and_download(aws_path: str):
        """
        Check modified date and download if within start and end date

        Args:
            - `aws_path`: File path on AWS
        """
        last_modified: datetime = client.modified(aws_path)
        with_tz = last_modified.replace(tzinfo=pytz.utc)

        before_stop_date = True

        if stop_date is not None:
            before_stop_date = last_modified < stop_date

        if with_tz > start_date and before_stop_date:
            download_destination = f"{out_path}/{os.path.basename(aws_path)}"
            client.download(aws_path, download_destination)

            logger.info(f"{os.path.basename(aws_path)} - downloaded")

        else:
            logger.warning(f"{last_modified} - out of range")

    # Create list of threads to download files within start/stop date
    for index, file in enumerate(files):
        thread = Thread(target=check_modified_date_and_download, args=(file,))
        threads.append(thread)
        threads[index].start()

    for thread in threads:
        thread.join()

    downloaded = list(out_path.iterdir())

    return downloaded, out_path
