import React from 'react';

const Container = ({children}) =>
            <div className="view">
                <div className="container-fluid">
                    <div className="row">
                    {children}
                    </div>
                </div>
            </div>;

export default Container;