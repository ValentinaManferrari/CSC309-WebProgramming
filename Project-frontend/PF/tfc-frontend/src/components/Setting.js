import React from 'react';
import { Grommet, Box} from 'grommet';
import "./css/setting.css";
import { Currency, HomeRounded, Notification, User, More, Flag } from 'grommet-icons';
import tfc_theme from '../constants/theme';
import {BillingComp} from "./Billing"
import {PaymentComp} from "/Payment."
import {CardComp} from "/Card.js"
import {
	BrowserRouter as Router,
    Route,
    Routes,
} from "react-router-dom";

function SettingComp(){

    return (
            <Box>
            <Router>
                <Routes>
                    {/* <Route path="/account" element={<AccountComp />} /> */}
                    <Route path="/my_subscription" element={<BillingComp />} />
                    <Route path="/payment" element={<PaymentComp />} />
                    <Route path="/card" element={<CardComp />} />
                </Routes>
            </Router>
        </Box>);
}

export default SettingComp;