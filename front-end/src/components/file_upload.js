import '../App.css';
import React, { useState} from 'react';
import api from '../api/post'


function AudioUpload({setPath}) {

    const [file, setFile] = useState()
    const [getMessage, setGetMessage] = useState({})

    function handleChange(event) {
      setFile(event.target.files)
    }
    
    function handleSubmit(event) {
      event.preventDefault()
      // const url = 'http://localhost:5000/audio_file';
      
      const formData = new FormData();
      // formData.append('file', file);
      // formData.append('fileName', file.name);
      
      for (let i = 0 ; i < file.length ; i++) {
        formData.append("file", file[i]);
      }
      
      const config = {
        headers: {
          'content-type': 'multipart/form-data',
        },
      };
      api.post('/audio_file', formData, config).then((response) => {
        console.log('From inside API :',response.data.path);
        setPath(response.data.path)
        setGetMessage(response)
      });
    }

    return (
      <div className="App">
          <form onSubmit={handleSubmit} >
            <h1>React File Upload</h1>
            <input type="file" onChange={handleChange} multiple 
            accept='wav'/>
            <button type="submit"> Upload </button>
            <div>{ getMessage.status === 200 ?
            <h3>File uploaded successfully</h3>
            : null }</div>
          </form>
      </div>
    );
  }

export default AudioUpload;

// dataPaths = localStorage.getItem('list_path');