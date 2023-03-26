import { createContext, useState } from "react";
import AuthService from "../services/auth-service";

export const useAPIContext = () => {
  const user_data = AuthService.getCurrentUser()
  const [loggedIn, setLoggedIn] = useState(AuthService.isLoggedIn());
  const [username, setUsername] = useState(user_data? user_data.username:"");
  const [avatar, setAvatar] = useState(user_data?user_data.avatar:"");
  return {
    loggedIn, setLoggedIn,
    username, setUsername,
    avatar, setAvatar
  }
}

const APIContext = createContext({
  loggedIn: null, setLoggedIn: () => { },
  username: null, setUsername: () => { },
  avatar: null, setAvatar: () => { },
})

export default APIContext;