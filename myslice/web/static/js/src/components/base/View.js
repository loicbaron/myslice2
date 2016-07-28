import React from 'react';


const View = ({children}) => {

    var num = React.Children.count(children);

    if (num == 1) {

        return <div className="p-center">
                    {children}
                </div>;

    } else if (num == 2) {
        let leftPanel = children[0].type.name;

        if (leftPanel == 'Panel') {
            return <div className="row">
                    <div className="col-sm-6">
                        <div className="p-left">
                            {children[0]}
                        </div>
                    </div>
                    <div className="col-sm-6">
                         <div className="p-right">
                             {children[1]}
                         </div>
                    </div>
                </div>;
        } else if (leftPanel == 'PanelMenu') {
            return <div className="row">
                    <div className="col-sm-3">
                        <div className="p-menu">
                            {children[0]}
                        </div>
                    </div>
                    <div className="col-sm-6">
                        <div className="p-center">
                            {children[1]}
                        </div>
                    </div>
            </div>

        }
    } else {
        return (
                <div className="p-center">
                    not supported (too many children)
                </div>
        );
    }
    
};

export default View;