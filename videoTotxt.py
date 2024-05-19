import subprocess
from subprocess import run
from pydub import AudioSegment
from faster_whisper import WhisperModel
from typing import Iterator, TextIO
from stable_whisper import modify_model
import stable_whisper


def extract_audio(input_m3u8, filename,ffmpeg_path):
    # Step 1: Download video segments
    print("started download")
    download_command = [
        ffmpeg_path,
        '-protocol_whitelist', 'file,http,https,tcp,tls',
        '-i', input_m3u8,
        '-c', 'copy',
        filename+'_mp4_video.mp4'
    ]
    run(download_command)

    # Step 2: Extract audio from the video file
    print("started extract")
    extract_command = [
        ffmpeg_path,
        '-i', filename+'_mp4_video.mp4',
        '-vn',
        '-acodec', 'copy',
        filename + '.aac'
    ]
    run(extract_command)
    print(f"Audio extraction completed. Output audio file: {filename}.aac")

def convert_aac_to_wav(output_audio,ffmpeg_path):
    output_audio_acc = output_audio + '.aac'
    print(output_audio,'<--- output_audio')
    convert_command = f'{ffmpeg_path} -i {output_audio_acc} -c pcm_s16le -ar 44100 {output_audio+".wav"}'
    result = subprocess.run(convert_command, shell=True, capture_output=True)
    print(result.stdout.decode(),'##########')

def convert_wav_to_mp3(filename,ffmpeg_path):
    wav_file = filename + ".wav"
    mp3_file = filename + ".mp3"
    convert_command = f'{ffmpeg_path} -i {wav_file} -ar 44100 -ac 2 -b:a 192k {mp3_file}'
    result = subprocess.run(convert_command, shell=True, capture_output=True)
    print(result.stdout.decode(),'<---- convert')

def split_audio(filename,wav_audio):
    song = AudioSegment.from_mp3(wav_audio)
    audio_end_time = 54 * 60 * 1000
    mins = 4
    start_time = 0
    filenamecount = 1

    for i in range(13):
        # PyDub handles time in milliseconds
        end_time = mins * 60 * 1000
        first_10_minutes = song[start_time:end_time]
        filenameExport = filename +'_'+ str(filenamecount) + '.wav'
        first_10_minutes.export(filenameExport, format="wav")
        start_time = end_time
        mins = mins + 4
        filenamecount = filenamecount + 1

def timestamp(timeFile,list1):
    with open(timeFile, 'w') as fp:
        fp.write(str(list1))
def generate_transcribe(filename):
    model = WhisperModel("small.en")
    filenamecount = 1
    for i in range(13):
        listAll = []
        textAll = []
        audio_name = filename + '_' + str(filenamecount) + '.wav'
        transcribe_txt = 'Transcribe'+'_'+filename+"_"+str(filenamecount)+'.txt'
        segments, info = model.transcribe(audio_name, language="en", word_timestamps=True)
        #print(segments,'<------- segments')
        #print(type(segments), '<------- type - segments')
        for index, segment in enumerate(segments):
            dictname = {"Word_": segment.text, "Start_": segment.start, "End_": segment.end}
            print(dictname)

            #listAll.append(dictname)
            #textAll.append(dictname)
            #print(textAll,'<------ textAll')
    '''
        with open(transcribe_txt, 'w') as fp:
            fp.write(str(listAll))
        filenamecount = filenamecount + 1
    with open("transcribe_txt", 'w') as fp:
        fp.write(str(textAll))
    '''
def SRT_transcribe(audio):
    print("SRT Transcription")
    model = stable_whisper.load_faster_whisper('small.en')
    filenamecount = 1
    for i in range(13):
        audio_name = filename + '_' + str(filenamecount) + '.wav'
        file_SRT = "FS_whisper_SRT_" + str(filenamecount)
        result = model.transcribe_stable(audio_name)
        result.to_srt_vtt(file_SRT,segment_level=False,word_level=True)
        print("Completed",filenamecount)
        filenamecount = filenamecount + 1
    print("Completed - ALL")

if __name__ == "__main__":
    filename = '95683'
    input_m3u8 = r"D:\@apps\ELCS\video_captioning\Videos\95683\95683.m3u8"
    ffmpeg_path = r"C:\Users\Sivaraman.V\ffmpeg-2024-01-01_build\bin\ffmpeg.exe"
    # Step 1: Extract audio
    #extract_audio(input_m3u8, filename, ffmpeg_path)
    #convert_aac_to_wav(filename,ffmpeg_path)
    #wav_audio = "95683.wav"
    #split_audio(filename,wav_audio)
    #generate_transcribe(filename)
    SRT_transcribe(filename)