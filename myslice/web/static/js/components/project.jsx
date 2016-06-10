var Title = React.createClass({
  render: function() {
    return (
            <div className="p-view-header">
                <div className="container-fluid">
                    <div className="row">
                        <div className="col-sm-12" id="title-right">
                            <h1>New Project</h1>
                        </div>
                    </div>
                </div>
            </div>
    );
  }
});
var ProjectAdd = React.createClass({
    getInitialState: function() {
        return projectstore.getState();
    },

    componentDidMount: function() {
        

    // listen on state changes
    projectstore.listen(this.onChange);
    },

    componentWillUnmount() {
        projectstore.unlisten(this.onChange);
    },

    onChange(state) {
        this.setState(state);
    },
    handleClick(){
        if(this.state.selected!=null){
            projectactions.selectProject(this.state.selected);
        }
    },
    render: function() {
        return (
            <button className="elementAdd" onClick={this.handleClick}><img className="icon" src="/static/icons/plus.png" alt="+" /> Add Project</button>
        );
    }
});
var ProjectForm = React.createClass({
    getInitialState () {
        return projectformstore.getState();
    },
    componentDidMount: function() {
        // store
        projectformstore.listen(this.onChange);
    },
    componentWillUnmount() {
        projectformstore.unlisten(this.onChange);
    },
    onChange(state) {
        this.setState(state);
    },

    handleLabelChange(e) {
        projectformactions.updateLabel(e.target.value);
        projectformactions.updateName(this.normaliseLabel(e.target.value));
    },
    normaliseLabel(text) {
        return text.replace(/[^a-z0-9]+/gi, '').replace(/^-*|-*$/g, '').toLowerCase();
    },
    handleUrlChange: function(e) {
       projectformactions.updateUrl(e.target.value);
    },
    handleDescriptionChange: function(e) {
       projectformactions.updateDescription(e.target.value);
    },
    handleStartDateChange: function(e) {
       projectformactions.updateStartDate(e.target.value);
    },
    handleEndDateChange: function(e) {
       projectformactions.updateEndDate(e.target.value);
    },
    onPublicChanged: function (e) {
        projectformactions.updatePublic(e.currentTarget.checked);
        projectformactions.updateProtected(!e.currentTarget.checked);
        projectformactions.updatePrivate(!e.currentTarget.checked);
    },
    onProtectedChanged: function (e) {
        projectformactions.updatePublic(!e.currentTarget.checked);
        projectformactions.updateProtected(e.currentTarget.checked);
        projectformactions.updatePrivate(!e.currentTarget.checked);
    },
    onPrivateChanged: function (e) {
        projectformactions.updatePublic(!e.currentTarget.checked);
        projectformactions.updateProtected(!e.currentTarget.checked);
        projectformactions.updatePrivate(e.currentTarget.checked);
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

        projectformactions.postForm();

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
            </div>
                        </div>
                    </div>
                </div>
            </div>

        );
    }
});

var ProjectLabel = React.createClass({

    label: function() {
        let label = '';
        switch(this.props.project.action) {
            case 'REQ':
                label = 'requested ' + this.props.project.object.type;
        }
        return label;
    },

    render: function () {
        return (

            <div className="row">
                <div className="col-md-12">
                    <div className="elementIcon">
                <img src="/static/icons/projects-w-24.png" alt="" />
            </div>
                    <div className="elementLabel">{ this.label() }</div>
                </div>
            </div>
        )
    }
});
var ProjectStatus = React.createClass({
    render: function () {
        return (
            <div className="row">
                <div className="col-md-12">
                    <div className="elementStatus">{ this.props.status }</div>
                </div>
            </div>
        )
    }
});

var ProjectRow = React.createClass({
     /*
     getInitialState () {
        return {
        'selected':false
        };
     },
     */
     handleClick(){
        projectactions.selectProject(this.props.project);
        /*
        if(this.state.selected){
            this.setState({'selected':false});
        }else{
            this.setState({'selected':true});
        }
        */
     },
     render: function() {
         if(this.props.selected == this.props.project.id){
            var liClass = 'elementBox selected';
         }else{
            var liClass = 'elementBox';
         }
         return (
             <li className={liClass} onClick={this.handleClick}>
                 <ProjectLabel project={this.props.project} />
                 <div className="row">
                     <div className="col-md-6">
                         <div className="elementId">
                             {this.props.project.id}
                         </div>
                         <div className="elementDate">
                            Created: { moment(this.props.project.created).format("DD/MM/YYYY H:mm") }
                            <br />
                            Updated: { moment(this.props.project.updated).format("DD/MM/YYYY H:mm") }
                         </div>
                     </div>
                     <div className="col-md-6">

                     </div>
                 </div>
                 <ProjectStatus status={this.props.project.status} />
             </li>
         );
     }
 });

var ProjectList = React.createClass({

    getInitialState: function() {
        return projectstore.getState();
    },

    componentDidMount: function() {
        

    // listen on state changes
    projectstore.listen(this.onChange);
    },

    componentWillUnmount() {
        projectstore.unlisten(this.onChange);
    },

    onChange(state) {
        this.setState(state);
    },

    render: function() {
        var selected = this.state.selected;
        var project = this.state.project;
        if (this.state.errorMessage) {
            return (
                <div>Something is wrong</div>
            );
        }

        return (
            <ul className="elementList">
            {project.map(function(project) { return <ProjectRow key={project.id} project={project} selected={selected}></ProjectRow>; }) }
            </ul>
        );
    }
});

ReactDOM.render(
        <ProjectList />,
        document.getElementById('projects-list')
);

var ProjectInfo = React.createClass({
    render: function() {
        for(var i=0; i<this.props.project.length; i++){
            if(this.props.project[i].id===this.props.selected){
                var p = this.props.project[i];
                break;
            }
        }
        console.log(p);
        return (
        <div>
            <h1>{p.hrn}</h1>
            <h4>{p.id}</h4>
            <dl>
                <dt>visibility:</dt>
                <dd>{p.visibility}&nbsp;</dd>
                <dt>url:</dt>
                <dd><a href="{p.url}" target="_blank">{p.url}</a>&nbsp;</dd>
                <dt>description:</dt>
                <dd>{p.description}&nbsp;</dd>
                <dt>start:</dt>
                <dd>{p.start_date}&nbsp;</dd>
                <dt>end:</dt>
                <dd>{p.end_date}&nbsp;</dd>
            </dl>
            <div className="panel panel-default">
              <div className="panel-heading">
                <h3 className="panel-title">Users</h3>
              </div>
              <div className="panel-body">
                <ul>
                {p.pi_users.map(function(listValue, i){
                  return <li key={i}>{listValue}</li>;
                })}
                </ul>
              </div>
            </div>
            <div className="panel panel-default">
              <div className="panel-heading">
                <h3 className="panel-title">Experiments</h3>
              </div>
              <div className="panel-body">
                <ul>
                {p.slices.map(function(listValue, i){
                  return <li key={i}>{listValue}</li>;
                })}
                </ul>
              </div>
            </div>
        </div>
        );
    }
});
var UserRow = React.createClass({
     /*
     getInitialState () {
        return {
        'selected':false
        };
     },
     */
     handleClick(){
        console.log(this.state);
        //projectactions.selectProject(this.props.project);
        /*
        if(this.state.selected){
            this.setState({'selected':false});
        }else{
            this.setState({'selected':true});
        }
        */
     },
     render: function() {
         if(this.props.selected == this.props.project.id){
            var liClass = 'elementBox selected';
         }else{
            var liClass = 'elementBox';
         }
         return (
             <li className={liClass} onClick={this.handleClick}>
                 <div className="row">
                     <div className="col-md-6">
                         <div className="elementId">
                             {this.props.user.id}
                         </div>
                         <div>
                             {this.props.user.first_name} {this.props.user.last_name}
                         </div>

                     </div>
                     <div className="col-md-6">

                     </div>
                 </div>
             </li>
         );
     }
 });
var ProjectRight = React.createClass({
    getInitialState: function() {
        return projectstore.getState();
    },

    componentDidMount: function() {
        

    // listen on state changes
    projectstore.listen(this.onChange);
    },

    componentWillUnmount() {
        projectstore.unlisten(this.onChange);
    },

    onChange(state) {
        this.setState(state);
    },

    render: function() {
        var selected = this.state.selected;
        var project = this.state.project;
        if (this.state.errorMessage) {
            return (
                <div>Something is wrong</div>
            );
        }
        if(selected==null){
            return(
            <div>
            <Title></Title>
            <ProjectForm></ProjectForm>
            </div>
            ) 
        }else{
            return (<ProjectInfo key={selected} project={project} selected={selected}></ProjectInfo>);
        }
    }
});

ReactDOM.render(
        <ProjectRight />,
        document.getElementById('projects-right')
);
ReactDOM.render(
        <ProjectAdd />,
        document.getElementById('project-add')
);
