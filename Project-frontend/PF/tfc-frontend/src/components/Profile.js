import React from 'react';
import { Grommet, Box, Tab, Tabs, Button,Form, FormField, TextInput, Text } from 'grommet';
import "./css/profile.css";
import { User } from 'grommet-icons';
import tfc_theme from '../constants/theme';

function ProfileComp(){

    return(
        <Grommet theme = {tfc_theme}>
            <Text> View and Edit Profile info Here </Text>
        </Grommet>
    );
}

export default ProfileComp;