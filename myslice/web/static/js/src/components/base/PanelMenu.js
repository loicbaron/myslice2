import React from 'react';

class PanelMenu extends React.Component {

    render() {
        return (
            <ul>
                {this.props.children}
            </ul>
        );
    }

}

export default PanelMenu;