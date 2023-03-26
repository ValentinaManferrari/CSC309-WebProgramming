import React, { useContext, Component } from "react";
import "./css/profile.css";
import UserProfile from '../components/AccountComponents/UserProfile'
import {Image, Grommet, Box, Grid} from "grommet";
import tfc_theme from '../constants/theme';

function Profile() {
  return (
    <div>
      <Grommet theme={tfc_theme}>

        <UserProfile />
      </Grommet>
    </div>
  );
}

export default Profile;