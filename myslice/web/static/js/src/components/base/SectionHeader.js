import React from 'react';

const SectionHeader = ({children}) => {
    var num = React.Children.count(children);
    if (num >= 2) {
        return (
            <div className="s-header">
                <div className="row">
                    <div className="col-sm-6">
                        {children[0]}
                    </div>
                    <div className="col-sm-6 s-header-right">
                        {children.slice(1)}
                    </div>
                </div>
            </div>
        );
    } else {
        return (
            <div className="s-header">
                <div className="row">
                    <div className="col-sm-12">
                        {children}
                    </div>
                </div>
            </div>
        );
    }
};

export default SectionHeader;