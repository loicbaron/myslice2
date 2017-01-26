/**
 * Created by amirabradai on 14/10/2016.
 */
import alt from '../../alt';
import actions from '../../actions/views/Dashboard';
import source from '../../sources/views/Dashboard';

var removeFromArray = function(myArray, searchTerm, property=null) {
        for(var i = 0, len = myArray.length; i < len; i++) {
            if(property==null){
                var a = myArray[i];
            }else{
                var a = myArray[i][property];
            }
            if (a === searchTerm){
                myArray.splice(i, 1);
                return myArray;
            }
        }
        return myArray;
};

class DashboardStore {

    constructor() {


        this.filter = [];

        this.dialog = null;


        this.bindListeners({

            updateSlices: actions.UPDATE_SLICES,
            fetchProjects: actions.FETCH_PROJECTS,
            errorProjects: actions.ERROR_PROJECTS,
            showDialog: actions.SHOW_DIALOG,
            updateProjects: actions.UPDATE_PROJECTS,

        });

        this.registerAsync(source);
    }

    fetchProjects(filter) {

        this.filter = filter;

        if (!this.getInstance().isLoading()) {
            this.getInstance().fetch();
        }

    }
    updateProjects(projects) {
        if (projects.hasOwnProperty('data')) {
            this.projects = projects.data.result;
        } else {
            this.projects = projects;
        }
    }

    showDialog(dialog) {
        this.dialog = dialog;
    }
    updateSlices(slices) {
        if (slices.hasOwnProperty('data')) {
            this.current.slices = slices.data.result;
        } else {
            this.current.slices = slices;
        }
    }
    errorProjects(errorMessage) {
        console.log(errorMessage);
    }

}


export default alt.createStore(DashboardStore, 'DashboardStore');

