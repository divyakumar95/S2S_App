import api from '../api/post'
import ReactAudioPlayer from 'react-audio-player';
import { useState } from 'react';
import config from '../config';

export default function GenModel({ path }) {
  const [getMessage, setGetMessage] = useState({})
  var get_audio 
  var get_image 
  function Trigger_call() {
    console.log("here in display function ")  
    console.log(path)

    const fetchPosts=()=>{
      api.post('/trigger', {
        'File_path': path
      }).then(response => {
          console.log("SUCCESS", response)
          // setPredPath(response.data)
          setGetMessage(response)
      }).catch(error => {
          console.log(error)
      })}
      fetchPosts();
    }
    
    console.log('inside gernrate model',getMessage.data)
    if (getMessage.status ===200) {
      get_audio= config.baseURL+'/play_audio/'+ getMessage.data['Predicted_path']
      get_image= config.baseURL+'/plot/'+ getMessage.data['plot_path']+'.png'
    }
  
    return(
    <div>
      <li>
				<a onClick={()=>{ Trigger_call();}}
        href ="/#" > Trigger Model </a>
				<div> { getMessage.status === 200 ?
              <h3>Model Predicted successfully</h3>
              :null }
        </div>
		  </li>
      <li>
        { getMessage.status === 200 ? 
        <div>
          <h3>Play Audio</h3>
            <ReactAudioPlayer
                  autoPlay={true}
                  src={get_audio}
                  controls={true}
                  />
        </div>
        :null }      
        </li>
      <li>
        { getMessage.status === 200 ?
				<div>
          <h3>Plot data</h3>
          <img 
				    src = {get_image} 
				    alt=''/><br/>
          </div>
        :null }</li>
    </div>
  )
}
