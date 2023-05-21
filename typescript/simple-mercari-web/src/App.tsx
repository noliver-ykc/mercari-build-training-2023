import { useState } from 'react';
import './App.css';
import { ItemList } from './components/ItemList';
import { Listing } from './components/Listing';
import logo from './components/assets/logo.png';
import { ItemCallout } from './components/ItemList/ItemCallout';
function App() {
  // reload ItemList after Listing complete
  const [reload, setReload] = useState(true);
  return (
    <div className="page-spacing">
      <header className='Title'>
        <img className ="simple-logo" src={logo} alt="logo"/>
        <div>
          <Listing onListingCompleted={() => setReload(true)} />
        </div>
      </header>
      <ItemCallout reload={reload} onLoadCompleted={() => setReload(false)} />
      <div>
        <ItemList reload={reload} onLoadCompleted={() => setReload(false)} />
      </div>
    </div>
  )
}

export default App;
