import { clearProjectDetailData,setProjectDetailData } from "../ProjectReducer";


describe('Dashboard Tiles Redux Slice', () => {

    it('should clear Project data', () => {
        const initialState = {
          isLoading: true,
          ProjectData: {},
          errors: {},
        };
      
        const nextState = clearProjectDetailData(initialState);
      
        expect(nextState).toEqual({
        payload:{
          isLoading: true,
          ProjectData: {},
          errors: {},
        },
          type: 'projectDetailData/clearProjectDetailData',
        });
      });



      it('should set loading state', () => {
        const initialState = {
          isLoading: false,
          ProjectData: {},
          errors: {},
        };
      
        const action = setProjectDetailData(initialState);
        expect(action.payload.isLoading).toBe(false);
      });
      

})