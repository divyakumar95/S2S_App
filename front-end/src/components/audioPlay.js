import AudioPlayer from 'react-h5-audio-player';
import ReactAudioPlayer from 'react-audio-player';
import 'react-h5-audio-player/lib/styles.css';
import React, { useState, useEffect } from 'react';
import api from '../api/post';
import config from '../config';

function PlayAudio({predPath}) {
	//const [play, setplay] = useState();
	const [getMessage, setGetMessage] = useState({})
	console.log('here in play audio', predPath)

	const file_name = async () => {
        const response = await api.get('/play_audio/'+predPath['Predicted_path']
		).then(response => {
            console.log("SUCCESS", response)
            setGetMessage(response)
        }).catch(error => {
            console.log(error)
        })
    }

return (
    <li>
		<h3>To get audio</h3>
		<a onClick={()=>{
			file_name();
		}}>
			Get audio
		</a>
		{ getMessage ?
			<ReactAudioPlayer
				autoPlay={true}
				// src = {'http://localhost:5000/play_audio/'+predPath['Predicted_path']}
				src={getMessage.data}
				// onPlay={e => console.log("onPlay")}
				controls={true}
				/> :null
		}
  	</li>
    );
};

export default PlayAudio;

