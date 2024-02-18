// import './App.css';

import MessageBox from "./components/MessageBox";
import Navbar from "./components/Navbar"
import FormComponent from "./components/FormComponent";
import React, { useEffect, useState } from "react";
import AppContext from "./AppContext";

function App() {
  const [isActive, setIsActive] = useState(false);
  // useEffect(() => {
  //   const handleBeforeUnload = () => {
  //     setIsActive(false);
  //   };
  //   window.addEventListener('beforeunload', handleBeforeUnload);
  //   return () => {
  //     window.removeEventListener('beforeunload', handleBeforeUnload);
  //   };
  // }, []);
  return (
    <AppContext.Provider value={{ isActive, setIsActive }}>
      <div className="App width-[100vw] height-[100vh] bg-gradient-to-b from-[#0e091e] to-[#232283]">
        <div className="">
          <Navbar />
          <FormComponent />
          <MessageBox />
        </div>
      </div>
    </AppContext.Provider>
  );
}

export default App;
