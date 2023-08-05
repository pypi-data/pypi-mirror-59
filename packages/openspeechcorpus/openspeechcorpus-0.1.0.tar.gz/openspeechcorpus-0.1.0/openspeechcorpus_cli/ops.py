#!/usr/bin/env python

import argparse
import requests
import json

from requests.exceptions import ConnectionError

from os.path import exists, isdir, join
from os import mkdir

PAGE_SIZE = 500


def download_file(url, local_filename):
    # Taken from here
    # https://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py/16696317#16696317
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                #  f.flush() commented by recommendation from J.F.Sebastian
    return local_filename


def download_files(json_data, corpus, output_folder, output_file, s3_prefix, text_node):
    for audio_data in json_data:
        print("Element: {}".format(audio_data["id"]))
        if corpus == "tales":
            audio_id = audio_data["audio"]["audiofile"].replace(".mp4", "")
            file_name = "{}.mp4".format(join(output_folder, str(audio_data["audio"]["id"])))
        else:
            audio_id = audio_data["audio"]["id"]
            file_name = "{}.mp4".format(join(output_folder, str(audio_id)))
        output_file.write("{},{}\n".format(file_name, audio_data[text_node]["text"].strip()))
        if not exists(file_name):
            print("Download file: {}{}.mp4".format(s3_prefix, audio_id))
            print("Saving into {}".format(file_name))
            try:
                download_file(
                    "{}{}.mp4".format(s3_prefix, audio_id),
                    file_name
                )
            except ConnectionError:
                print("Error getting file {}".format(file_name))
        else:
            print("File {} already exists, skipping".format(file_name))


def execute_from_command_line():
    parser = argparse.ArgumentParser(
        "Download files from Open Speech Corpus"
    )

    parser.add_argument(
        "--from",
        help="ID for the initial Audio Data",
        default=1
    )

    parser.add_argument(
        "--to",
        help="ID for the final Audio Data",
        default=500
    )

    parser.add_argument(
        "--url",
        help="URL for the list API endpoint",
        default="http://openspeechcorpus.contraslash.com/api/words/list/"
    )

    parser.add_argument(
        "--corpus",
        help="Name of the corpus [aphasia|words]",
        default=""
    )

    parser.add_argument(
        "--s3_prefix",
        default="https://s3.amazonaws.com/contraslash/openspeechcorpus/media/audio-data/v2/"
    )

    parser.add_argument(
        "--output_folder",
        help="Folder to store the recordings",
        type=str,
        required=True
    )

    parser.add_argument(
        "--output_file",
        help="File where transcriptions are stored",
        default="transcription.txt"
    )

    parser.add_argument(
        "--text_node",
        help="Inner node containing text information",
        default="level_sentence"
    )

    parser.add_argument(
        "--force_create",
        help="Force creation of output folder",
        default=True
    )

    parser.add_argument(
        "--download_all",
        help="Download all the selected corpus",
        action="store_true"
    )

    args = vars(parser.parse_args())

    url = args["url"]
    corpus = args.get("corpus", "")
    if corpus:
        if corpus == "tales":
            url = "http://openspeechcorpus.contraslash.com/api/tale-sentences/list/"
            args["text_node"] = "tale_sentence"
            args["s3_prefix"] = "https://s3.amazonaws.com/contraslash/openspeechcorpus"
            print("Aphasia corpus selected, using URL: http://openspeechcorpus.contraslash.com/api/tale-sentences/list/")
        elif corpus == "aphasia":
            url = "http://openspeechcorpus.contraslash.com/api/words/list/"
            args["text_node"] = "level_sentence"
            print("Aphasia corpus selected, using URL: http://openspeechcorpus.contraslash.com/api/words/list/")
        elif corpus == "words":
            url = "http://openspeechcorpus.contraslash.com/api/isolated-words/list/"
            args["text_node"] = "isolated_word"
            print("Words corpus selected, using URL: http://openspeechcorpus.contraslash.com/api/isolated-words/list/")
        else:
            print("Unexisting corpus, valid options are: tales, aphasia, words")
            exit(1)

    if not exists(args["output_folder"]):
        print("Output folder does not exists")
        if args["force_create"]:
            print("force_create flag detected, creating {}".format(args["output_folder"]))
            mkdir(args["output_folder"])
        else:
            exit(1)
    if not isdir(args["output_folder"]):
        print("Output folder exists exists but is not a folder")
        exit(2)

    output_file = open(args["output_file"], "w+")
    if args.get("download_all", False):
        actual_index = args["from"]
        print("Downloading whole corpus, starting in {}".format(actual_index))
        actual_url = "{}?from={}&to={}".format(url, actual_index, actual_index+PAGE_SIZE)
        print("Querying {}".format(actual_url))
        response = requests.get(actual_url)
        while response.status_code == 200 and response.json():
            json_data = response.json()
            print("We get {} audio datas".format(len(json_data)))
            try:
                download_files(json_data, corpus, args["output_folder"], output_file, args["s3_prefix"], args["text_node"])
            except KeyboardInterrupt:
                print("Process interrupting, finishing gracefully")
                output_file.close()
                exit(0)
            actual_index += PAGE_SIZE
            actual_url = "{}?from={}&to={}".format(url, actual_index, actual_index + PAGE_SIZE)
            print("Querying {}".format(actual_url))
            response = requests.get(actual_url)
        output_file.close()
    else:
        print("Downloading segment from {} to {}".format(args["from"], args["to"]))
        url = "{}?from={}&to={}".format(url, args["from"], args["to"])
        print("Querying {}".format(url))
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            print("We get {} audio datas".format(len(json_data)))
            try:
                download_files(json_data, corpus, args["output_folder"], output_file, args["s3_prefix"], args["text_node"])
            except KeyboardInterrupt:
                print("Process interrupting, finishing gracefully")
            finally:
                output_file.close()
        else:
            print("Cannot connect to server, response status was {}".format(response.status_code))
