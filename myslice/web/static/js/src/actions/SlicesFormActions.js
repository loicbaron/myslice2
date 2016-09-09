import alt from '../alt';

class SlicesFormActions {
   
    normaliseLabel(label){
        return label.replace(/[^a-z0-9]+/gi, '').replace(/^-*|-*$/g, '').toLowerCase();
    }
 
    updateLabel(label){
        return label;
    }
    updateName(name){
        return name;
    }
    updateProject(project){
        return project;
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

    initComponent() {
        return true;
    }
}

export default alt.createActions(SlicesFormActions);
