import React, { useState } from 'react';
import { Grommet, Box, Button, Paragraph, Spinner } from 'grommet';
import { useNavigate } from 'react-router-dom';
import "./css/page404.css";

const WEBSITE_BASE = "http://localhost:3000/";


function Page404(){

    const navigate = useNavigate();

    return(
        <Grommet>
            <div className ="body">
            <Box align="center" pad="large">
                <Box align="center" gap="small">
                  <Paragraph textAlign="center">
                    Not Found 404.
                  </Paragraph>
                  <Button primary label="Back to Home Page"
                  onClick={() => navigate('/home')}/>
                </Box>
            </Box>
            </div>
        </Grommet>
        );
}

export default Page404;