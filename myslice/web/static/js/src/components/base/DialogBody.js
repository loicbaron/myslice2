import React from 'react';

class DialogBody extends React.Component {
    render() {
        return (
            <div className="d-body">
                { this.props.children }
            </div>
        );
    }
}

export default DialogBody;