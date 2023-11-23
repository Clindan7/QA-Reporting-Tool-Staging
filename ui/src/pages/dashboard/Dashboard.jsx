import { useCallback, useEffect, useState } from 'react';
import { BsSearch } from 'react-icons/bs';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from "react-router-dom";
import DashboardCard from '../../components/dashboard/DashboardCard';
import ProjectAction from '../../redux/actions/ProjectActions';

import './Dashboard.css';
import LoadingScreen from '../../components/ui/loader/Loader';

const Dashboard = () => {
  const tileData = useSelector((state) => state?.DashboardReducer?.DashboardData || {});
  const isLoading = useSelector((state) => state?.DashboardReducer?.isLoading)
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [searchInput, setSearchInput] = useState("");
  const [filterInput, setFilterInput] = useState(1);

  const getDashboardData = useCallback(async () => {
    dispatch(ProjectAction.DashboardTilesAsync(searchInput, filterInput))
  }, [dispatch, searchInput, filterInput])

  useEffect(() => {
    getDashboardData();
  }, [searchInput, filterInput, getDashboardData])


  const handleSearch = (e) => {
    const keyword = e.target.value;
    setSearchInput(keyword);
  };

  const handleStatusChange = (e) => {
    const filter = e.target.value;
    setFilterInput(filter);
  };

  return (
    <>
      {isLoading && <LoadingScreen />}

      <div className='dashBox'>
        <div className="top-filters pad-left">
          <div className='filter-size'>
            <select className='filter-box' placeholder="Filter by status" onChange={handleStatusChange}>
              <option value="1">Ongoing</option>
              <option value="0">Completed</option>
            </select>
          </div>

          <div className="input-group search-size" >
            <input
              type="text"
              className="search-box"
              placeholder="Search Project"
              onChange={handleSearch}
              value={searchInput} />
            <span className="input-group-text icon-span" ><BsSearch className="icon" /></span>
          </div>
        </div>


        <div className="row tile-style ">
          {tileData?.length > 0 ?
            (tileData?.map((project) => (
              <div className="card card_style col-4"
                key={project.id} onClick={() => navigate(`/project/${project.id}`)}>
                <DashboardCard project={project} />
              </div>
            ))) : <p className='no_data'>No Data Found !!</p>}
        </div>
      </div>

    </>
  );
}

export default Dashboard
