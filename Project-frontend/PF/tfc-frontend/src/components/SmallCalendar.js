import React, { useState } from 'react';
import { Grommet, Box, Button, Calendar, Text } from 'grommet';
import { FormPreviousLink, FormNextLink } from 'grommet-icons';

function SmallCalendar(){
  const [date, setDate] = useState();

  const onSelect = (nextDate) => {
    setDate(nextDate !== date ? nextDate : undefined);
  };

  return (
    <Grommet >
    <Box align="center" pad="large">
      <Calendar
        date={date}
        onSelect={onSelect}
        size="small"
        bounds={['2020-09-08', '2025-12-13']}
        header={({
          date: currentDate,
          locale,
          onPreviousMonth,
          onNextMonth,
          previousInBound,
          nextInBound,
        }) => (
          <Box direction="row" align="center" justify="between">
            <Button disabled={!previousInBound} onClick={onPreviousMonth}>
              <Box>
                <FormPreviousLink />
              </Box>
            </Button>
           <Text size="small">
              <strong>
                {currentDate.toLocaleDateString(locale, {
                  month: 'long',
                  year: 'numeric',
                })}
              </strong>
            </Text>
            <Button disabled={!nextInBound} onClick={onNextMonth}>
              <Box>
                <FormNextLink />
              </Box>
            </Button>
          </Box>
        )}
      />
    </Box>
   </Grommet>
  );
};

export default  SmallCalendar;