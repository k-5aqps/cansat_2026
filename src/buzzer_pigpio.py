# -*- coding: utf-8 -*-
#ゴール後ブザーを鳴らしゴールを周知する
import pigpio
import time
import csv

buzzerpin=18

pi = pigpio.pi()

tempo = 146
note_length = 60/tempo

pitch_dic = {
        'C3':131,     'C#3':139,    'D3':147,
        'D#3':155,    'E3':165,     'F3':175,
        'F#3':185,    'G3':196,     'G#3':208,
        'A3':220,
        'A#3': 233,   'B3': 246,    'C4': 261,
        'C#4': 277,   'D4': 293,    'D#4': 311,
        'E4': 329,    'F4': 349,    'F#4': 370,
        'G4': 392,    'G#4': 415,   'A4': 440,
        'A#4': 466,   'B4': 493,    'C5': 523,
        'C#5': 554,   'D5': 587,    'D#5': 622,
        'E5': 659,    'F5': 698,    'F#5': 740,
        'G5': 783,  'G#5': 830,   'A5': 880,
        'A#5': 932,   'B5': 987,    'C6': 1046,
        'C#6': 1108,  'D6': 1174,   'D#6': 1244,
        'E6': 1318,   'F6': 1396,   'F#6': 1480,
        'G6': 1568,   'G#6': 1661,  'A6': 1760,
        'A#6': 1864,  'B6': 1975,   'C7': 2093,
        'C#7':1109,   'D7':1175,    'D#7':1245,
        'E7':1319
    }

duration_dic = {
    'whole': 1,            'half' : 0.5,
    'one-third' : 1/3,     'quarter' : 0.25,
    'dotted_eighth':0.75,'rest_little':1/40,
    'dotted_double':2.5,'double':2,
    'dotted_whole':1.5
}

def init():
    pi.set_mode(buzzerpin, pigpio.OUTPUT)

def read_music(filename:str):
    global tempo, note_length
    with open(filename, mode = "r",encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        sheet = [row for row in reader]
    tempo = int(sheet[0][0])
    note_length = 60/tempo
    sheet.pop(0)
    for notes in sheet:
        if notes == []:
            return
        mode, note1, note2, note3,duration = notes
        match mode:
            case 'rest':
                rest(duration)
            case '1':
                note(note1,duration)
            case '2':
                coard(note1, note2, duration)
            case '3':
                triad(note1, note2, note3, duration)
            case 'tempo':
                tempo = int(note1)
                note_length = 60/tempo
        rest("rest_little")

def music_Mario():
    coard('C4', 'G4', 'one-third')
    coard('E4', 'C5', 'one-third')
    coard('G4', 'E5', 'one-third')
    coard('C5', 'G5', 'one-third')
    coard('E5', 'C6', 'one-third')
    coard('G5', 'E6', 'one-third')
    coard('E6', 'G6', 'whole')
    coard('C6', 'E6', 'whole')
    coard('C4', 'G#4', 'one-third')
    coard('D#4', 'C5', 'one-third')
    coard('G#4', 'D#5', 'one-third')
    coard('C5', 'G#5', 'one-third')
    coard('D#5', 'C6', 'one-third')
    coard('G#5', 'D#6', 'one-third')
    coard('D#6', 'G#6', 'whole')
    coard('C6', 'D#6', 'whole')
    coard('D4', 'A#4', 'one-third')
    coard('F4', 'D5', 'one-third')
    coard('A#4', 'F5', 'one-third')
    coard('D5', 'A#5', 'one-third')
    coard('F5', 'D6', 'one-third')
    coard('A#5', 'F6', 'one-third')
    coard('F6', 'A#6', 'whole')
    coard('D6', 'A#6', 'one-third')
    coard('D6', 'A#6', 'one-third')
    coard('D6', 'A#6', 'one-third')
    coard('C6', 'C7', 'whole')
    coard('C6', 'C7', 'whole')
    for i in range(0, 3):
        rest('whole')

def note(pitch, duration):
    pi.hardware_PWM(buzzerpin,pitch_dic[pitch],500000)
    time.sleep(note_length * duration_dic[duration])

def rest(duration):
    pi.hardware_PWM(buzzerpin,0,0)
    time.sleep(note_length * duration_dic[duration])
    pi.hardware_PWM(buzzerpin,50,0)

def coard(pitch1, pitch2, duration):
    count = 0
    while True:
        pi.hardware_PWM(buzzerpin,pitch_dic[pitch1],500000)
        time.sleep(0.02)
        pi.hardware_PWM(buzzerpin,pitch_dic[pitch2],500000)
        time.sleep(0.02)
        count += 1
        if(note_length * duration_dic[duration] <= count*0.04):
            break

def triad(pitch1, pitch2, pitch3, duration):
    count = 0
    while True:
        pi.hardware_PWM(buzzerpin,pitch_dic[pitch1],500000)
        time.sleep(0.02)
        pi.hardware_PWM(buzzerpin,pitch_dic[pitch2],500000)
        time.sleep(0.02)
        pi.hardware_PWM(buzzerpin,pitch_dic[pitch3],500000)
        time.sleep(0.02)
        count += 1
        if(note_length * duration_dic[duration] <= count*0.06):
            break

def main():
    init()
    read_music("dango.csv")

    #buzz()

if __name__ == "__main__":
    main()
