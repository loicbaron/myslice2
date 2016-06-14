import React from 'react';

class Title extends React.Component {
  render() {
        return (
            <div className="p-title">
                <h1>{this.props.title}</h1>
                <h2>{this.props.subtitle}</h2>
            </div>
        );
  }
}

export default Title;