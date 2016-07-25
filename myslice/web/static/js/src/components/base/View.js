import React from 'react';

import Container from './Container';

const View = ({children}) => {

    var num = React.Children.count(children);

    if (num == 1) {
        return (
            <Container>
                <div className="col-sm-12 panel p-center">
                    {children}
                </div>
            </Container>
        );
    } else if (num == 2) {
        let leftPanel = children[0].type.name;

        if (leftPanel == 'Panel') {
            return (
                <Container>
                    <div className="col-sm-6">
                        <div className="panel p-left">
                            {children[0]}
                        </div>
                    </div>
                    <div className="col-sm-6">
                         <div className="panel p-right">
                             {children[1]}
                         </div>
                    </div>
                </Container>
            );
        } else if (leftPanel == 'PanelMenu') {
            return (
                <Container>
                    <div className="col-sm-3 p-menu">
                        {children[0]}
                    </div>
                    <div className="col-sm-6 panel p-center">
                        {children[1]}
                    </div>
                </Container>
            );
        }
    } else {
        return (
            <Container>
                <div className="col-sm-12 panel p-center">
                    not supported (too many children)
                </div>
            </Container>
        );
    }
    
};

export default View;