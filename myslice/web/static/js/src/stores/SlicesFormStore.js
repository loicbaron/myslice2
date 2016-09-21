import alt from '../alt';
import source from '../sources/Slice';
import actions from '../actions/SlicesFormActions';

class SlicesFormStore {

    constructor() {
        this.label = '';
        this.name = '';
        this.project = '';

        this.bindListeners({
            updateLabel: actions.UPDATE_LABEL,
            updateName: actions.UPDATE_NAME,
            updateProject: actions.UPDATE_PROJECT,
            normaliseLabel: actions.NORMALISE_LABEL,
            updateLoading: actions.LOADING,
            submitForm: actions.SUBMIT_FORM,
            submitSuccess: actions.SUBMIT_SUCCESS,
            submitError: actions.SUBMIT_ERROR,
        });

        this.registerAsync(source);
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
    updateProject(project) {
        this.project = project;
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

export default alt.createStore(SlicesFormStore, 'SlicesFormStore');
