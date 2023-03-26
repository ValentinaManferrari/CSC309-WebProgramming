import React, { useCallback, useState } from 'react';
import { Grommet, Box, Button, Form, FormField, Select } from 'grommet';
import "./css/filter.css";
import tfc_theme from '../constants/theme';

const options = [
  { label: 'Proximity', value: 1 },
  { label: 'option 2', value: 2 },
  { label: 'option 3', value: 3 },
];

function FilterComp(){
  const [value, setValue] = useState({});
  const onChange = useCallback((nextValue) => setValue(nextValue), []);

  return (
      <Grommet theme={tfc_theme}>
        <Box direction="row" align="center" pad="large">
          <Form onSubmit={() => console.log('Submit', value)} >
           <Box direction="row" gap="medium" align="center">
            <FormField label="Sory By" name="sort">
              <Select
                name="select"
                placeholder="Select a filter criterion"
               options={options}
                labelKey="label"
                valueKey="value"
              />
            </FormField>
            <Box direction="row" gap="small">
            <Button type="submit" label="Filter"  pad = "large" primary className="filterbutton" />
            <Button type="submit" label="Clear"  pad = "large" className="filterbutton" />
            </Box>
            </Box>
          </Form>
        </Box>
      </Grommet>
  );
};

export default FilterComp;