import React, { useEffect, useState } from "react";
import { Form, TextInputField, PasswordInputField, validators } from 'grommet-controls';
import { Link, useNavigate, Navigate } from 'react-router-dom';
import AuthService from "../../../services/auth-service";
import { Button, Box } from "grommet";
import { useContext } from "react";
import APIContext from "../../../Contexts/APIContext"


const EditProfileButton = () => {

  return (
    <>
      <Button secondary>
        <Link to="/edit_profile">Edit Profile</Link>
      </Button>
    </>
  )
}

export default EditProfileButton;