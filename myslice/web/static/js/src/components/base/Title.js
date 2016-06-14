import React from 'react';

export default class Title extends React.Component {
  render() {
        return (
            <div className="p-title">
                <h1>{this.props.title}</h1>
            </div>
        );
  }
}