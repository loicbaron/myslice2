var Resource = React.createClass({
     getDefaultProps: function() {
         return {
             resource: {
                 "testbed" : null,
                 "hostname" : null,
                 "state" : null,
                 "access": { "status": false, "message": "pending", "timestamp": null }
             }
         };
     },

     render: function() {
         if (typeof this.props.resource.access == 'undefined') {
             this.props.resource.access = { "status": false, "message": "pending" }
         }
         return (
             <tr>
                 <td>{this.props.resource.testbed}</td>
                 <td className="resource">{this.props.resource.hostname}</td>
                 <td>{this.props.resource.state}</td>
                 <td>{this.props.resource.access.status} ({this.props.resource.access.message})</td>
                 <td>{this.props.resource.timestamp}</td>
             </tr>
         );
     }
 });