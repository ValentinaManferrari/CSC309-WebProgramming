import React, { Component, useImperativeHandle } from "react";
import tfc_theme from '../constants/theme';
import  { PageHeader,Box, Markdown, Button, Card, Grommet, InfiniteScroll, Image, Text, ThemeContext, Form, FormField, TextInput }from "grommet";
import { FormNext, Bookmark } from 'grommet-icons';

class StudioSearchResult extends Component{

  constructor(props) {
    super(props);
    this.state = {
      id:  this.props.id,
      name: this.props.name,
      address: this.props.address,
      phone: this.props.phone,
    };
  }

  redirectStudio = () => {
    this.props.history.push(`/studios/list_by_location/${this.props.id}/`, {id: this.props.id})
  }
  
  render(){
    return (
        <Card width="1100px"  pad="medium"  gap="large" round="medium"  flex="grow">
        <Box direction="row" gap="large" justify="between" align="center">
        <Box direction="row" gap="medium">
            <Box width="xsmall" height="xsmall" background="orange!" round="small">
            <Image src= "https://i.ibb.co/2jNBdKP/Icon-3.png" />
            </Box>

            <Box>
            <Text size="large" color="text-strong" weight="bold" skeleton={{ width: 'small' }}>
            {this.state.name}
            </Text>
            <Text size="small">{this.state.address}</Text>
            <Text size="small">{this.state.phone}</Text>
            </Box>
        </Box>
        <Button label="View Details" reverse icon={<FormNext />} secondary onClick={this.redirectStudio}/>
        </Box>
        </Card>
    );
  }
}

export default StudioSearchResult;
