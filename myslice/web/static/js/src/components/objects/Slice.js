import React from 'react';

import { List, ListSimple } from '../base/List';
import { Element, ElementOptions } from '../base/Element';
import ElementTitle from '../base/ElementTitle';
import ElementId from '../base/ElementId';
import DateTime from '../base/DateTime';
import { Icon } from '../base/Icon';

const SliceElement = ({slice, isSelected, handleSelect, options}) => {

    var label = slice.name || slice.shortname;
    var project = slice.project.name || slice.project.shortname;
    var authority = '';

    if (typeof slice.authority !== 'undefined') {
        authority = slice.authority.name || slice.authority.shortname;
    }

    var link = "/slices/" + slice.hrn;

    return (
         <Element type="slice"
                  element={slice}
                  isSelected={isSelected}
                  handleSelect={handleSelect}
                  status={status}
                  options={options}
         >

             <a href={link}><ElementTitle label={label} detail={slice.shortname} /></a>
             <ElementId id={slice.id} />
             <div className="elementDetail">
                 <span className="elementLabel">Part of project</span> {project}
                 <br />
                 <span className="elementLabel">Managed by</span> {authority}
             </div>
             <div className="row elementDate">
                 <div className="col-sm-3">
                     <span className="elementLabel">Created</span>
                     <br />
                     <DateTime timestamp={slice.created} />
                 </div>
                 <div className="col-sm-3">
                     <span className="elementLabel">Enabled</span>
                     <br />
                     <DateTime timestamp={slice.enabled} />
                 </div>
                 <div className="col-sm-3">
                     <span className="elementLabel">Updated</span>
                     <br />
                     <DateTime timestamp={slice.updated} />
                 </div>
             </div>
         </Element>
    );
};


SliceElement.propTypes = {
    slice: React.PropTypes.object.isRequired,
};

SliceElement.defaultProps = {
};

const SliceList = ({slices, selected, handleSelect, options}) => {

    let iconSelected = "arrow";

    if (selected) {
        if (selected instanceof Array) {
            iconSelected = "check";
        } else {
            selected = [selected];
        }
    }

    return (<List>
        {
            slices.map(function (slice) {

                let isSelected = false;
                if (selected) {
                    isSelected = selected.some(function (el) {
                        return el.id === slice.id;
                    });
                }

                return <SliceElement key={slice.id}
                                     slice={slice}
                                     isSelected={isSelected ? iconSelected : null}
                                     handleSelect={handleSelect}
                                     options={options}
                />;
            })
        }
    </List>);
};

SliceList.propTypes = {
    slices: React.PropTypes.array.isRequired,
};

SliceList.defaultProps = {
};

export { SliceElement, SliceList };