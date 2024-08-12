import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface College {
  school_name: string;
  school_city: string;
  school_state: string;
  college_board_code: string;
}

interface CollegesState {
  data: College[];
}

const initialState: CollegesState = {
  data: [],
};

const collegesSlice = createSlice({
  name: 'colleges',
  initialState,
  reducers: {
    setColleges(state, action: PayloadAction<College[]>) {
      state.data = action.payload;
    },
  },
});

export const { setColleges } = collegesSlice.actions;

export default collegesSlice.reducer;
