import React from 'react';

import actions from '../../actions/NavBarActions';

class SlicesMenuButton extends React.Component {

    showMenu() {
        console.log('pressed')
        actions.showMenu(true);
    }

    render() {
        return <div onMouseEnter={this.showMenu}>aaaa</div>;
    }
}

export default SlicesMenuButton;