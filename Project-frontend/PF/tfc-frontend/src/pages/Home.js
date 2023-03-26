import React, { Component } from "react";
// import home from './img/home-background.jpg';
import "./css/home.css";
import NavbarComp from "../components/Navbar.js";
import FooterComp from "../components/Footer.js";
import CarouselComp from "../components/Carousel.js";
import tfc_theme from '../constants/theme';
import {Footer, Box, Text, Anchor, Grommet} from "grommet";
import styled from 'styled-components';


const footerContent = [
  ['For Trainees', 'Find a course', 'Find a studio', 'Find a coach','Membership'],
  ['For Trainers', 'Join Us', 'View Jobs', 'Coaches','Stories', 'FAQ'],
  ['About', 'Our Story', 'Contact Us', 'Help', 'FAQ'],
];

const StyledAnchor = styled(Anchor)`
  font-weight: 200;
`;

const FooterAnchor = ({ ...rest }) => (
  <StyledAnchor href="/" size="small" color="black" {...rest} />
);

const FooterContent = () =>
  footerContent.map((item) => (

      <Box gap="medium" key={item[0]}>
          <Text weight="bold" size="medium" className = "ColumnTitle">
            {item[0]}
          </Text>

          <Box>
            {[1, 2, 3,4].map((i) => (
              <FooterAnchor key={item[i]}>{item[i]}</FooterAnchor>
            ))}
          </Box>

          <Box gap="medium">
          </Box>
      </Box>
  ));


function Home(){
    return(
       <Grommet theme={tfc_theme}>
       <div className = "Carousel">
        <CarouselComp />
       </div>
       <div className = "Footer">
           <Footer background="white" pad="large">
                <FooterContent />
           </Footer>
       </div>
       </Grommet>
        );
    }

export default Home;