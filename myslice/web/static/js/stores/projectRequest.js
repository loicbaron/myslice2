/**
 * Project Store
 */

class ProjectRequestStore {

    constructor() {
        this.project = []
        this.errorMessage = null;

        this.bindListeners({
            updateProjectElement: projectrequestactions.updateProjectElement,
            updateProject: projectrequestactions.updateProject,

        });


    }

    updateProjectElement(project) {
        console.log("STORAGE UPD ACTIVITY:" + project.id)
        // Check if we already have this project in the state
        let index = this.project.findIndex(function(projectElement) {
            if (projectElement.id === project.id) {
                return true;
            }
            return false;
        });
        /*  If we do we update it, otherwise we add a new
            project event to the state (at the top of the array) */
        if (index !== -1) {
            this.project[index] = project;
        } else {
            this.project.unshift(project);
        }

        this.errorMessage = null;
        // optionally return false to suppress the store change event
    }

    updateProject(project) {
        this.project = project;
    }

}


window.projectrequeststore = alt.createStore(ProjectRequestStore, 'ProjectRequestStore');

