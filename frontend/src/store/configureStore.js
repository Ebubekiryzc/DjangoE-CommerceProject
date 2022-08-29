import { createStore, applyMiddleware } from "redux";
import thunk from "redux-thunk";
import { composeWithDevTools } from "redux-devtools-extension";
import rootReducer from "./rootReducer";

const userInfoFromStorage = localStorage.getItem('userInfo') ? JSON.parse(localStorage.getItem('userInfo')) : null

const middleware = [thunk];

const initialState = {
    userLogin: { userInfo: userInfoFromStorage }
}

export function configureStore() {
    return createStore(rootReducer,
        initialState,
        composeWithDevTools(applyMiddleware(...middleware)),
    );
}