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
    static searchText(el, value){
        var k;
        for(k in el){
            if(Array.isArray(el[k]) || (typeof el[k] === 'object')){
                if(this.searchText(el[k], value)){
                    return true;
                }
            }else{
                if(el[k]!=null && el[k].toString().indexOf(value)>-1){
                    return true;
                }
            }
        }
        return false;
    }
}
export default Commons;
