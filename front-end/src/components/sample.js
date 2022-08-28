import { useEffect, useState } from 'react';
import api from '../api/post'

function World(){
    const [getMessage, setGetMessage] = useState({})
    useEffect(()=>{
        const fetchPosts = async () => {
            const response = await api.post('/welcome').then(response => {
                console.log("SUCCESS", response)
                setGetMessage(response)
            }).catch(error => {
                console.log(error)
            })
        }
        fetchPosts();
    },[])
    return (
    <div className="App">
        <header className="App-header">
            <div>{getMessage.status === 200 ?
            <h3>{getMessage.data.message}</h3>
            :
            <h3>LOADING</h3>}</div>
        </header>
      </div>
    );
}

export default World;