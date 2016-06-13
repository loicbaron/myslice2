import alt from '../alt';

class ProjectsFormActions {
    
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

    loading(loading) {
        return loading;
    }

    submitForm() {
        this.loading(true);
        return true;
    }

    submitSuccess(response) {
        this.loading(false);
        return response;
    }

    submitError(response) {
        this.loading(false);
        return response;
    }
}

module.exports = alt.createActions(ProjectsFormActions);
