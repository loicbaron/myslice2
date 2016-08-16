import React from 'react';

const SectionBody = ({children}) =>
    <div className="s-body">
        <div className="row">
            <div className="col-md-12">
                {children}
            </div>
        </div>
    </div>;

export default SectionBody;