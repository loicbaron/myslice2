import React from 'react';

import Container from './Container';

class View extends React.Component {

    render() {
        var num = React.Children.count(this.props.children);
        if (num == 1) {
            return (
                <Container>
                    <div className="col-sm-12 p-center">
                        {this.props.children}
                    </div>
                </Container>
            );
        } else if (num == 2) {
            let leftPanel = this.props.children[0].type.name;

            if (leftPanel == 'Panel') {
                return (
                    <Container>
                        <div className="col-sm-6 p-left">
                            {this.props.children[0]}
                        </div>
                        <div className="col-sm-6 p-right">
                            {this.props.children[1]}
                        </div>
                    </Container>
                );
            } else if (leftPanel == 'PanelMenu') {
                return (
                    <Container>
                        <div className="col-sm-3 p-menu">
                            {this.props.children[0]}
                        </div>
                        <div className="col-sm-6 p-center">
                            {this.props.children[1]}
                        </div>
                    </Container>
                );
            }
        } else {
            return (
                <Container>
                    <div className="col-sm-12 p-center">
                        not supported (too many children)
                    </div>
                </Container>
            );
        }

    }
    
}

export default View;