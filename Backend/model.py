from sklearn.preprocessing import StandardScaler
from keras.models import load_model
import matplotlib

matplotlib.use("Qt5Agg")
print(matplotlib.get_backend())

import matplotlib.pyplot as plt
from pydub import AudioSegment
import soundfile as sf
import numpy as np
import warnings
import librosa
import time
warnings.filterwarnings('ignore')

class model_class():
    def __init__(self,feature_path,silence_path, plot_path, wav_size=4000, scal=True, english_path=None):
        # self.model_path = base_path+'/'+model_path
        # self.english_path = base_path+english_path
        # self.german_path = base_path+'/'+german_path
        self.feature_path = feature_path
        self.plot_path = plot_path
        self.sil_path =  silence_path
        self.wav_size = wav_size
        self.scal = scal
        


    def show_data(self,data,name):
        plt.figure()
        plt.title("data")
        plt.savefig(name)
        plt.plot(data)
        plt.show()
        return plt

    def add_silence(self,infile,outfile,size):
        audio_in_file = infile
        audio_out_file = outfile

        if 'wav' in audio_in_file:
            song = AudioSegment.from_wav(audio_in_file)
            # print(max(song,key=len))
            if len(song)<size: 
                for i in range(100,10000,100):
                    one_sec_segment = AudioSegment.silent(duration=i)  #duration in milliseconds
                    sec_segment = AudioSegment.silent(duration=100)  #duration in milliseconds    
                    # read wav file to an audio segment
            
                    # Add above two audio segments    
                    final_song =  sec_segment + song + one_sec_segment
                    # print(len(final_song))
            
                    if len(final_song)>size:
                        final_song = final_song[:size]
                        final_song.export(audio_out_file, format="wav")
                        break
            elif len(song) >= size:
                song = song[:size]
                song.export(audio_out_file,format='wav')
        return audio_out_file

    def feat(self,fileName,featPath,inp='mfcc'):
        x, sr = librosa.load(fileName)
        if inp == 'mfcc':
            data = librosa.feature.mfcc(x, sr=sr, n_mfcc = 40)
        elif inp == 'log_spect':
            data, phase = librosa.magphase(librosa.stft(x,n_fft=512))
        else:
            raise 'invalid feature extraction type'
        fileName = fileName.split('/')
        ext = featPath + fileName[-1][:-4]+'_'+inp+'.npy'
        # print(ext)
        with open(ext, 'wb') as f:
            np.save(f, data)
        return ext, data,sr

    def feat_exact(self, input, featpath,silencePath ,audio_size=4000,scal=True):
        outfile = input.split('/')
        # outfile = outfile[-1].split('.')
        dest_path = silencePath + outfile[-1]
        split =  input.split('/')
        dest_path = silencePath + split[-1]
        # print(dest_path)
        out = self.add_silence(input,dest_path,audio_size)
        # print(out)
        extracted,data, sr = self.feat(out,featpath)
        return extracted,data, sr

    def predict_model(self, model_path, og_path, file_feature, out_path, scale=True):
        extract, og, sr = self.feat_exact(input = file_feature, silencePath=self.sil_path, featpath=self.feature_path)
        #with open(file_feature,'rb') as f:
        x_in, sr = librosa.load(og_path)
        # og = np.load(f)
        default = og.shape
        print('original')
        if scale==True:
            standard_scaler = StandardScaler()
            dat = standard_scaler.fit_transform(og)
        else:
            dat = og
        dat = dat.flatten()
        dat = dat.reshape(1,dat.shape[0])
        print('input data shape: ',dat.shape)
        if np.isnan(np.sum(dat)):
            print("There is a NAN prensent in predicted output")
        # self.check_nan(dat)
        model = load_model(model_path)
        pred = model.predict(dat)
        # 
        deFlat =  np.reshape(pred,default)
        #
        if scale==True:
            deFlat = standard_scaler.inverse_transform(deFlat)
        if np.isnan(np.sum(deFlat)):
            print("There is a NAN prensent in predicted output")
            print('Is nans in input file: ',np.isnan(np.sum(deFlat)))
        audio_wav = librosa.feature.inverse.mfcc_to_audio(deFlat, n_mels = 40)
        # print('Audio plot')
        timestr = time.strftime("%Y_%m_%d-%I_%M_%S_%p")
        aud_path = 'Predicted-{%s}.wav'%timestr
        sf.write(out_path+aud_path, audio_wav, 16000, 'PCM_16')
        return og,deFlat,x_in,audio_wav,aud_path
    
    def save_plot(self,a,b,c,d,name):
        fig, axes = plt.subplots(2, 2, figsize=(10,8))
        axes[0][0].plot(a) # top plot
        axes[0][1].plot(b) # top plot
        axes[1][0].plot(c) # middle plot
        axes[1][1].plot(d) # top plot
        axes[0][0].set_title('Original data')
        axes[0][1].set_title('Predicted data') # top plot
        axes[1][0].set_title('Original wav') # middle plot
        axes[1][1].set_title('Predicted wav') # top plot'''
        tim = time.strftime("%Y-%m-%d-%I-%M-%S-%p")
        nea = "plot-{0}_{1}".format(name, tim)
        plt.savefig(self.plot_path+nea)
        plt.close(fig)
        return fig,nea
        
'''
    def main(self):
        #ext, sr = self.feat_exact(input = self.german_path,silencePath=self.sil_path,featpath=self.feature_path)
        og_dat,pred_dat,og_wave,pred_wav =  self.predict_model(model_path=self.model_path,og_path=self.Original_path,file_feature=self.german_path,out_path=self.predicted_path,scale=True)

Base_dir =  os.getcwd()
mod_path =  'models/Weights-016--0.16979.hdf5'
germ_og  =  'uploads/Ger_Three.wav'   # 'uploads/Ger-01.wav'
eng_path =  'uploads/Eng_Three.wav'   # 'uploads/Eng-01.wav'SS
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

if __name__ == '__main__':
    load = model_class(base_path = Base_dir, model_path=mod_path , german_path=germ_og)
    ger_og, predicted, audio_path =  load.main()
    load.show_data(ger_og)
    load.show_data(predicted)
    load.show_data(audio_path)
    load.og_pred(eng_path,predicted)    '''