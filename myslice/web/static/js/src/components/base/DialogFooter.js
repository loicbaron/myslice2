import React from 'react';

const DialogFooter = ({children}) => {

    return (
        <div className="d-footer">
            <div className="row">
                <div className="col-sm-12">
                    {children}
                </div>
            </div>
        </div>
    );

};

export default DialogFooter;