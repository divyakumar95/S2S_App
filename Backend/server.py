from crypt import methods
from importlib.resources import contents
from subprocess import run, PIPE
from flask import Flask, render_template, request, request
from flask import json, send_from_directory, jsonify
from flask_cors import CORS
from model import model_class
import os
import warnings
import json
warnings.filterwarnings('ignore')

with open("config.json") as json_data_file:
    jd = json.load(json_data_file)

UPLOAD_FOLDER = jd['filepath']['upload']
ALLOWED_EXTENSIONS = {'mp3','wav'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'oh_so_secret'
app.config['BASE_URL'] = '/Users/admin/DBS_Assisgnments/Sem_3/Theses/Deployment/Backend/processed/predicted/' #'Backend'
app.config['IMAGE_URL'] = '/Users/admin/DBS_Assisgnments/Sem_3/Theses/Deployment/Backend/processed/plots/'
CORS(app, support_credentials=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/audio_rec', methods=['POST'])
def audio_rec():
    with open('/tmp/audio.wav', 'wb') as f:
        f.write(request.data)
    proc = run(['ffprobe', '-of', 'default=noprint_wrappers=1', '/tmp/audio.wav'], text=True, stderr=PIPE)
    return proc.stderr

@app.route('/audio_file', methods=['POST'])
def upload_file():
    #print('hello: '+ str(request.files))
    #uploaded_file = request.files['file']
    files = request.files.getlist('file')
    paths = []
    if len(files)!=0:
        for uploaded_file in files:
            if uploaded_file.filename != '':
                uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename))
            paths.append(os.path.join(app.config['UPLOAD_FOLDER'],uploaded_file.filename))
        return jsonify({'status': 1, 'message':'File uploaded successfully', 'path':paths})
    else:
        return jsonify({'status':'File not found'})


@app.route('/welcome', methods=['POST'])
def welcome():
    message = 'Hello Divya connect to flask!' 
    response = app.response_class(
        response=json.dumps(message),
        status=200,
        mimetype='application/json'
    )
    return jsonify({'message': message})

@app.route('/trigger', methods=['POST'])
def triggers():
    content = request.json
    # Eng_File,Ger_File = None
    for fil in content['File_path']:
        if 'Eng' in fil:
            Eng_File = fil
        elif 'Ger' in fil:
            Ger_File= fil
    split =  Ger_File.split('/')
    splitName = split[-1].split('.')[0]
    mod = model_class(silence_path=jd['filepath']['silence'],feature_path=jd['filepath']['feature'],plot_path=jd['filepath']['plot'])
    og_dat,pred_dat,og_wave,pred_wav,audio_path =  mod.predict_model(model_path= jd['MODEL'], og_path=Eng_File,file_feature=Ger_File,out_path=jd['filepath']['reult'])
    plot,plot_path = mod.save_plot(og_dat,pred_dat,og_wave,pred_wav,name=splitName)
    return jsonify({'plot_path': plot_path, 'Predicted_path':audio_path})

@app.route('/play_audio/<file_name>',methods=['POST','GET'])
def play_Audio(file_name):
   print(file_name)
   root_dir = os.path.dirname(os.getcwd())
   print(os.path.join(root_dir, 'static','js'))
   return send_from_directory( 
                    directory= app.config['BASE_URL'], path=file_name, as_attachment=False)

@app.route('/plot/<file_name>',methods=['POST','GET'])
def plot(file_name):
    return send_from_directory(
                    directory= app.config['IMAGE_URL'], path=file_name, as_attachment=False)

if __name__ == "__main__":
    # app.logger = logging.getLogger('audio-gui')
    app.run(debug=True, port=5000)