import React from 'react';
import { Grommet, Box, Tab, Tabs, NameValueList, NameValuePair, Text } from 'grommet';
import "./css/billing.css";
import { Currency, HomeRounded, Notification, User } from 'grommet-icons';
import tfc_theme from '../constants/theme';


function BillingComp(props){

    return(
        <Grommet theme = {tfc_theme}>
            <Text> Put Billing Information Here </Text>
        </Grommet>
    );
}

export default BillingComp;