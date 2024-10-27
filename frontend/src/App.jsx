import './App.css'
import AddItem from "./components/AddItem"
import Item from "./components/Item"
import { useState, useEffect, useContext } from "react"
import { MyContext } from './MyContext';

function App() {
  const { items, setItems } = useContext(MyContext);

  useEffect(() => {
    const fetchItems = async () => {
      try {
        const response = await fetch('https://3okx9781kk.execute-api.us-east-2.amazonaws.com/v1', {
          method: 'GET', // Specify the request method
          headers: {
            "Content-Type": "application/json", // Set the content type to JSON
          },
        });

        if (!response.ok) {
          throw new Error('Error: ' + response.statusText);
        }

        const responseData = await response.json(); // Parse JSON response
        setItems(responseData); // Handle the response data
      } catch (error) {
        alert(error); // Handle any errors
      }
    }
    fetchItems()
  }, [])

  return (
    <div className="app">
      <p>Currently supported platforms: RIDE, Burton, Smith, Halfdays</p>
      <AddItem></AddItem>
      {items && items.length > 0 && <div>{items.map((item) => {
        return <Item key={item.itemId} item={item}></Item>
      })}</div>}
    </div>
  )
}

export default App
