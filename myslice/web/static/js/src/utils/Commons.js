class Commons {
    static containsObject(obj, list){
        if (typeof list != 'undefined'){
            for(var i=0; i<list.length; i++){            
                if(list[i].id==obj.id){
                    return true;
                }
            }
        }
        return false;
    }
    static removeFromArray(myArray, searchTerm, property=null) {
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
    }
}
export default Commons;
