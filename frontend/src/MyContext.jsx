import React, { createContext, useState } from 'react';

const MyContext = createContext();

const MyProvider = ({ children }) => {
  const [items, setItems] = useState(null);
  const [loading, setLoading] = useState(false)

  return (
    <MyContext.Provider value={{ 
      items, setItems, loading, setLoading
    }}>
      {children}
    </MyContext.Provider>
  );
};

export { MyContext, MyProvider };
