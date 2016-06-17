import React from 'react';

class ElementLabel extends React.Component {

    render() {

        return (
            <h3 className="elementLabel">
                {this.props.label}
                &nbsp;
                <span>
                    {this.props.detail}
                </span>
            </h3>
        );

    }
}

export default ElementLabel;