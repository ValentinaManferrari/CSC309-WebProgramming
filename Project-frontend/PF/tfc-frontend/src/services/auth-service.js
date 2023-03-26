import axios from "axios";
// Inspiration: https://www.bezkoder.com/react-hooks-jwt-auth/
const BACKEND_DOMAIN = "http://localhost:8000/"
const API_URL = BACKEND_DOMAIN + "accounts/"

const register = (props) => {
  return axios.post(API_URL + "signup/", props , {headers:{ 'Content-Type': 'multipart/form-data'}})
}

const login = (username, password) => {
  return axios
  .post(API_URL + "login/", {username, password})
  .then((response)=>{
      if (response.data.access){
        localStorage.setItem("accessToken", response.data.access);
        localStorage.setItem("refreshToken", response.data.refresh);
        localStorage.setItem("user", JSON.stringify(response.data.user));
      }
      return {success:true, message:response.data};
    }).catch((response)=>{
    return {success:false, message: response.response.data.detail};
  })
}

const logout = () => {
  localStorage.removeItem("accessToken");
  localStorage.removeItem("refreshToken");
  localStorage.removeItem("user");
}

const isLoggedIn = () => {
  var res = localStorage.getItem("user") != null;
  return res;
}


const getCurrentUser = () => {
  return JSON.parse(localStorage.getItem("user"))
}

const authHeader = () => {
  const token = localStorage.getItem('accessToken');
  console.log(token)

  if (token) {
    return 'Bearer ' + token;
  } else {
    return "";
  }
}

const AuthService = {
  register,
  login,
  logout,
  getCurrentUser,
  authHeader,
  isLoggedIn
};

export default AuthService;