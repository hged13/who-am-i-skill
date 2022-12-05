from mycroft import MycroftSkill, intent_file_handler
import pandas as pd
import librosa




class WhoAmI(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('i.am.who.intent')
    def handle_i_am_who(self, message):
        self.speak_dialog('i.am.who')
        model = self.build_model()

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
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

        dtc = KNeighborsClassifier(n_neighbors=4)
        dtc.fit(X_train, y_train)

        y_pred = dtc.predict(X_test)
            

    def features_extractor(self,file):
        audio, sample_rate = librosa.load(file, res_type='kaiser_fast')
        mfcss_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
        mfccs_scaled_features = np.mean(mfcss_features.T, axis=0)

        return mfccs_scaled_features


def create_skill():
    return WhoAmI()
