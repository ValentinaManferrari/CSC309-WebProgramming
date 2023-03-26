import React, { useState } from 'react';
import { Grommet, Box, Button, Paragraph, Spinner } from 'grommet';
import { useNavigate } from 'react-router-dom';
import "./css/general_error.css";

const WEBSITE_BASE = "http://localhost:3000/";


function General_Error(){

    const navigate = useNavigate();

    return(
        <Grommet>
            <div className ="body">
            <Box align="center" pad="large">
                <Box align="center" gap="small">
                  <Paragraph textAlign="center">
                    An error happens! You may try the following things:...
                  </Paragraph>
                  <Button primary label="Back to Home Page"
                  onClick={() => navigate('/home')}/>
                </Box>
            </Box>
            </div>
        </Grommet>
        );
}

export default General_Error;