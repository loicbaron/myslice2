import React from 'react';

class ElementTitle extends React.Component {

    render() {

        return (
            <h3 className="elementTitle">
                {this.props.label}
                &nbsp;
                <span>{this.props.detail}</span>
            </h3>
        );

    }
}

export default ElementTitle;