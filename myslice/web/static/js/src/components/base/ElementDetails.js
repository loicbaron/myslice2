import React from 'react';

const ElementDetails = ({data}) => {
    var pairs = [];
    for(var k in data){
        if(k.indexOf('key') == -1 && k.indexOf('credential') == -1){
            pairs.push(<p><span className="elementLabel">{k}</span>: {data[k]}</p>);
        }
    }
    return(
        <div className="row">
            {pairs}
        </div>
    );
};

export default ElementDetails;
