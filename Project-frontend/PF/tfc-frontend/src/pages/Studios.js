import React, { Component, useImperativeHandle } from "react";
import "./css/studios.css";
import tfc_theme from '../constants/theme';
import  { PageHeader,Box, Markdown, Button, Card, Grommet, InfiniteScroll, Image, Text, ThemeContext, Form, FormField, TextInput }from "grommet";
import { FormNext, Bookmark } from 'grommet-icons';
import API from '../api';
import StudioSearchResult from "../components/StudioSearchResult";

class Studios extends Component {
    constructor() {
        super();
        this.state = {
            input: "",
            results: []
        };
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(event) {
        event.preventDefault();
        this.getData(this.state.input);
    }

    getData = (input) => {
      console.log(input)
      var latitude = document.getElementById("latitude").value;
      var longitude = document.getElementById("longitude").value;
      var radius = document.getElementById("radius").value;
      var URL = "/studios/list_by_location/?latitude="+latitude+"&longitude="+longitude;
      API.get(URL)
          .then(res => {
              if (res.status === 200) {
                  this.setState({ results: [] })
                  console.log(res.data.length)
                  if (res.data.length > 0) {
                      let len = res.data.length;
                      let result_temp = [];
                      // result_temp.push(<Label></Label>)
                      for (let i = 0; i < len; i++) {
                          result_temp.push(<StudioSearchResult id={res.data[i].id} name={res.data[i].name} address={res.data[i].address} phone={res.data[i].phone}></StudioSearchResult>);
                      }
                      this.setState({ results: result_temp });
                  }
                  if (res.data.length === 0) {
                      alert("No Studios found");
                  }
              } else if (res.status === 400) {
                  alert("System Error. Please refresh");
              }
          })
    }

    render() {

        return (
          <Grommet theme={tfc_theme}>

          <Box direction="row" background = "white" gap = "300px" className = "PageHeader">
              <PageHeader title="Studios" subtitle="A subtitle for the page."/>
          </Box>
          
          <Box>
              <Form onSubmit={this.handleSubmit}>
                <FormField name="radius" htmlFor="radius" label="Radius">
                  <TextInput id="radius" name="radius" />
                </FormField>
                <FormField name="latitude" htmlFor="latitude" label="Latitude">
                  <TextInput id="latitude" name="latitude" />
                </FormField>
                <FormField name="longitude" htmlFor="longitude" label="Longitude">
                  <TextInput id="longitude" name="longitude" />
                </FormField>
                <Box direction="row" gap="medium">
                  <Button type="submit" primary label="Submit" />
                  <Button type="reset" label="Reset" />
                </Box>
              </Form>
          </Box>
          
          <Box className = "Result" pad = "large">
            {this.state.results}
          </Box>

          </Grommet>
        );
    }
}
export default Studios;