This collection of scripts is to receive line-in audio from a police scanner,
save it to a set of 59 second files, and send each off to Google Transcribe
service to be turned into text. This text is then parsed and sent to a web
page to be presented to the user in descending order.

Since the line input will be shared on a live darkice stream as well as being
parsed by the transcription service, the ALSA input must be split into two
parts. The easiest way is to define two virtual `dsnoop` interfaces inside of
a `.asoundrc` file as follows:

    pcm.scanner_files {
    	type dsnoop
    	ipc_key 234884
    	slave {
    		pcm "hw:0,0"
    		channels 1
    		rate 8000
    	}
    	bindings.0 0
    }

    pcm.scanner_stream {
    	type dsnoop
    	ipc_key 234884
    	slave {
    		pcm "hw:0,0"
    		channels 1
    		rate 22050
    	}
    	bindings.0 0
    }

Then `arecord` can be set up to constantly listen on the interface and make a
series of 16000 bitrate mono WAV files.

    arecord -f S16_LE -D plug:scanner_files --max-file-time 59 \
      --use-strftime scanner-%Y-%m-%d-%H-%M-%S.wav

The files are created when the recording begins and labeled with a local timestamp in the filename. The result looks something like below:

    rob@focus:~/scanner$ ls -l|tail -4
    -rw-r--r-- 1 rob rob 944044 Jun 17 16:58 scanner-2018-06-17-16-57-45.wav
    -rw-r--r-- 1 rob rob 944044 Jun 17 16:59 scanner-2018-06-17-16-58-44.wav
    -rw-r--r-- 1 rob rob 944044 Jun 17 17:00 scanner-2018-06-17-16-59-43.wav

When completed, a 59 second file at 16000 bytes per second will be 944044 bytes
including a 44 byte WAV file header.

We need to detect when the files are completed which we can define as:

* 944044 bytes - except when something goes wrong with arecord
* No longer open by arecord writer
* A file with a newer date exists

The [watchdog library](https://pythonhosted.org/watchdog/api.html) seems to be
a good way to detect when the next sequence file is created and use that.
Trying to monitor if the current file stops being modified is less efficient
because every write from `arecord` triggers an event. The watchdog module
also has an issue where the inotify watch limit can be reached with a large
number of files.

In order to not send duplicate files to Google Transcription service the
script must be aware of files that it has already sent. Several possible methods
to achieve this are:

* Move the file from the current to an archive directory once processed
* Keep a list of items already sent to Google and the results received
* Need some way to represent that an empty result was received

These can be stored in either a local database or a simpler file structure for temporary use.

# Setup of this Project

    pip freeze > requirements.txt
    pip install -r requirements.txt

    export GOOGLE_APPLICATION_CREDENTIALS='/home/rob/Transcription Scanner-5c2677f79ba7.json'
