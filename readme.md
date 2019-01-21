Plan is to generate some new lecture based on previous lectures and corpora
learned from them. list of used lectures: 
- https://www.youtube.com/watch?v=EXGFGvpadnE
- https://www.youtube.com/watch?v=AerWN3xXmuk
- https://www.youtube.com/watch?v=p2IsK53lEEc
- https://www.youtube.com/watch?v=m43zk_iaIcw
- https://www.youtube.com/watch?v=dCFB11dpFJo
- https://www.youtube.com/watch?v=qJX5grOtZmU
- https://www.youtube.com/watch?v=XkoxK7dJz5E
- https://www.youtube.com/watch?v=d1kBTnFEjMI
- https://www.youtube.com/watch?v=9llfV_WINto
- https://www.youtube.com/watch?v=XmGr0CCEzhc
- https://www.youtube.com/watch?v=U50SJwORuPY
- https://www.youtube.com/watch?v=AMR09Chqxc0

-   speech to text
    -   google api speech to text: https://cloud.google.com/speech-to-text/docs/
    -   files are big, so I must upload them to the google cloud storage (GCS)
        -   I created new regional bucket in EU here
            https://console.cloud.google.com/storage
        -   I upload here all lectures        
    -   then I set project in command line, being sure I use project ID, not the
        project name `gcloud config set project divine-glazing-140110` and then
        I can finally use the speech to text, be sure audio files are in wav or
        flac (note: console in browser works a bit better than desktop version)
        `gcloud ml speech recognize-long-running
        "gs://european-germany-bucket/mono-[NatsuCon2013] Grek1 - Mahó šódžo
        včera dnes a zítra.wav" --async --language-code="cs-CZ"` it returns the
        job it, with it we can control its progress If I want to hint some words
        for it, I can do it by passing it as hints: `gcloud ml speech
        recognize-long-running "gs://european-germany-bucket/mono-[NatsuCon2013]
        Grek1 - Mahó šódžo včera dnes a zítra.wav" --async
        --language-code="cs-CZ" --hints="[mahó, šódžó]"` the following command
        shows progress of the job, and after it's done, it outputs the result
        `gcloud ml speech operations describe "3785909817154180023"` when job is
        done, we save the resulting json into file `gcloud ml speech operations
        describe "3785909817154180023" | gsutil cp -
        "gs://european-germany-bucket/[NatsuCon2013] Grek1 - Mahó šódžo včera
        dnes a zítra.json" gcloud ml speech operations wait
        "1719105980631949569" | gsutil cp - "gs://european-germany-bucket/Grek1
        -  IKEA Záporáci.json"` waits until the job is over and then saved its
        result into json file
    - for creating the subtitle format, I can use this: https://github.com/Naki21/google-speech-to-text
    
-   new text generations there are PDF's with some approaches, other approaches
    are:
    -   https://github.com/tensorflow/models/tree/master/research/maskgan
    -   https://medium.com/@G3Kappa/writing-a-weight-adjustable-markov-chain-based-text-generator-in-python-9bbde6437fb4
    -   https://www.analyticsvidhya.com/blog/2018/03/text-generation-using-python-nlp/

-   text to speech Generated lecture will then be transferred into audio
    -   using some known libraries for TTS
        -   either by https://github.com/marytts/marytts if it will work Marytts is
            built from source to add new language. Marytts is installed through the
            installer to be used as txt to wav server.
            -   very research, lots of features, still evolving, no detailed up-to-date 
                documentation. Not practical to use.
        -   or https://github.com/espeak-ng/espeak-ng could be used. Need to find
            out how to add new voice. Has czech support
        -   or use the Festival
            https://en.wikipedia.org/wiki/Festival_Speech_Synthesis_System, it has
            guide for creating voices http://festvox.org/festvox/festvox_toc.html
            https://pdfs.semanticscholar.org/8be7/32f13c3ab0b14bea9179775df006a607c365.pdf
    -   training neural network for TTS - I'll probably use that, can use that to overfit on one voice
        -   there have been some paper lately for TTS using attention-based models.
            -   e.g.: https://github.com/mozilla/TTS, https://arxiv.org/pdf/1703.10135.pdf
            https://deepmind.com/blog/wavenet-generative-model-raw-audio/ etc.
        - some reddit discussions for it 
            - https://www.reddit.com/r/MachineLearning/comments/867y9m/d_facebook_unable_to_replicate_google_tacotron/
            - https://www.reddit.com/r/MachineLearning/comments/845uji/d_are_the_hyperrealistic_results_of_tacotron2_and/
            - https://www.reddit.com/r/MachineLearning/comments/7ksuh7/r_tacotron_2_natural_tts_synthesis_by/
-   tooling and data preparation
    -   for extraction audio from video, I used VLC player, which can export flac audio from video
    -   for downloading from youtube, both video and audio, I used https://www.onlinevideoconverter.com
    -   for trimming and cutting longer video, I used Movico (desktop app for windows 10, with ads but for free and does the job)
    -   for converting other audio formats to wav, I used Sound Converter (desktop app for windows 10)
    
- data structure:
    - in `text_out/google-stt` are automatically generated subtitles 
    - in `text_out/corrected-final` are final versions of srt files 
    - in `text_out/corrected-final-for-nlp` are final versions of srt file modified to be more suitable for NLP
    - in `pure_text_dataset` are pure text sentences from previous directory