var React = require('react');

module.exports = React.createClass({
  render: function() {
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
});