import { combineReducers } from "redux";
import { productListReducers } from "./reducers/productReducers";

const rootReducer = combineReducers({
  productList: productListReducers,
});

export default rootReducer;
