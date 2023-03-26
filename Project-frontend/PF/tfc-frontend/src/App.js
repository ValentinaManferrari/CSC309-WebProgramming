import React, {Component} from 'react';
/*import Body from "./components/Body";*/
import NavComp from "./components/Navbar";
import FooterComp from "./components/Footer";
import tfc_theme from './constants/theme';
import {Grommet, Box} from 'grommet';
import {
	BrowserRouter as Router,
    Route,
    Routes,
} from "react-router-dom";

import Home from "./pages/Home";
import Studios from "./pages/Studios";
import Classes from "./pages/Classes";
import Settings from "./pages/Settings";
import Profile from "./pages/Profile";
import Login_SignUp from "./pages/Login_SignUp"
import Subscription_choices from "./pages/Subscription_choices"
import APIContext, {useAPIContext} from "./Contexts/APIContext";
import BillingComp from "./components/Billing";
import PaymentComp from "./components/Payment";
import CardComp from "./components/Card";
import ProfileComp from "./components/Profile";
import Not_Auth from "./pages/Not_Auth";
import General_Error from "./pages/General_Error";

import EditProfile from './components/AccountComponents/EditProfile';
import SignUpForm from "./components/AccountComponents/SignUpForm"
import Page404 from "./pages/Page404";
import './App.css';

const userSession = {
  user: {
    name: "Alan Souza",
    thumbnail: "//s.gravatar.com/avatar/b226da5c619b18b44eb95c30be393953?s=80"
  },
  items: [
    {
      label: "Logout",
      href: "#"
    }
  ]
};

function App(){
  return (
    <APIContext.Provider value={useAPIContext()}>
      
        <Router>
            <Grommet theme = {tfc_theme}>
            <div className = "App-header">
            <Box>
                <NavComp />
            </Box>
            </div>

            <div className='App-body'>
            <Box>
                <Routes>
                    <Route path="home" element={<Home/>} />
                    <Route index element={<Home/>} />
                    <Route path="studios" element={<Studios/>} />
                    <Route path="classes" element={<Classes/>} />
                    <Route path="profile" element={<Profile />} />
                    <Route path="settings"  element={<Settings />}>
                      <Route path ="account" element={<ProfileComp />}/>
                      <Route path ="my_subscription" element={<BillingComp />}/>
                      <Route path ="payment" element={<PaymentComp />}/>
                      <Route path ="card" element={<CardComp />}/>
                    </Route>
                    <Route path="profile" element={<Profile/>} />
                    <Route path="edit_profile" element={<EditProfile/>} />
                    <Route path="login" element={<Login_SignUp/>}/>
                    <Route path="signup" element={<SignUpForm/>}/>
                    <Route path='subscription_choices' element={<Subscription_choices/>}/>
                    <Route path='not_found' element = {<Page404/>}/>
                    <Route path='not_auth' element = {<Not_Auth/>}/>
                    <Route path='error' element = {<General_Error/>}/>
                </Routes>
            </Box>
            </div>

            <div className = "App-footer">
              <FooterComp />
            </div>
           </Grommet>
        </Router>
    </APIContext.Provider>
    );
}

export default App;
