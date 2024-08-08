import { configureStore } from '@reduxjs/toolkit';
import { useDispatch } from 'react-redux';
import collegesReducer from './slices/collegesSlice';

const store = configureStore({
    reducer: {
        colleges: collegesReducer,
    },
});

export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType < typeof store.getState > ;

export const useAppDispatch = () => useDispatch < AppDispatch > ();
export default store;