import alt from '../alt';
import source from '../sources/ProjectsSource';
import actions from '../actions/ProjectsFormActions';

class ProjectsFormStore {

    constructor() {
        this.bindListeners({
            initComponent: actions.INIT_COMPONENT,
            updateLabel: actions.UPDATE_LABEL,
            updateName: actions.UPDATE_NAME,
            updateAuthority: actions.UPDATE_AUTHORITY,
            updatePublic: actions.UPDATE_PUBLIC,
            updateProtected: actions.UPDATE_PROTECTED,
            updatePrivate: actions.UPDATE_PRIVATE,
            updateUrl: actions.UPDATE_URL,
            updateDescription: actions.UPDATE_DESCRIPTION,
            updateStartDate: actions.UPDATE_START_DATE,
            updateEndDate: actions.UPDATE_END_DATE,
            normaliseLabel: actions.NORMALISE_LABEL,
            updateLoading: actions.LOADING,
            submitForm: actions.SUBMIT_FORM,
            submitSuccess: actions.SUBMIT_SUCCESS,
            submitError: actions.SUBMIT_ERROR,
        });
        this.initComponent();
        this.registerAsync(source);
    }
    initComponent(){
        var d = new Date();
        var df = d.getFullYear()+"-"+(d.getMonth()+1)+"-"+d.getDate()+" "+d.getHours()+":"+ d.getMinutes()+":"+d.getSeconds()
        this.label = '';
        this.name = '';
        this.authority = '';
        this.v_public = true;
        this.v_protected = false;
        this.v_private = false;
        this.url = '';
        this.description = '';
        this.start_date = df;
        this.end_date = '';
        this.message = {};
    }
    normaliseLabel(label){
        this.name = label;
    }
    updateLabel(label) {
        this.label = label;
    }
    updateName(name) {
        this.name = name;
    }
    updateAuthority(authority) {
        console.log("store: "+authority);
        this.authority = authority;
    }
    updatePublic(v_public) {
        this.v_public = v_public;
    }
    updateProtected(v_protected) {
        this.v_protected = v_protected;
    }
    updatePrivate(v_private) {
        this.v_private = v_private;
    }
    updateUrl(url) {
        this.url = url;
    }
    updateDescription(description) {
        this.description = description;
    }
    updateStartDate(start_date) {
        this.start_date = start_date;
    }
    updateEndDate(end_date) {
        this.end_date = end_date;
    }


    updateLoading(loading) {
        this.loading = loading;
    }

    submitForm() {

        if (!this.getInstance().isLoading()) {
            this.getInstance().submit();
        }
    }

    submitSuccess(response) {
        this.message['type'] = "success";
        this.message['msg'] = "Project "+this.name+" has been requested, it will apear in your dashboard after validation.";
        // XXX Should manage the PI case
        //this.message['msg'] = "Project "+this.name+" has been created.";
    }

    submitError(response) {
        this.message['type'] = "error";
        this.message['msg'] = response.data.error;
    }
}

export default alt.createStore(ProjectsFormStore, 'ProjectsFormStore');
