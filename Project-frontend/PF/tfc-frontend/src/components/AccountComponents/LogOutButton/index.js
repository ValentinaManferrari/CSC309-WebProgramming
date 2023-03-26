import React, { useEffect, useState } from "react";
import { Form, TextInputField, PasswordInputField, validators } from 'grommet-controls';
import { Link, useNavigate, Navigate } from 'react-router-dom';
import AuthService from "../../../services/auth-service";
import { Button, Box } from "grommet";
import { useContext } from "react";
import APIContext from "../../../Contexts/APIContext"


const LogOutButton = () => {
  let navigate = useNavigate();
  const {setLoggedIn} = useContext(APIContext)
  const logOut = () => {
    AuthService.logout();
    navigate("/login");
    setLoggedIn(false)
    console.log("Log out successful! ")
  };

  return (
    <>
      <Button secondary onClick={logOut}>Log Out</Button>
    </>
  )
}

export default LogOutButton;