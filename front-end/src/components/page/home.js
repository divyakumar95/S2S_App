import React from 'react';
import { useState} from 'react';
import AudioUpload from '../file_upload'
import GenModel from '../display';

export const Home = () => {
  const [path, setPath] = useState();
  // const [predPath, setPredPath] = useState();
  return (
      <main className='wrapper'>
        <section className='hero'>
          <h1>
            GRU based Machine Translation
          </h1>
        </section>
      <section className='breweries' id="home">
        <ul>
          <AudioUpload setPath={setPath}/>
          <GenModel path={path}/>
        </ul>
      </section>
      </main>
  );
}

export default Home;