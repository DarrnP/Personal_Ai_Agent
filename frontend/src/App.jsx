import { useState } from 'react'
import './App.css'

function App() {
  const [userChoice,setUserChoice]=useState('')
  return (
    <>
      <h1>Personal Ai Agent</h1>    
      <div className='container'>
        <input placeholder='select date'/>
        <div>
          
        </div>
      </div>   
    </>
  )
}

export default App
