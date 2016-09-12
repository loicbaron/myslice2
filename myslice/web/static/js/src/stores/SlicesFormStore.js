import alt from '../alt';
import source from '../sources/SlicesSource';
import actions from '../actions/SlicesFormActions';

class SlicesFormStore {

    constructor() {
        this.bindListeners({
            initComponent: actions.INIT_COMPONENT,
            updateLabel: actions.UPDATE_LABEL,
            updateName: actions.UPDATE_NAME,
            updateProject: actions.UPDATE_PROJECT,
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
        this.label = '';
        this.name = '';
        this.project = '';
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
        this.message['type'] = "success";
        this.message['msg'] = "Slice "+this.name+" has been created.";
    }

    submitError(response) {
        this.message['type'] = "error";
        this.message['msg'] = response.data.error;
    }
}

export default alt.createStore(SlicesFormStore, 'SlicesFormStore');
