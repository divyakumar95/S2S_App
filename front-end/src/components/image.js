import React, { useState } from 'react';
import api from '../api/post';
import config from '../config';

function DispImage({predPath}) {
	const [getMessage, setGetMessage] = useState({})

	const image_file = () => {
		console.log('Inside Image before Api')
        api.get('/plot/'+predPath['plot_path']+'.png'
		).then(response => {
            console.log("SUCCESS", response)
            setGetMessage(response)
			// console.log('Get message',getMessage)
        }).catch(error => {
            console.log(error)
        })
		//console.log(getMessage)
    }
		return (
			<li>
				<a onClick={()=>{ image_file();}}> Get Image </a>
				<img 
				//src={url} 
				src = {getMessage.data} 
				alt=''/><br/>
			</li>
			)
};

export default DispImage;