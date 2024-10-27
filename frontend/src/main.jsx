import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import { MyProvider } from './MyContext.jsx'; // Adjust the import as needed

createRoot(document.getElementById('root')).render(
  //<StrictMode>
  <MyProvider>
    <App />
  </MyProvider>
  //</StrictMode>,
)
