import { useState, useContext } from 'react'
import { nanoid } from "nanoid"
import { MyContext } from '../MyContext';

export default function AddItem() {
    const { setItems, setLoading, items, loading } = useContext(MyContext)

    // helper functions

    const isValidUrl = (url) => {
        const regex = /^(ftp|http|https):\/\/[^ "]+$/;
        return regex.test(url);
    };

    // state

    const [formData, setFormData] = useState({
        url: ''
    })

    // on form change

    const handleChange = (event) => {
        const { name, value } = event.target
        setFormData((prev) => {
            return {
                ...prev,
                [name]: value,
            }
        })
    }

    // on form submit

    const handleSubmit = async (event) => {
        event.preventDefault()
        if (!formData.url) {
            alert('Ensure all required fields are filled')
        } else if (!isValidUrl(formData.url)) {
            alert('Please enter a valid URL')
        } else {
            setLoading(true)
            try {
                const response = await fetch('https://18.218.68.142:5000/scrape', {
                    method: 'POST', // Specify the request method
                    headers: {
                        "Content-Type": "application/json", // Set the content type to JSON
                    },
                    body: JSON.stringify({
                        url: formData.url
                    }), // Convert data to JSON string
                });

                if (!response.ok) {
                    // Parse the error message from the response
                    const errorData = await response.json();
                    throw new Error(errorData.error);  // Throw an error with the message received from Lambda
                }
                const responseData = await response.json(); // Parse JSON response
                //console.log(responseData)
                const newItem = {
                    ...formData,
                    itemId: nanoid(),
                    name: responseData.name,
                    price: responseData.price,
                    img: responseData.img,
                    prices: [[responseData.price, new Date().toISOString()]]
                }
                try { // since first api call was successful, now we push complete item to DB
                    const response = await fetch('https://3okx9781kk.execute-api.us-east-2.amazonaws.com/v1', {
                        method: 'POST', // Specify the request method
                        headers: {
                            "Content-Type": "application/json", // Set the content type to JSON
                        },
                        body: JSON.stringify(newItem), // Convert data to JSON string
                    });

                    if (!response.ok) {
                        // Parse the error message from the response
                        const errorData = await response.json();
                        throw new Error(errorData.message);  // Throw an error with the message received from Lambda
                    }
                    setItems((prev) => [newItem, ...prev])
                    setFormData({
                        url: ''
                    })
                } catch (error) {
                    alert(error); // Handle any errors
                }
            } catch (error) {
                alert(error); // Handle any errors
            }
            setLoading(false)
        }
    }

    return (
        <div>
            <form>
                <label htmlFor="url">URL</label>
                <input
                    type="text"
                    id="url"
                    name="url"
                    value={formData.url}
                    onChange={handleChange}
                />
                <br></br>
                <div className="submit">
                    <button onClick={handleSubmit}>Add Item</button>
                    {!items && <div>Searching for items...</div>}
                    {items && items.length === 0 && !loading && <div>Add an item to get started!</div>}
                    {loading && <div>Scanning URL...</div>}
                </div>
            </form>
        </div>
    )
}