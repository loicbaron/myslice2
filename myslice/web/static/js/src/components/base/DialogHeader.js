import React from 'react';

const DialogHeader = ({children}) => {

    var num = React.Children.count(children);
    if (num >= 2) {
        return (
            <div className="d-header">
                <div className="row">
                    <div className="col-sm-6">
                        {children[0]}
                    </div>
                    <div className="col-sm-6 d-header-right">
                        {children.slice(1)}
                    </div>
                </div>
            </div>
        );
    } else {
        return (
            <div className="d-header">
                <div className="row">
                    <div className="col-sm-12">
                        {children}
                    </div>
                </div>
            </div>
        );
    }
    
};

export default DialogHeader;