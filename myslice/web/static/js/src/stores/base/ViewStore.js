import alt from '../../alt';
import actions from '../../actions/base/ViewActions';

class ViewStore {

    constructor() {
        this.selectedElement = null;

        this.bindListeners({
            updateSelectedElement: actions.UPDATE_SELECTED_ELEMENT,
        });

    }

    updateSelectedElement(selectedElement) {
        this.selectedElement = selectedElement;
    }

}

export default alt.createStore(ViewStore, 'ViewStore');
