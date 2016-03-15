

var ResourceList = React.createClass({

    render: function () {
        var resourceNodes = this.props.data.map(function (resource) {
            return (
                <Resource resource={resource}></Resource>
            );
        });
        return (
            <table className="resourceList">
                {resourceNodes}
            </table>
        );
    }
});

var ResourceView = React.createClass({
    loadResources: function() {
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            cache: false,
            success: function(data) {
                this.setState({data: data.resources});
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },
    getInitialState: function() {
        return {data: []};
    },
    componentDidMount: function() {
        this.loadResources();
        // open websocket to get updates
        //setInterval(this.loadResources, this.props.pollInterval);
    },
    render: function() {
        return (
          <div className="resourceView">
            <ResourceList data={this.state.data} />
          </div>
        );
    }
});

React.render(
        <ResourceView url="http://localhost:8111/api/resources" />,
        document.getElementById('content')
);