import alt from '../alt';

class ProjectsFormActions {
   
    normaliseLabel(label){
        return label.replace(/[^a-z0-9]+/gi, '').replace(/^-*|-*$/g, '').toLowerCase();
    }
 
    updateLabel(label){
        return label;
    }
    updateName(name){
        return name;
    }
    updateAuthority(authority){
        console.log("actions: "+authority);
        return authority;
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

export default alt.createActions(ProjectsFormActions);
