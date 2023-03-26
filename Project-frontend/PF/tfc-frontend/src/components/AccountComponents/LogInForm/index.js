import React, {useState } from "react";
import { Form, TextInputField, PasswordInputField, validators } from 'grommet-controls';
import { Link, useNavigate, Navigate } from 'react-router-dom';
import AuthService from "../../../services/auth-service";
import { Button, Box } from "grommet";
import {useContext} from "react";
import APIContext from "../../../Contexts/APIContext";
import './style.css';

const LogInForm = () => {
  const [message, setMessage] = useState("");
  const {setLoggedIn, setUsername, setAvatar} = useContext(APIContext)
  let navigate = useNavigate();

  const handleLogin = (e) => {
    setMessage("");

    AuthService.login(e.username, e.password).then(
      (data) => {
        if(data.success){
          let user_data = AuthService.getCurrentUser()
          navigate("/profile");
          setLoggedIn(true)  
          setUsername(user_data.username)
          setAvatar(user_data.avatar)
          console.log("Log in successful! ")
        }
        else {
          setMessage(data.message);
        }
      },
      (error) => {
        const resMessage =
          (error.response &&
            error.response.data &&
            error.response.data.message) ||
          error.message ||
          error.toString();
        console.log("best place")
        console.log(error)
        setMessage(resMessage);
      }
    );
  }
  return (
    <>
      {AuthService.isLoggedIn() && <Navigate to="/profile"/>}
      <Form
        onSubmit={handleLogin}
        pad={{
          horizontal: 'small',
        }}
      >
        <TextInputField
          label="Username"
          name="username"
          validation={[validators.required()]}
        />
        <PasswordInputField
          label="Password"
          name="password"
          validation={[
            validators.required(),
            // validators.minLength(8)
          ]}
        />
        <Box pad="small">
          <Button type="submit" label="Log In" />
        </Box>
        <Link to={"/signup"} className="signUpLink">Don't have an account?</Link>

        {message !== "" && <Box className="ErrorMessage"> {message} </Box>}
      </Form>
    </>
  )
}

export default LogInForm;