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


def convert_to_audio(midi_filename, soundfont='fluidr3_gm2-2.sf2', output_path='../pianosite/public/media/audio/', output_types=['oga']):
    """
    Convert a single midi file to an audio given a list of output_types

    paramters:
    `midi_filename`: the filename of the midi file to convert
    `soundfont`: the soundfont filename used in converting the midi to audio
    `output_types`: accepted file output types (wav, oga, ogg, etc.)
    """
    if not soundfont:
        return "You need to download a soundfont file to convert the midi into audio!"
    try:
        filename = midi_filename.split(".")[0]

        for output_type in output_types:
            output_filename = u"{}{}.{}".format(
                output_path, filename, output_type
            )
            subprocess.call(
                [
                    'fluidsynth', '-T', output_type, '-F', output_filename,
                    '-ni', soundfont, midi_filename
                ]
            )

        # return output_filename
    except:
        raise "Incorrect File type or file has no name!"


def slice_audio(audio_file_name, length=(30 * 1000)):
    """
    Using pydub to slice 30 seconds from the middle of the song

    Output ogg and mp3 file types
    """
    song = None

    try:
        file_name = audio_file_name.split(".")[0]
        file_type = audio_file_name.split(".")[1]

        if file_type == 'oga':
            file_type = 'ogg'
            song = AudioSegment.from_ogg(audio_file_name)
        elif file_type == 'mp3':
            song = AudioSegment.from_mp3(audio_file_name)

        if song:
            if song.duration_seconds * 1000 <= length:
                """ If the song is less than 30 seconds, give them half """
                song = song[:(song.duration_seconds / 2) * 1000]

            else:
                lower_bound = length - (length / 2)
                song = song[lower_bound:(length * 2) - lower_bound].fade_in(2000).fade_out(3000)

            slice_file_name = u"{}_slice.{}".format(file_name, file_type)
            song.export(slice_file_name, format=file_type)

            return slice_file_name

    except IOError as e:
        print e.errno
        print e


# convert_to_audio(midi_filename="mary.mid")
# slice_audio(audio_file_name="mary.ogg")
