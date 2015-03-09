import os
import subprocess
import midi

from pydub import AudioSegment


def sample_midi(filename, total_length=(60 * 1000000) * 30):
    """
    Return a sampling of the midi file

    total_length of the sample is 30 seconds by default
    """
    pattern = midi.read_midifile(filename)

    new_pattern = midi.Pattern()
    new_track = midi.Track()

    events = []

    for track in pattern:
        if isinstance(track, midi.Track):
            # new_track = midi.Track()
            # new_pattern.append(new_track)
            for event in track:
                events.append(event)

    if len(events) > 2:
        # Take a sampling of the midi
        beginning = len(events) / 8
        end = len(events) / 6

        new_track = events[beginning:end]

        new_pattern.append(new_track)

        # Add End of Track line
        eot = midi.EndOfTrackEvent(tick=1)
        new_track.append(eot)

    return new_pattern

# sampled_midi = sample_midi("mary.mid")
# midi.write_midifile("mary2.mid", sampled_midi)


def is_fluidsynth_installed():
    """ Check to make sure fluidsynth exists in the PATH """
    for path in os.environ['PATH'].split(os.pathsep):
        f = os.path.join(path, 'fluidsynth')
        if os.path.exists(f) and os.access(f, os.X_OK):
            return True

    return False


def convert_to_audio(midi_file, soundfont='fluidr3_gm2-2.sf2', output_path='../pianosite/public/media/audio/', output_types=['oga']):
    """
    Convert a single midi file to an audio given a list of output_types

    paramters:
    `midi_file`: the filename of the midi file to convert
    `soundfont`: the soundfont filename used in converting the midi to audio
    `output_types`: accepted file output types (wav, oga, ogg, etc.)
    """
    if not soundfont:
        return "You need to download a soundfont file to convert the midi into audio!"
    try:
        filename = midi_file.split(".")[0]

        for output_type in output_types:
            output_filename = u"{}{}.{}".format(
                output_path, filename, output_type
            )
            subprocess.call(
                [
                    'fluidsynth', '-T', output_type, '-F', output_filename,
                    '-ni', soundfont, midi_file
                ]
            )
    except:
        raise "Incorrect File type or file has no name!"


def slice_audio(audio_file, file_type='oga', length=(30 * 1000)):
    """
    Using pydub to slice 30 seconds from the middle of the song
    """
    song = None
    if file_type == 'oga':
        song = AudioSegment.from_ogg(audio_file)

    if song:
        if song.duration_seconds <= length:
            """ If the song is less than 30 seconds, give them half """
            song = song[:song.duration_seconds / 2]

        else:
            song = song[(length - (length / 2)):(length + (length * 2))]

        song.export(u"{}_slice.{}".format(audio_file, file_type), format=file_type)

# convert_to_audio(soundfont='fluidr3_gm2-2.sf2', output_path='../pianosite/public/media/audio/')
