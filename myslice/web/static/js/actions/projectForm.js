/**
 * Project view actions
 *
 */

class ProjectFormActions {
    postForm() {
        //console.log(projectformstore.state);
        var v = 'public';
        if(projectformstore.state.v_public) v = 'public';
        if(projectformstore.state.v_protected) v = 'protected';
        if(projectformstore.state.v_private) v = 'private';

        return (dispatch) => {
            // we dispatch an event here so we can have "loading" state.
            dispatch();
            axios.post('/api/v1/projects', {
                    'data':{
                        'label': projectformstore.state.label,
                        'name':  projectformstore.state.name,
                        'visibility': v,
                        'url': projectformstore.state.url,
                        'description': projectformstore.state.description,
                        'start_date': projectformstore.state.start_date,
                        'end_date': projectformstore.state.end_date,
                    }
            }).then(function (response) {
                console.log(response);
                alt.recycle(projectformstore);
            }.bind(this)).catch(function (response) {
                console.log(response);
                console.log("error");
            }.bind(this));

        }
    }
    updateLabel(label){
        return label;
    }
    updateName(name){
        return name;
    }
    updatePublic(v_public){
        return v_public;
    }
    updateProtected(v_protected){
        return v_protected;
    }
    updatePrivate(v_private){
        return v_private;
    }
    updateUrl(url){
        return url;
    }
    updateDescription(description){
        return description;
    }
    updateStartDate(start_date){
        return start_date;
    }
    updateEndDate(end_date){
        return end_date;
    }
}

window.projectformactions = alt.createActions(ProjectFormActions);
