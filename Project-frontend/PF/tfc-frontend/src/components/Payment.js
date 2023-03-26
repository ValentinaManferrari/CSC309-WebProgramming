import React from 'react';
import { Grommet, Box, Tab, Tabs, List, Menu} from 'grommet';
import "./css/payment.css";
import { Currency, HomeRounded, Notification, User, More, Flag } from 'grommet-icons';
import tfc_theme from '../constants/theme';

/*Payment Data*/
const data = [];

function PaymentComp(){
    return(

    <Grommet theme={tfc_theme}>

        <div className="PaymentList">
             <Box pad = "80px">
                <List data={data} action={(item, index) => (
                    <div className = "Payment">
                        <Box>
                            <Menu key={index} icon={<More/>} hoverIndicator="true" items={[{icon: <Flag />, label: 'Report' }]}/>
                        </Box>
                    </div>
                    )} step={4} show={{ page: 1 }} paginate />
             </Box>
        </div>
    </Grommet>
    );
}

export default PaymentComp;