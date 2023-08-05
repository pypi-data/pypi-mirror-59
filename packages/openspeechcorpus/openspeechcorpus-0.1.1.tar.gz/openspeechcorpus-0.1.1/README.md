# Open Speech Corpus CLI

This repository contains the code required to download audiodata from 
[openspeechcorpus.com](http://openspeechcorpus.contraslash.com)

Open Speech Corpus is composed by far for three subcorpuses:

- Tales: A crowdsourced corpus based on reading of latin american short tales
- Aphasia: A crowdsourced corpus based in words categorized in 4 levels of difficulty
- Isolated words: A crowdsourced corpus based in isolated words

To download files from the Tales Project use

```bash
ops  \
    --output_folder tales/ \
    --output_file tales.txt  \
    --corpus tales
```

To download files from the Isolated Words Project use

```bash
ops  \
    --output_folder isolated_words/ \
    --output_file isolated_words.txt  \
    --corpus words
```

To download files from the Aphasia Project use

```bash
ops  \
    --output_folder aphasia/ \
    --output_file aphasia.txt  \
    --corpus aphasia
```

By default the page size is 500, to modify it use the args `--from` and `--to` i.e:

```bash
ops  \
    --from 500 \
    --to 1000 \
    --output_folder aphasia/ \
    --output_file aphasia.txt  \
    --corpus aphasia
```

You can download the whole corpus using the flag `--download_all`

```bash
ops  \
    --output_folder aphasia/ \
    --output_file aphasia.txt  \
    --corpus aphasia \
    --download_all
```

If you use the flag `--download_all` with the flag `--from` the process will start in the specified arg `from` using a
page size of 500

## Recursive Convert

The Open Speech Corpus stores its files in mp4 format, which is undesired for most audio processing tasks. To convert 
the files into a wav format, first install [ffmpeg](https://www.ffmpeg.org/download.html), then you can execute the
`recursive_convert` utility which receives as first argument the source_folder with the mp4 files and as second argument
the output folder i.e.:

```bash
recursive_convert aphasia aphasia_wav
```

