import React, { Component } from "react";
import "./css/subscriptions.css";
import NavbarComp from "../components/Navbar.js";
import FooterComp from "../components/Footer.js";
import SettingComp from "../components/Setting.js";
import tfc_theme from '../constants/theme';
import {Grommet} from "grommet";

function Subscriptions(){

    return(
            <div>
               <Grommet theme={tfc_theme}>
                     <SettingComp />
               </Grommet>
            </div>
    );
}


export default Subscriptions;