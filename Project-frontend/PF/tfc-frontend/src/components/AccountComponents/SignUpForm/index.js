import React, { useState } from "react";
import { Form, TextInputField, PasswordInputField, EmailInputField, validators } from 'grommet-controls';
import { Link, useNavigate, Navigate } from 'react-router-dom';
import AuthService from "../../../services/auth-service";
import { Button, Box, FileInput, FormField } from "grommet";
import './style.css';

const SignUpForm = () => {
  const [message, setMessage] = useState("");
  const [avatar, setAvatar] = useState();
  let navigate = useNavigate();

  const handleRegister = (e) => {
    setMessage("")
    e.avatar=avatar
    let formData = new FormData()
    for (var key in e){

      if(e[key])
        formData.append(key, e[key])
    }
    console.log(formData)

    AuthService.register(formData).then(
      (response) => {
        if (response && response.data && response.data.errors)
          setMessage(response.data.errors.join("\n"));
        else if(response && response.data && response.data.username) 
          navigate("/login");
      },
      (error) => {
        console.log("this?")
        const resMessage =
          (error.response &&
            error.response.data &&
            error.response.data.message) ||
          error.message ||
          error.toString();
        setMessage(resMessage);
      }
    );
  }

  return (
    <>
      {AuthService.isLoggedIn() && <Navigate to="/profile" />}
      <Form
        validate="blur"
        onSubmit={handleRegister}
        pad={{
          horizontal: 'small',
        }}
        className="SignUpForm"
        messages={{
          required: 'This is a required field.',
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
        <PasswordInputField
          label="Repeat Password"
          name="password2"
          validation={[
            validators.required(),
            validators.minLength(8)
          ]}
        />
        <EmailInputField
          label="Email"
          name="email"
          validation={[validators.email()]}
        />
        <TextInputField
          label="First Name"
          name="first_name"
        />
        <TextInputField
          label="Last Name"
          name="last_name"
        />
        <TextInputField
          label="Phone"
          name="phone"
        />

        <FormField
            htmlFor="avatar"
            name="avatar"
            label="Avatar"
          >
            <FileInput
              messages={{
                dropPrompt: 'Drag and drop'
              }}
              id="avatar"
              onChange={(event, { files }) => setAvatar(files[0])}
              name="avatar"
            />
          </FormField>



        <Box pad="small">
          <Button type="submit" label="Sign Up" />
        </Box>
        <Link to={"/login"}>Already have an account?</Link>
        
        {message !== "" && <Box className="ErrorMessage"> {message} </Box>}
      </Form>
    </>
  )
}

export default SignUpForm;