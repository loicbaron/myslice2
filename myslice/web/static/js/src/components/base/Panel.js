import React from 'react';

const Panel = ({children}) =>
    <div className="panel">
        {children}
    </div>;

const PanelBody = ({children}) =>
     <div className="p-body">
         {children}
     </div>;

const PanelHeader = ({children}) => {

    var num = React.Children.count(children);

    if (num >= 2) {
        return (
            <div className="p-header">
                <div className="row">
                    <div className="col-sm-8">
                        {children[0]}
                    </div>
                    <div className="col-sm-4 p-header-right">
                        {children.slice(1)}
                    </div>
                </div>
            </div>
        );
    } else {
        return (
            <div className="p-header">
                <div className="row">
                    <div className="col-sm-12">
                    {children}
                    </div>
                </div>
            </div>
        );
    }
};

export { Panel, PanelBody, PanelHeader };