var alt = require('../alt');
var source = require('../sources/ProjectsSource');
import ProjectsFormActions from '../actions/ProjectsFormActions';

class ProjectsFormStore {

    constructor() {
        var d = new Date();
        var df = d.getFullYear()+"-"+(d.getMonth()+1)+"-"+d.getDate()+" "+d.getHours()+":"+ d.getMinutes()+":"+d.getSeconds()
        this.label = '';
        this.name = '';
        this.v_public = true;
        this.v_protected = false;
        this.v_private = false;
        this.url = '';
        this.description = '';
        this.start_date = df;
        this.end_date = '';


        this.bindListeners({
            updateLabel: ProjectsFormActions.UPDATE_LABEL,
            updateName: ProjectsFormActions.UPDATE_NAME,
            updatePublic: ProjectsFormActions.UPDATE_PUBLIC,
            updateProtected: ProjectsFormActions.UPDATE_PROTECTED,
            updatePrivate: ProjectsFormActions.UPDATE_PRIVATE,
            updateUrl: ProjectsFormActions.UPDATE_URL,
            updateDescription: ProjectsFormActions.UPDATE_DESCRIPTION,
            updateStartDate: ProjectsFormActions.UPDATE_START_DATE,
            updateEndDate: ProjectsFormActions.UPDATE_END_DATE,

            updateLoading: ProjectsFormActions.LOADING,
            submitForm: ProjectsFormActions.SUBMIT_FORM,
            submitSuccess: ProjectsFormActions.SUBMIT_SUCCESS,
            submitError: ProjectsFormActions.SUBMIT_ERROR,
        });

        this.registerAsync(source);
    }

    updateLabel(label) {
        this.label = label;
    }
    updateName(name) {
        this.name = name;
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

        this.message = response.data.error;
    }

    submitError(response) {

        this.message = response.data.error;
    }
}

export default alt.createStore(ProjectsFormStore, 'ProjectsFormStore');
