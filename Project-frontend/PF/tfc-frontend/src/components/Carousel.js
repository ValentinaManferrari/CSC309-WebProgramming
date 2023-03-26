import React from 'react';
import { Grommet, Box, Button, Carousel, Text } from 'grommet';
import "./css/carousel.css";
import tfc_theme from "../constants/theme";

function CarouselComp(){

  return(
   <Grommet theme= {tfc_theme}>
      <Box align="center" pad="large">
        <Carousel controls="arrows" className = "HomeImageSet" >
          <Box
            fill = "vertical"
            align="center"
            justify="center"
            gap="small"
            className = "slide-1"
          >
            <Box className = "HomeText">
                <Text weight="bold" size="6xl" className = "slogan-1" color = "tfc-background-3" >
                    <div> Decide. </div>
                    <div> Commit. </div>
                    <div> Succeed. </div>
                </Text>
            </Box>
            <Button primary align = "center" size="large" label="Join Us!" color = "tfc-background-3" background = "tfc-background-3" className = "button"/>
            <Box
                align = "bottom"
                backgroundImg= "tfc-background-3"
                gap="large">
            </Box>
          </Box>

          <Box
            fill = "vertical"
            align="center"
            justify="center"
            background="light-3"
            gap="small"
          >
            <Box className = "HomeImage"  align = "center">
                <Text weight="bold" size="xlarge">
                    Slide 2
                </Text>
            </Box>
            <Button label="Button" align = "bottom" color = "tfc-text"/>
            <Button label="Button" align = "bottom" color = "tfc-text"/>
            <Box
                align = "bottom"
                backgroundImage = "tfc-background-3"
                gap="large">
            </Box>
          </Box>

          <Box
            fill
            align="center"
            justify="center"
            background="light-5"
            gap="small"
          >
            <Box className = "HomeImage"  align = "center" >
                <Text weight="bold" size="xlarge">
                    Slide 3
                </Text>
            </Box>
            <Button label="Button" align = "bottom" color = "tfc-text"/>
            <Button label="Button" align = "bottom" color = "tfc-text"/>
            <Button label="Button" align = "bottom" color = "tfc-text"/>
            <Box
                align = "bottom"
                background= "light-4"
                gap="large">
            </Box>
          </Box>
        </Carousel>
      </Box>
       </Grommet>
    );
}

export default CarouselComp;