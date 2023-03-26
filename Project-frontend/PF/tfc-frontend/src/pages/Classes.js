import "./css/classes.css";
import React, { Component, useEffect, useState } from 'react';
import { PageHeader, Grommet,Anchor, Menu, List, InfiniteScroll, Box, Button, Card, Grid, Image, Text } from 'grommet';
import { FormNext, Flag, More, FormAdd} from 'grommet-icons';
import tfc_theme from '../constants/theme';
import FilterComp from "../components/Filter";

/*Class Data*/
const data = [];
for (let i = 0; i < 95; i += 1) {
  data.push({
    entry: `Class${i + 1}`,
  });
}

function Classes(){

  const [loading, setLoading] = useState(true);
  useEffect(() => {
    setTimeout(() => setLoading(!loading), 3000);
  }, [loading]);

  return (
      <Grommet theme = {tfc_theme}>

             <div  className = "PageHeader">
             <Box direction="row" background = "white"  gap = "300px">
                <PageHeader title="Classes" subtitle="A subtitle for the page."/>
                <FilterComp />
             </Box>
             </div>

             <div className="ClassList">
             <Box pad = "80px">
                <List data={data} action={(item, index) => (
                    <div className = "ClassComp">
                        <Box>
                            <Box>
                            <Anchor color = "black" icon={<FormAdd />} size = "large" hoverIndicator="brand"/>
                            </Box>
                            <Menu key={index} icon={<More/>} hoverIndicator="true" items={[{icon: <Flag />, label: 'Report' }]}/>
                        </Box>
                    </div>
                    )} step={4} show={{ page: 1 }} paginate />
             </Box>
             </div>
      </Grommet>
  );
};

export default Classes;
