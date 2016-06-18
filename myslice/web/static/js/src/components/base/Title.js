import React from 'react';

class Title extends React.Component {
  render() {

      return (
          <div>
              <h1>{this.props.title} <span>{this.props.subtitle}</span></h1>
          </div>
      );
  }
}

export default Title;