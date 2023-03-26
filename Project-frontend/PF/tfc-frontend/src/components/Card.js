import React from 'react';
import { Grommet, Box, Tab, Tabs, Button,Form, FormField, TextInput, Text } from 'grommet';
import "./css/card.css";
import { Currency, HomeRounded, Notification, User } from 'grommet-icons';
import tfc_theme from '../constants/theme';

const data = [
];

function CardComp(){

        const [value, setValue] = React.useState({ name: 'a', email: 'b' });
        const message = value.name && value.email && value.name[0] !== value.email[0]  ? 'Mismatched first character': undefined;

    return(

        <Grommet theme = {tfc_theme}>

        /* No card added */

            <Box fill align="center" justify="center">
                <Box width="medium">
                    <Form value={value} onChange={(nextValue) => setValue(nextValue)}
                        onSubmit={({ value: nextValue }) => console.log(nextValue)} >
                         <FormField label="Card Number" name="card_num" required>
                            <TextInput aria-label="card_num" name="card_num"/>
                         </FormField>

                         <FormField label="Card Holder Name" name="card_holder_name" required>
                            <TextInput aria-label="card_holder_name" name="card_holder_name" type="name" />
                         </FormField>

                        <FormField label="CVC" name="cvc" required>
                            <TextInput aria-label="cvc" name="cvc" />
                        </FormField>

                        <FormField label="Expire Date" name="expire_date" required>
                            <TextInput aria-label="expire_date" name="expire_date" type="date" />
                        </FormField>

                        {message && (
                            <Box pad={{ horizontal: 'small' }}>
                                <Text color="status-error">{message}</Text>
                            </Box>
                        )}

                    <Box direction="row" justify="between" margin={{ top: 'medium' }}>
                        <Button onClick={() => setValue({ name: '', email: '' })} type="reset" label="Reset" />
                        <Button type="submit" label="Add/Update" primary />
                        <Button onClick={() => setValue({ name: '', email: '' })} label="Cancel" /> /* Keep Original Information*/
                    </Box>
                </Form>
            </Box>
        </Box>


        </Grommet>

        /* Already has a card added */
        /*
        <Box pad="small" gap="medium">
            <NameValueList layout="grid" pairProps={{ direction: 'column' }}>
                {Object.entries(data).map(([name, value]) => (
                <NameValuePair name={name}>
                <Text>{value}</Text>
            </NameValuePair>))}
            </NameValueList>
        </Box>

        <Box direction="row">
             <Button type="reset" label="Update" />
             <Button type="delete" label="Delete" />
        </Box>
        */

    );
}

export default CardComp;