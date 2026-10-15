import { useState } from 'react'
import './App.css'

function App() {
  const [userChoice,setUserChoice]=useState('')
  return (
    <>
      <h1>Ai Email Agent</h1>    
      <div className='container'>
        <h2>Choose a profile</h2>
        <div style={{display:'flex',flexDirection:'row',gap:'5px'}}>
          <button>Personal</button>
          <button>College</button>
        </div>
        <button>Check Unread Emails</button>
      </div>   
    </>
  )
}

export default App
