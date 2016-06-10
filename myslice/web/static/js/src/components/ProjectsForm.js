var React = require('react');
var store = require('../stores/ProjectsFormStore');
var actions = require('../actions/ProjectsFormActions');
var LoadingPanel = require('./LoadingPanel');

module.exports = React.createClass({
    getInitialState () {
        return store.getState();
    },
    componentDidMount: function() {
        // store
        store.listen(this.onChange);
    },
    componentWillUnmount() {
        store.unlisten(this.onChange);
    },
    onChange(state) {
        this.setState(state);
    },

    handleLabelChange(e) {
        actions.updateLabel(e.target.value);
        actions.updateName(this.normaliseLabel(e.target.value));
    },
    normaliseLabel(text) {
        return text.replace(/[^a-z0-9]+/gi, '').replace(/^-*|-*$/g, '').toLowerCase();
    },
    handleUrlChange: function(e) {
       actions.updateUrl(e.target.value);
    },
    handleDescriptionChange: function(e) {
       actions.updateDescription(e.target.value);
    },
    handleStartDateChange: function(e) {
       actions.updateStartDate(e.target.value);
    },
    handleEndDateChange: function(e) {
       actions.updateEndDate(e.target.value);
    },
    onPublicChanged: function (e) {
        actions.updatePublic(e.currentTarget.checked);
        actions.updateProtected(!e.currentTarget.checked);
        actions.updatePrivate(!e.currentTarget.checked);
    },
    onProtectedChanged: function (e) {
        actions.updatePublic(!e.currentTarget.checked);
        actions.updateProtected(e.currentTarget.checked);
        actions.updatePrivate(!e.currentTarget.checked);
    },
    onPrivateChanged: function (e) {
        actions.updatePublic(!e.currentTarget.checked);
        actions.updateProtected(!e.currentTarget.checked);
        actions.updatePrivate(e.currentTarget.checked);
    },
    handleSubmit: function(e) {
        // prevent the browser's default action of submitting the form
        e.preventDefault();
        var label = this.state.label;
        var description = this.state.description;

        var flag = false;
        var msg = '';
        if(!label){
            msg += 'Name is required \n';
            flag = true;
        }
        if(!description){
            msg += 'Description is required \n';
            flag = true;
        }
        if(flag){
            alert(msg);
            return;
        }

        actions.submitForm();

    },
    render: function () {
        return (
            <div className="p-view-body">
                <div className="container-fluid">
                    <div className="row">
                        <div className="col-md-12">
                            <div id="project-form">
                                <form className="experimentForm" onSubmit={this.handleSubmit}>
                                <input type="text" placeholder="Name" value={this.state.label} onChange={this.handleLabelChange} />
                                <div>{this.state.name}</div>
                                <input type="radio" value={this.state.v_public} checked={this.state.v_public === true } onChange={this.onPublicChanged} /> Public
                                <input type="radio" value={this.state.v_protected} checked={this.state.v_protected === true } onChange={this.onProtectedChanged} /> Protected
                                <input type="radio" value={this.state.v_private} checked={this.state.v_private === true } onChange={this.onPrivateChanged} /> Private <br/>

                                <input type="text" placeholder="URL" value={this.state.url} onChange={this.handleUrlChange} /><br/>
                                <textarea name="description" placeholder="Describe your project in a few words..." value={this.state.description} onChange={this.handleDescriptionChange} /><br/>
                                Start: <input type="text" placeholder="yyyy-mm-dd hh:mm" value={this.state.start_date} onChange={this.handleStartDateChange} />
                                End: <input type="text" placeholder="yyyy-mm-dd hh:mm" value={this.state.end_date} onChange={this.handleEndDateChange} /><br/>
                                <br/>
                                <div><i><b>Important: </b>quote in your papers</i></div>
                                <div>Experiments leading to the publication of this paper have been performed using the OneLab Federation of testbeds.</div>
                                <input type="submit" value="Save"/>
                                </form>
                                <div className="">
                                    {this.state.message}
                                </div>
                                <LoadingPanel show={this.state.loading} />
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        );
    }
});