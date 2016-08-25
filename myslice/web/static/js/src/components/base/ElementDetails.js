import React from 'react';

const ElementDetails = ({data}) => {
    var pairs = [];
    for(var k in data){
        var val = null;
        if(k.indexOf('key') == -1 && k.indexOf('credential') == -1 && k.indexOf('type')==-1){
            if(Array.isArray(data[k])){
                if(typeof(data[k][0])==='string'){
                    var val = data[k].join(', ');
                }
            }
            if(typeof(data[k])==='string'){
                var val = data[k];
            }
            if(val!=null){
                pairs.push(<p key={k}><span className="elementLabel">{k}</span>: {val}</p>);
            }
        }
    }
    var padding = {"paddingTop":"10px"};
    return(
        <div className="row" style={padding}>
            <div className="col-sm-12">
            {pairs}
            </div>
        </div>
    );
};

export default ElementDetails;
