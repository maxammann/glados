import distutils
import subprocess

LAME_ARGUMENTS = "--decode --silent --mp3input -t --signed --bitwidth 16 --little-endian --resample 16 - -".split(" ")
FFMPEG_ARGUMENTS = "-i pipe:0 -loglevel quiet -f s16le -acodec pcm_s16le -r 16000 pipe:1".split(" ")


def find_decoder():
    lame = distutils.spawn.find_executable("lame")

    if lame is not None:
        print("Using lame as decoder")
        return [lame] + LAME_ARGUMENTS

    ffmpeg = distutils.spawn.find_executable("ffmpeg")

    if ffmpeg is not None:
        print("Using ffmpeg as decoder")
        return [ffmpeg] + FFMPEG_ARGUMENTS

    raise NotImplementedError("Lame and ffmpeg wasn't found!")


decoder = find_decoder()


def mp3_decode(audio_data):
    try:
        call = subprocess.Popen(decoder, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        return call.communicate(input=audio_data)[0]
    except subprocess.CalledProcessError as e:
        raise IOError(e)
