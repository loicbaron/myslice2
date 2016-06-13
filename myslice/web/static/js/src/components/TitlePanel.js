import React from 'react';

export default class TitlePanel extends React.Component {
  render() {
        return (
                <div className="p-view-header">
                    <div className="container-fluid">
                        <div className="row">
                            <div className="col-sm-12">
                                <h1>{this.props.title}</h1>
                            </div>
                        </div>
                    </div>
                </div>
        );
  }
}