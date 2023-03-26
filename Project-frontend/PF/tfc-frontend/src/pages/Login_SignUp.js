import React, { Component } from "react";
import "./css/login_signup.css";
import NavbarComp from "../components/Navbar";
import FooterComp from "../components/Footer";
import LogInForm from "../components/AccountComponents/LogInForm";
import tfc_theme from '../constants/theme';
import { Image, Grommet, Box, Grid } from "grommet";


function Login_SignUp() {
  return (
    <div>
      <Grommet theme={tfc_theme}>

        <Box direction="row" className="LogInBlock">
          <Box className="panel" a>
            <LogInForm />
          </Box>
          <Box className="pic" >
            <Image src="https://i.ibb.co/VwJkLB2/Image.png" />
          </Box>
        </Box>
      </Grommet>
    </div>


    //                <Grid fill = "true"
    //                    areas={[
    //                      { name: 'pic', start: [0, 0], end: [0, 0] },
    //                      { name: 'panel', start: [1, 0], end: [1, 0] },
    //                    ]}
    //                    columns={['small', 'flex']}
    //                    rows={['flex']}
    //                    gap="medium" >
    //                        <Box gridArea="pic">
    //                               <div className="pic" >
    //                               <Image src= "https://i.ibb.co/VwJkLB2/Image.png"  alignSelf = "center"/>
    //                               </div>
    //                        </Box>
    //
    //                        <Box gridArea="panel" className = "panel">
    //                            <Box>
    //                            </Box>
    //                            <LoginComp  className = "Panel"/>
    //                        </Box>
    //                </Grid>
  );
}

export default Login_SignUp;



