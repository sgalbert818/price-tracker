import { useContext } from "react"
import { MyContext } from '../MyContext';
import LineChart from "./LineChart"
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowUpRightFromSquare, faX } from '@fortawesome/free-solid-svg-icons';

export default function Item({ item }) {
    const { setItems } = useContext(MyContext);

    const handleDelete = async (id) => {
        const itemToDelete = {
            itemId: id
        }
        try {
            const response = await fetch('https://3okx9781kk.execute-api.us-east-2.amazonaws.com/v1', {
                method: 'DELETE', // Specify the request method
                headers: {
                    "Content-Type": "application/json", // Set the content type to JSON
                },
                body: JSON.stringify(itemToDelete), // Convert data to JSON string
            });

            if (!response.ok) {
                // Parse the error message from the response
                const errorData = await response.json();
                throw new Error(errorData.message);  // Throw an error with the message received from Lambda
            }
            const responseData = await response.json(); // Parse JSON response
            //console.log('Success:', responseData); // Handle the response data
        } catch (error) {
            alert(error); // Handle any errors
        }
        setItems((prev) => {
            return prev.filter((item => item.itemId !== id))
        })
    }

    return (
        <div className="item">
            <div className="h1">
                <img src={item.img}></img>
            </div>
            <div className="h2">
                <div className="item-desc">
                    <div className="item-desc-title">{item.name}</div>
                    <div className="item-desc-price">Current Price: ${item.price}</div>
                    <button id="link-btn"><a href={item.url} target="_blank"><FontAwesomeIcon icon={faArrowUpRightFromSquare} /></a></button>
                    <button id="del-btn" onClick={() => handleDelete(item.itemId)}><FontAwesomeIcon icon={faX} /></button>
                </div>
                <div className="chart-container">
                    <LineChart data={item.prices}></LineChart>
                </div>
            </div>
        </div>
    )
}