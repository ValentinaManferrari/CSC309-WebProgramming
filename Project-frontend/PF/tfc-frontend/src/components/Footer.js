import React from 'react';
import { Grommet as GrommetIcon } from 'grommet-icons';
import styled from 'styled-components';
import { Grommet, Anchor, Box, Footer, Main, Text } from 'grommet';
import './css/footer.css';
import tfc_theme from '../constants/theme';

const footerContent = [
  ['For Trainees', 'Find a course', 'Find a studio', 'Find a coach','Membership'],
  ['For Trainers', 'Join Us', 'View Jobs', 'Coaches','Stories', 'FAQ'],
  ['About', 'Our Story', 'Contact Us', 'Help', 'FAQ'],
];

function FooterComp(){
return(

  <Grommet theme={tfc_theme}>
    <Box >

    <Footer background="light-2" pad={{ horizontal: 'large', vertical: 'small' }}>
      <Box direction="row" gap="small">
        <GrommetIcon color="tfc-text" />
        <Text alignSelf="center"> Toronto Fitness Club </Text>
      </Box>
      <Text textAlign="center" size="small">
        © 2022 Copyright
      </Text>
    </Footer>
  </Box>
   </Grommet>
);
}


export default FooterComp;