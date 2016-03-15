/*
 * action types
 */

const ADD_SLICE = 'ADD_SLICE'

/*
 * action creators
 */

function addSlice(name) {
  return { type: ADD_SLICE, name: name }
}

/*
 * dispatcher
 */

function Slice(state = [], action) {
    switch (action.type) {
        case ADD_SLICE:
            console.log('hello')
            return [
                ...state,
                {
                    text: action.name,
                    completed: false
                }
            ]
        //case COMPLETE_TODO:
        //    return state.map((todo, index) => {
        //        if (index === action.index) {
        //            return Object.assign({}, todo, {
        //                completed: true
        //            })
        //        }
        //        return todo
        //    })
        default:
            return state
  }
}

/*
 * Store
 */
let store = Redux.createStore(Slice)

// Every time the state changes, log it
// Note that subscribe() returns a function for unregistering the listener
let unsubscribe = store.subscribe( () =>
  console.log(store.getState())
)

// Dispatch some actions
store.dispatch(addSlice('Learn about actions'))
store.dispatch(addSlice('Learn about reducers'))
store.dispatch(addSlice('Learn about store'))
//store.dispatch(completeTodo(0))
//store.dispatch(completeTodo(1))

unsubscribe()