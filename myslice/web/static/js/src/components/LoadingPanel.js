var React = require('react');
var classNames = require('classnames');

module.exports = React.createClass({

    render: function() {
        var loadingClass = classNames({
            'loading': true,
            'hidden': !this.props.show
        });
        return (
            <div className={loadingClass}>
                <img src="/static/images/loading.svg" alt="Loading..." />
            </div>
        );
    }
});