import React, { Component } from "react";
import "./css/settings.css";
import {User, Yoga, Database, CreditCard, More } from 'grommet-icons';
import { Grommet, Box, Tabs, Tab} from 'grommet';
import { BrowserRouter as Router, Routes, Route, Link, Outlet } from 'react-router-dom'
import tfc_theme from '../constants/theme';

function Settings(){


    return(

    <Grommet theme={tfc_theme}>

        <Box>
            <div className = "Tab">
                <Box>
                    <Tabs>
                    <Tab title={ <Link to="/settings/account"> Account </Link> } icon={<User />}></Tab>
                    <Tab title={ <Link to="/settings/my_subscription"> Billing </Link> } icon={<Yoga />}> </Tab>
                    <Tab title={ <Link to="/settings/payment"> Payment History </Link> } icon={<Database />}> </Tab>
                    <Tab title={ <Link to="/settings/card"> Payment Info </Link> } icon={<CreditCard />}> </Tab>
                  </Tabs>
                </Box>
            </div>

            <Outlet/>
        </Box>

    </Grommet>
    );
}

export default Settings;
