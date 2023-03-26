import React, { useState } from 'react';
import { Grommet, Box, Button, Paragraph, Spinner } from 'grommet';
import { useNavigate } from 'react-router-dom';
import "./css/page404.css";

const WEBSITE_BASE = "http://localhost:3000/";


function Not_Auth(){

    const navigate = useNavigate();

    return(
        <Grommet>
            <div className ="body">
            <Box align="center" pad="large">
                <Box align="center" gap="small">
                  <Paragraph textAlign="center">
                    You need to log in to access this page.
                  </Paragraph>
                  <Button primary label="Log in"
                  onClick={() => navigate('/login')}/>
                </Box>
            </Box>
            </div>
        </Grommet>
        );
}

export default Not_Auth;