import alt from '../../alt';
import actions from '../../actions/base/ElementActions';

class ElementStore {

    constructor() {
        this.selected = null;

        this.bindListeners({
            selectElement: actions.SELECT_ELEMENT,
        });

    }

    selectElement(selected) {
        this.selected = selected;
    }

}

export default alt.createStore(ElementStore, 'ElementStore');