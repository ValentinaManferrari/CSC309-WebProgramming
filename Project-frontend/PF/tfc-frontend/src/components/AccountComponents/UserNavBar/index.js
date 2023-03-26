import React from "react";
import { Link } from 'react-router-dom';
import AuthService from "../../../services/auth-service";
import { Box, Avatar, Text } from "grommet";
import LogOutButton from "../LogOutButton";
import { useContext } from "react";
import APIContext from "../../../Contexts/APIContext";
import './style.css';

const UserNavBar = () => {
  const { loggedIn, username, avatar } = useContext(APIContext)
  return (
    <>
      {loggedIn ?
        <>
          <Box direction="row" align="right" gap="large" >

            <LogOutButton />
            <Link color="tfc-text" to="/profile">
              <Box direction="row" align="right" gap="small" label="user_information" className="User">
                <Text>
                  {username}
                </Text>
                <Avatar src={avatar == null ? "/images/no_avatar.jpg" : avatar} className="NavAvatar" />
              </Box>
            </Link>
          </Box>
        </>
        :
        <>
          <Box direction="row" align="right" gap="medium" className="UserLinks">
            <Link to="/login"> Log In </Link>
            <Link to="/signup"> Sign Up </Link>
          </Box>
        </>
      }
    </>
  )
}


export default UserNavBar;