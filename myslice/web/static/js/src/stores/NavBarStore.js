import alt from '../alt';
import actions from '../actions/NavBarActions';
import source from '../sources/NavBarSource';

class NavBarStore {

    constructor() {
        /* the list of user slices to show on the menu */
        this.slices = [];
        this.projects = [];

        /* the currently active slice */
        this.currentSlice = {};

        /* show/hide the Slices menu */
        this.slicesMenu = false;

        this.bindListeners({
            setCurrentSlice: actions.SET_CURRENT_SLICE,
            updateSliceElement: actions.UPDATE_SLICE_ELEMENT,
            updateSlices: actions.UPDATE_SLICES,
            updateProjects: actions.UPDATE_PROJECTS,
            fetchSlices: actions.FETCH_SLICES,
            fetchProjects: actions.FETCH_PROJECTS,
            showMenu: actions.SHOW_MENU
        });

        this.registerAsync(source);


    }

    fetchSlices() {

        if (!this.getInstance().isLoading()) {
            this.getInstance().fetch();
        }

    }
    fetchProjects() {

        if (!this.getInstance().isLoading()) {
            this.getInstance().getProjects();
        }

    }
    /*
        set the current slice
        - from the url if we are in /slices/example.slice.hrn
        - from the localstorage if available
        - if the slice is not found defaults to the first one
        - or empty otherwise
     */
    setCurrentSlice(hrn = null) {
        var index = null;

        if (hrn) {
            index = this.slices.findIndex(function(s) {
                return (s.hrn === hrn);
            });
        } else {
            let id = localStorage.getItem('slice');
            index = this.slices.findIndex(function(s) {
                return (s.id === id);
            });
        }

        if (index !== -1) {
            this.currentSlice = this.slices[index];
        } else if (this.slices.length > 0) {
            this.currentSlice = this.slices[0];
        } else {
            this.currentSlice = {
                    id: null
            }
        }

        localStorage.setItem('slice', this.currentSlice.id);

    }

    updateSliceElement(slice) {
        let index = this.slices.findIndex(function(sliceElement) {
            return (sliceElement.id === slice.id);
        });

        if (index !== -1) {
            this.slices[index] = slice;
        } else {
            this.slices.unshift(slice);
        }

        this.errorMessage = null;
    }

    /*
        Every time we update the slice list we also check the
        current slice
     */
    updateSlices(slices) {
        if (slices.hasOwnProperty('data')) {
            this.slices = slices.data.result;
        } else {
            this.slices = slices;
        }

        var u = window.location.href.toString().split(window.location.host)[1].split('/');
        var hrn = u[2];
        var ctl = u[1];

        if (ctl === 'slices') {
            this.setCurrentSlice(hrn);
        } else {
            this.setCurrentSlice();
        }
    }

    updateProjects(projects) {
        if (projectss.hasOwnProperty('data')) {
            this.projects = projects.data.result;
        } else {
            this.projects = projects;
        }
    }

    showMenu(show) {
        this.slicesMenu = show;
    }

}


export default alt.createStore(NavBarStore, 'NavBarStore');

