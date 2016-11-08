import React from 'react';

import List from '../base/List';

import Element from '../base/Element';
import ElementTitle from '../base/ElementTitle';
import ElementId from '../base/ElementId';
import DateTime from '../base/DateTime';

import DeleteSliceFromProject from '../DeleteSliceFromProject';

class SliceElement extends React.Component {

    render() {
        var label = this.props.slice.name || this.props.slice.shortname;
        var project = this.props.slice.project.name || this.props.slice.project.shortname;
        var authority = this.props.slice.authority.name || this.props.slice.authority.shortname;
        var button = '';
        var link = "/slices/"+this.props.slice.hrn;
        if(this.props.removeSlice){
            button = <DeleteSliceFromProject slice={this.props.slice} />
        }

        var options = [
            'delete',
            'test'
        ];
        return (
             <Element element={this.props.slice}
                      type="slice"
                      select={this.props.select}
                      status={this.props.slice.status}
                      options={options}
                      icon="slice"
             >

                 <a href={link}><ElementTitle label={label} detail={this.props.slice.shortname} /></a>
                 <ElementId id={this.props.slice.id} />
                 {button}
                 <div className="elementDetail">
                     <span className="elementLabel">Part of project</span> {project}
                     <br />
                     <span className="elementLabel">Managed by</span> {authority}
                 </div>
                 <div className="row elementDate">
                     <div className="col-sm-3">
                         <span className="elementLabel">Created</span>
                         <br />
                         <DateTime timestamp={this.props.slice.created} />
                     </div>
                     <div className="col-sm-3">
                         <span className="elementLabel">Enabled</span>
                         <br />
                         <DateTime timestamp={this.props.slice.enabled} />
                     </div>
                     <div className="col-sm-3">
                         <span className="elementLabel">Updated</span>
                         <br />
                         <DateTime timestamp={this.props.slice.updated} />
                     </div>
                 </div>
             </Element>
         );
    }
}

SliceElement.propTypes = {
    slice: React.PropTypes.object.isRequired,
    removeSlice: React.PropTypes.bool,
    select: React.PropTypes.bool
};

SliceElement.defaultProps = {
    select: false,
    removeSlice: false,
};


class SliceList extends React.Component {

    render() {
        return (
            <List>
            {
                this.props.slices.map(function(slice) {
                    return <SliceElement key={slice.id} slice={slice} setCurrent={this.props.setCurrent} current={this.props.current} removeSlice={this.props.removeSlice} />;
                }.bind(this))
            }
            </List>
        );
    }
}

SliceList.propTypes = {
    slices: React.PropTypes.array.isRequired,
    current: React.PropTypes.object,
    removeSlice: React.PropTypes.bool,
    setCurrent: React.PropTypes.func
};

SliceList.defaultProps = {
    current: null,
    setCurrent: null,
    removeSlice: false,
};

export { SliceElement, SliceList};
