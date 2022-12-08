from mycroft import MycroftSkill, intent_file_handler
import pandas as pd
import numba
import numpy as np
import librosa
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics

import wave 
import pyaudio
import csv




class WhoAmI(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.model = KNeighborsClassifier(n_neighbors=4)
        self.df = pd.read_csv('/home/pi/.config/mycroft/skills/NewUserCreation/log.csv', names=['name', 'playlist', 'artist'])
    
    def initialize(self):
       self.model = self.build_model()

    @intent_file_handler('i.am.who.intent')
    def handle_i_am_who(self, message):
        self.speak_dialog('i.am.who')
        pred = self.get_prediction_sample()
        predic = str(pred[0])
        plist = self.get_playlist(predic)
        self.speak_dialog(predic)
        self.speak_dialog(plist)
    
    def get_prediction_sample(self):
        rec = self.start_recording()
        features = self.features_extractor(rec)
        features = features.reshape(1,-1)
        answer = self.model.predict(features)
        return answer
    
    def get_playlist(self,name2):
        name3 = str(name2)
        walka = self.df.loc[self.df['name'].eq(name3), 'playlist']
        return walka
    
    
    def start_recording(self):
        dir = self.file_system.path
        namelite =  "hannah.wav"
        filename = dir + "/" + namelite
        frames = 1024
        FORMAT = pyaudio.paInt16
        channels = 1
        sample_rate = 22050
        record_seconds = 7
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    output=True,
                    frames_per_buffer=frames)
        frames2 = []
        self.speak_dialog("Recording...")
        for i in range(int(44100 / frames * record_seconds)):
            data = stream.read(frames)
            frames2.append(data)
        self.speak_dialog("Finished recording.")
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(filename, "wb")
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(sample_rate)
        wf.writeframes(b"".join(frames2))
        wf.close()
        return filename
    


    def build_model(self):
        file = open('/home/pi/.config/mycroft/skills/NewUserCreation/wav.csv', 'r')
        df = pd.read_csv(file)
        audio_data, sampling_rate = librosa.load(df.iloc[0][0])
        mfccs = librosa.feature.mfcc(y=audio_data, sr=sampling_rate, n_mfcc=40)
        extracted_features = []
        for row in df.itertuples(name='file_name'):
            file_name = row[1]
            data = self.features_extractor(file_name)
            speaker = row[2]
            extracted_features.append([data, speaker])

        extracted_features_df = pd.DataFrame(extracted_features, columns=['audio', 'speaker'])

        X = np.array(extracted_features_df['audio'].tolist())
        y = np.array(extracted_features_df['speaker'].tolist())
        
        

        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
        
        

        dtc = KNeighborsClassifier(n_neighbors=4)
        dtc.fit(X_train, y_train)

        y_pred = dtc.predict(X_test)
        ac = metrics.accuracy_score(y_test, y_pred)
        acc = []
        acc.append(ac)
        
        file = open('/home/pi/.config/mycroft/skills/NewUserCreation/name.csv', 'a')
        writer = csv.writer(file)
        writer.writerow(acc)


        
        return dtc
            

    def features_extractor(self,file):
        audio, sample_rate = librosa.load(file, res_type='kaiser_fast')
        mfcss_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
        mfccs_scaled_features = np.mean(mfcss_features.T, axis=0)

        return mfccs_scaled_features


def create_skill():
    return WhoAmI()
