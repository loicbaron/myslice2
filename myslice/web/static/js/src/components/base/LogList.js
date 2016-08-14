import React from 'react';

import LogRow from './LogRow';

const LogList = ({log}) => 

    <ul className="logList">
    {
        log.sort((x,y) => 
                new Date(y.timestamp).getTime() - new Date(x.timestamp).getTime()
            ).map((l, index) => 
                <LogRow key={index} log={l} />
            )
     }
    </ul>;


export default LogList;