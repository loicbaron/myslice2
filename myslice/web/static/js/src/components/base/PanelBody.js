import React from 'react';

const PanelBody = ({children}) =>
     <div className="p-body">
        <div className="container-fluid">
            <div className="row">
                <div className="col-md-12">
                    {children}
                </div>
            </div>
        </div>
    </div>;

export default PanelBody;