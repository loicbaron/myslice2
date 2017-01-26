/**
 * Created by amirabradai on 14/10/2016.
 */
import alt from '../../alt';

class DashboardActions {

    fetchProjects(filter = {}) {
        return filter;
    }

    updateProject(project) {
        return project;
    }

    setCurrentProject(project) {
        return project;
    }
    showDialog(dialog) {
        return dialog;
    }
    errorProjects(errorMessage) {
        return errorMessage
    }
    updateSlices(slices) {
        return slices;
    }
    updateProjects(project) {
        return project;
    }
    fetchSlicesByProject(filter={}){
        return filter

    }
}

export default alt.createActions(DashboardActions);