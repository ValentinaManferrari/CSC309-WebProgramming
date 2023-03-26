import React from 'react';
import {Link} from 'react-router-dom';
import { Grommet, Image, Header, Nav } from 'grommet';
import "./css/navbar.css";
import tfc_theme from '../constants/theme';
import UserNavBar from './AccountComponents/UserNavBar';



const items = [
  { label: 'Home', href: "/home" },
  { label: 'Membership', href: "/subscription_choices" },
  { label: 'Coach', href: "#" },
  { label: 'Class', href: "/classes" },
  { label: 'Studio', href: "/studios"},
  { label: 'About', href: "#" },
];

function NavbarComp(){
    return(
      <Grommet theme={tfc_theme}>
      <div className = "NavBar">
        <Header background="white" pad="small">

        {/* Logo */}
        <Image src="https://i.ibb.co/LtkKcGb/logo.png" alt="logo" border="0" className = "HeaderLogo"/>

        {/* Menu */}
        <Nav direction="row" className = "Menu">
            {items.map((item) => (
                /*<Anchor href={item.href} label={item.label}  key={item.label} color = "tfc-background-1" className = "Menu"/>*/
                <Link to={item.href}> {item.label} </Link>
            ))}
        </Nav>

        <UserNavBar/>

        </Header>
      </div>
      </Grommet>
    );
};

export default NavbarComp;