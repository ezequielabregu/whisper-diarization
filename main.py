import whisper
from pyannote.audio import Pipeline
from pyannote_whisper.utils import diarize_text
import subprocess

title = 'AI transcription example'

with open("output/text.txt",'w') as file:
    pass
with open("output/text_full_timestamps.txt",'w') as file:
    pass
with open("output/markdown/first_timestamp.md",'w') as file:
    pass
with open('output/markdown/first_timestamp.md', 'a') as f:
    f.write('# ' + title + '\n')
    f.write('\n')
with open("output/markdown/speaker_number.md",'w') as file:
    pass
with open("output/markdown/speaker_name.md",'w') as file:
    pass

pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                    use_auth_token="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")
model = whisper.load_model("base")
asr_result = model.transcribe("data/audio-short.wav")
diarization_result = pipeline("data/audio-short.wav")
final_result = diarize_text(asr_result, diarization_result)

def transcribe():
    for seg, spk, sent in final_result:
        line = f'{seg.start:.2f} {seg.end:.2f} {spk} {sent}'                  
        #line = (f'{seg} {spk} {sent}') 
        with open('output/text.txt', "a", encoding='utf-8') as file:
            file.write(line + "\n")
            #file.write("\n")

def full_timestamps():
    for seg, spk, sent in final_result:
        line = f'{seg} {spk} {sent}'                  
        #line = (f'{seg} {spk} {sent}') 
        with open('output/text_full_timestamps.txt', "a", encoding='utf-8') as file:
            file.write(line + "\n")
            #file.write("\n")

def first_timestamp():
    with open('output/text.txt', 'r') as f:
        lines = f.readlines()

    output_lines = []
    current_speaker = ''
    current_line = ''
    
    for line in lines:
        start_time, end_time, speaker, text = line.split(maxsplit=3)

        start_time = float(start_time)
        minutes = start_time // 60
        hour = start_time // 3600
        seconds = start_time % 60
        millis = start_time - int(start_time)
        time_format = "%02d:%02d:%02d" % (hour, minutes, seconds)

        if speaker == current_speaker:
            current_line += ' ' + text.strip()
        else:
            if current_line:
                output_lines.append(current_line)
            current_speaker = speaker
            current_line = f'[{time_format}] **{speaker}**: {text.strip()}'
    if current_line:
        output_lines.append(current_line)

    for line in output_lines:
        #print(line)
        with open('output/markdown/first_timestamp.md', 'a') as f:
            f.write(line + '\n')
            f.write('\n')


def speaker_number():
    with open('output/text.txt', 'r') as f:
        lines = f.readlines()

    concatenated_lines = []
    current_speaker = None
    current_sentence = ''
    for line in lines:
        parts = line.strip().split()
        start_time = float(parts[0])
        end_time = float(parts[1])
        speaker = parts[2]
        sentence = ' '.join(parts[3:])
        if current_speaker is None:
            current_speaker = speaker
        if current_speaker == speaker:
            current_sentence += sentence + ' '
        else:
            concatenated_lines.append(f'**{current_speaker}**: {current_sentence.strip()}')
            concatenated_lines.append('')
            current_speaker = speaker
            current_sentence = sentence + ' '

    # Add the last sentence
    concatenated_lines.append(f'**{current_speaker}**: {current_sentence.strip()}')

    # Write the concatenated lines to a new file
    with open('output/markdown/speaker_number.md', 'w') as f:
        f.write('# ' + title + '\n')
        f.write('\n')
        f.write('\n'.join(concatenated_lines))


def speaker_name(name_0, name_1, name_2, name_3, name_4):
    with open('output/text.txt', 'r') as f:
        lines = f.readlines()

    speaker_names = {
        'SPEAKER_00': name_0,
        'SPEAKER_01': name_1,
        'SPEAKER_02': name_2,
        'SPEAKER_03': name_3,
        'SPEAKER_04': name_4,
    }

    concatenated_lines = []
    current_speaker = None
    current_sentence = ''
    for line in lines:
        parts = line.strip().split()
        start_time = float(parts[0])
        end_time = float(parts[1])

        minutes = int(start_time) // 60
        hour = int(start_time) // 3600
        seconds = start_time % 60
        millis = start_time - int(start_time)
        time_format = "%02d:%02d:%02d" % (hour, minutes, seconds)

        speaker = speaker_names.get(parts[2], parts[2]) # Use speaker name if available, else use speaker ID
        sentence = ' '.join(parts[3:])
        if current_speaker is None:
            current_speaker = speaker
        if current_speaker == speaker:
            current_sentence += sentence + ' '
        else:
            #concatenated_lines.append(f'{start_time:.2f} {end_time:.2f} **{current_speaker}**: {current_sentence.strip()}')
            concatenated_lines.append(f'**{current_speaker}**: {current_sentence.strip()}')

            concatenated_lines.append('')
            current_speaker = speaker
            current_sentence = sentence + ' '

    # Add the last sentence
    concatenated_lines.append(f'**{current_speaker}**: {current_sentence.strip()}')

    # Write the concatenated lines to a new file
    with open('output/markdown/speaker_name.md', 'w') as f:
        f.write('# ' + title + '\n')
        f.write('\n')
        f.write('\n'.join(concatenated_lines))


def converter(filename):
    file_1 = 'output/markdown/' + filename +'.md'
    file_pdf = 'output/pdf/' + filename + '.pdf'
    file_docx = 'output/docx/' + filename + '.docx'
    
    args_pdf = ['pandoc', file_1, '--pdf-engine=/usr/local/texlive/2023basic/bin/universal-darwin/xelatex', '-o', file_pdf]
    subprocess.check_call(args_pdf)

    args_docx = ['pandoc', '-s', file_1,'-o', file_docx]
    subprocess.check_call(args_docx)

    return "Files converted sucessfully"

transcribe()
full_timestamps()
first_timestamp()
speaker_number()
speaker_name('Maria B.', 'Jean S.', 'Speaker 3', 'Speaker 4', 'Speaker 5')

converter('first_timestamp')
converter('speaker_name')






##################################################
''' 
def timestamp_speaker():
    with open('output/text.txt', 'r') as f:
        lines = f.readlines()

    concatenated_lines = []
    current_speaker = None
    current_sentence = ''
    for line in lines:
        parts = line.strip().split()
        start_time = float(parts[0])
        end_time = float(parts[1])

        minutes = int(start_time) // 60
        hour = int(start_time) // 3600
        seconds = start_time % 60
        millis = start_time - int(start_time)
        time_format = "%02d:%02d:%02d" % (hour, minutes, seconds)

        speaker = parts[2]
        sentence = ' '.join(parts[3:])
        if current_speaker is None:
            current_speaker = speaker
        if current_speaker == speaker:
            current_sentence += sentence + ' '
        else:
            #concatenated_lines.append(f'{start_time:.2f} {end_time:.2f} **{current_speaker}**: {current_sentence.strip()}')
            concatenated_lines.append(f'[{time_format}] **{current_speaker}**: {current_sentence.strip()}')
            concatenated_lines.append('')
            current_speaker = speaker
            current_sentence = sentence + ' '

    # Add the last sentence
    #concatenated_lines.append(f'{start_time:.2f} {end_time:.2f} **{current_speaker}**: {current_sentence.strip()}')
    concatenated_lines.append(f'{time_format}] **{current_speaker}**: {current_sentence.strip()}')

    # Write the concatenated lines to a new file
    with open('output/timestamps_speakers.md', 'w') as f:
        f.write('# ' + title + '\n')
        f.write('\n')
        f.write('\n'.join(concatenated_lines)+ '\n')


'''

'''
def speakers_only():
    with open('output/text.txt', 'r') as f:
        lines = f.readlines()

    concatenated_lines = []
    current_speaker = None
    current_sentence = ''
    for line in lines:
        parts = line.strip().split()
        start_time = float(parts[0])
        end_time = float(parts[1])
        speaker = parts[2]
        sentence = ' '.join(parts[3:])
        if current_speaker is None:
            current_speaker = speaker
        if current_speaker == speaker:
            current_sentence += sentence + ' '
        else:
            concatenated_lines.append(f'**{current_speaker}**: {current_sentence.strip()}')
            concatenated_lines.append('')
            current_speaker = speaker
            current_sentence = sentence + ' '

    # Add the last sentence
    concatenated_lines.append(f'**{current_speaker}**: {current_sentence.strip()}')

    # Write the concatenated lines to a new file
    with open('output/speakers_only.md', 'w') as f:
        f.write('# ' + title + '\n')
        f.write('\n')
        f.write('\n'.join(concatenated_lines)+ '\n')
'''