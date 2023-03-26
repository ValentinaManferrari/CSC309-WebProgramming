import React, { Component } from "react";
import "bootstrap/dist/css/bootstrap.css";
import {
	BrowserRouter as Router,
    Route,
    Routes,
} from "react-router-dom";
import Home from "../pages/Home";
import Studios from "../pages/Studios";
import Classes from "../pages/Classes";
import Settings from "../pages/Settings";
import Profile from "../pages/Profile";
import Login_SignUp from "../pages/Login_SignUp"
import Subscription_choices from "../pages/Subscription_choices"

function Body(){
    return(
        <Router>
            <Routes>
                <Route path="/home" element={<Home/>} />
                <Route path="/studios" element={<Studios/>} />
                <Route path="/classes" element={<Classes/>} />
                <Route path="/settings" element={<Settings/>} />
                <Route path="/profile" element={<Profile/>} />
                <Route path="/login" element={<Login_SignUp/>}/>
                <Route path='/subscription_choices' element={<Subscription_choices/>}/>
            </Routes>
        </Router>
    );
}

export default Body;
