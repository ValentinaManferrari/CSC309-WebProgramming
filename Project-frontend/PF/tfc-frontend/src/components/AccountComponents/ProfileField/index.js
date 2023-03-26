import React from "react";
import { Box} from "grommet";
import AuthService from "../../../services/auth-service";
import './style.css';

const ProfileField = (props) => {
  let user_data = AuthService.getCurrentUser()
  return (
    <Box className="ProfileEntry"> {props.label}: {user_data[props.field] == null ? "" : user_data[props.field]}</Box>
  )
}

export default ProfileField