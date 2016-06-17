import React from 'react';

class ElementStatus extends React.Component {

    render() {

        switch(this.props.status) {
            case 'enabled':
                return (
                    <div className="elementStatus">
                        <i className="fa fa-check"></i>&nbsp;Enabled
                    </div>
                );
                break;
        }

    }
}

export default ElementStatus;