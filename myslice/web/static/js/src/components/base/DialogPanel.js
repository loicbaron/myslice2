import React from 'react';

const DialogPanel = ({children}) =>
     <div className="container">
        <div className="row">
            <div className="col-sm-8 col-sm-offset-2">
                <div className="d-panel">
                    {children}
                </div>
            </div>
        </div>
    </div>;

export default DialogPanel;