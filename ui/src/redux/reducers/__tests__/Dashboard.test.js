import { clearDashboardTilesData,setDashboardTilesData,setDashboardTilesLoading ,setDashboardTilesError, slice} from "../DashboardReducer";

describe('Dashboard Tiles Redux Slice', () => {

    it('should clear dashboard data', () => {
        const initialState = {
          isLoading: true,
          DashboardData: {},
          errors: {},
        };
      
        const nextState = clearDashboardTilesData(initialState);
      
        expect(nextState).toEqual({
        payload:{
          isLoading: true,
          DashboardData: {},
          errors: {},
        },
          type: 'dashboardTilesData/clearDashboardTilesData',
        });
      });
      

  
      it('should set loading state', () => {
        const initialState = {
          isLoading: false,
          DashboardData: {},
          errors: {},
        };
      
        const action = setDashboardTilesLoading(initialState);
        expect(action.payload.isLoading).toBe(false);

      });
      
      it('should handle setDashboardTilesData', () => {
        const state = {
          isLoading: true,
          DashboardData: {},
          errors: {},
        };
        const newData = { someKey: 'someValue' };
        const newState=slice.reducer(state,setDashboardTilesData(newData))
        expect(newState).toEqual({
          isLoading: false,
          DashboardData: newData,
          errors: {},
        });
      });


      it('should handle setDashBoardTilesError',()=>{
        const state={
          isLoading:true,
          DashboardData:{},
          errors:{}
        };
        const newData={someKey:"someValue"};
        const newState=slice.reducer(state,setDashboardTilesError(newData))
        expect(newState).toEqual({
          isLoading:false,
          DashboardData:{},
          errors:newData
        })
      })
     



  });