import React from "react";
import { Navigate } from 'react-router-dom';
import { Box, Grid, Image } from "grommet";
import AuthService from "../../../services/auth-service";
import './style.css';
import ProfileField from "../ProfileField";
import EditProfileButton from "../EditProfileButton";


const UserProfile = () => {
  let user_data = AuthService.getCurrentUser()
  return (
    <>
      {!(AuthService.isLoggedIn()) ? <Navigate to="/login" /> :
        <Grid
          rows={['medium', 'medium']}
          columns={['medium', 'small']}
          gap="small"
          areas={[
            { name: 'profile_data', start: [0, 0], end: [0, 1] },
            { name: 'avatar', start: [1, 0], end: [1, 1] },
          ]}
          className="ProfileBox"
        >
          <Box gridArea="profile_data" background="light-5" className="FieldBox">
            <ProfileField label="Username" field="username"/>
            <ProfileField label="First name" field="first_name"/>
            <ProfileField label="Last name" field="last_name"/>
            <ProfileField label="Email" field="email"/>
            <ProfileField label="Phone" field="phone"/>
          </Box>
          <Box gridArea="avatar" background="light-5" className="AvatarBox">
            <Image src={user_data.avatar == null ? "/images/no_avatar.jpg" : user_data.avatar} />
          </Box>
            <EditProfileButton/>
        </Grid>}
    </>
  )
}

export default UserProfile;