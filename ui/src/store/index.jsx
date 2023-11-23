import { configureStore } from "@reduxjs/toolkit";
import rootReducer from '../store/RootReducer';

import { persistStore, persistReducer } from 'redux-persist';
import thunkMiddleware from 'redux-thunk';
import storage from 'redux-persist/lib/storage'

const persistConfig = {
    key: "root",
    storage,
}
const persistedReducer = persistReducer(persistConfig, rootReducer)

export const store = configureStore({
    reducer: persistedReducer,
    middleware: [thunkMiddleware],
})
const persistor = persistStore(store);
export { persistor };
export default store;