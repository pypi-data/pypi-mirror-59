# Description

ftvstt is a France Télévisions python library which encapsulates multiple online speech-to-text APIs, in order to call them as easily as possible.

It currently supports :
- [x] Amazon Transcribe
- [x] Google Cloud speech-to-text
- [x] Vocapia Voxsigma
- [x] Bertin Mediaspeech

# Quickstart

ftvstt is not currently available through pip, you have to download the package and import it directly :
ftvstt is currently available through pip by running : **pip install ftvstt**.
You should then be able to import the package :

```python
import ftvstt
```

# Usage

Example of transcription through the services:

Vocapia Voxsigma:
```python
vocapiaTranscriber = ftvstt.Vocapia("https://rest1.vocapia.com:8093/voxsigma")
vocapiaTranscriber.authenticate("EXAMPLE_ID","EXAMPLE_PASS")
transcript = vocapiaTranscriber.transcribe("/path/to/file.wav")
vocapiaTranscriber.deauthenticate()
```

Bertin Mediaspeech:
```python
bertinTranscriber = ftvstt.Bertin("https://demo02.mediaspeech.com:4433/api")
bertinTranscriber.authenticate("EXAMPLE_ID","EXAMPLE_PASS")
transcript = bertinTranscriber.transcribe("/path/to/file.wav")
bertinTranscriber.deauthenticate()
```

Amazon transcribe:
```python
amazonTranscriber = ftvstt.Amazon("AMAZON_S3_BUCKET_NAME")
amazonTranscriber.authenticate("AMAZON_AWS_ID_KEY", "AMAZON_AWS_SECRET_KEY")
transcript = amazonTranscriber.transcribe("/path/to/file.wav")
amazonTranscriber.deauthenticate()
```
You can also authenticate directly with path to the credentials csv file:
```python
amazonTranscriber.authenticate_with_file("/path/to/amazon/credentials.csv")
```

You need an amazon AWS S3 bucket besides Amazon AWS Transcribe in order to make transcriptions.

If your file is already on a S3 bucket, use instead:
```python
transcript = amazonTranscriber.transcribe("https://url/to/s3/file.wav", s3file=True)
```

Google cloud speech-to-text:
```python
googleTranscriber = ftvstt.Google()
googleTranscriber.authenticate("GOOGLE_CLIENT_EMAIL", "GOOGLE_PIVATE_KEY")
transcript = googleTranscriber.transcribe("/path/to/file.wav")
googleTranscriber.deauthenticate()
```
You can also authenticate directly with path to client service credentials json file with google.
```python
googleTranscriber.authenticate_with_file("/path/to/google/credentials.json")
```


# Custom vocabulary file

For every provider except Bertin, you can add a custom vocabulary file of probable words as shown :
```python
googleTranscriber = ftvstt.Google()
googleTranscriber.authenticate_with_file("/path/to/google/credentials.json")
googleTranscriber.set_vocabulary_file("/path/to/vocabulary/file.txt")
transcript = googleTranscriber.transcribe("/path/to/file.wav")
googleTranscriber.deauthenticate()
```

The vocabulary file should be of the form:
```
word1
word2
word3
...
```

# Results handling

Once a transcription is done, the transcribe function of a Transcriber returns a Transcript instance from ftvstt.transcripts sub-module.

A Transcript instance, as transcript in previous codes, has several useful attributes :

**transcript.text**: a string containing the textual transcript of the audio file.  
**transcript.words**: a list of Word instances from ftvstt.transcripts sub-module, each one has a content (str), a startTime (float), an endTime (float), a speaker (Speaker instance from ftvstt.transcripts sub-module) (and can have a confidence (float) depending on the provider used) attribute.  
**transcript.speakers**: a list of Speaker instances from ftvstt.transcripts sub-module, each one has an id (int), (and can have a gender (str : "M" or "F") depending on the provider used).  
**transcript.raw**: a string containing the raw result of the transcription received from the provider, which type is transcript.rawType (str : "json" or "xml").

You can also dump the results in a normalised (the same format for any provider) json file:
```python
transcript.dump_normalised_result("/output/path/to/normalized/result.json")
```

You can also load a transcript from a raw result file:
```python
with open("/path/to/bertin/raw/result.xml") as file:
    raw = file.read()

transcript = ftvstt.Transcript(raw=raw, provider=ftvstt.Bertin)
```
# Error handling

If an error has occured during transcription, a custom python Exception from the ftvstt.exceptions sub-module will be raised. The error will also be accessbile in the exception attribute of the transcript result, as you can see in this example:

```python
googleTranscriber = ftvstt.Google()
googleTranscriber.authenticate("/path/to/google/credentials.json")
try:
    transcript = googleTranscriber.transcribe("/path/to/file.wav")
except:
    pass
raise transcript.exception
googleTranscriber.deauthenticate()
```

# Testing

Coming soon...
