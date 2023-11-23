import { useState, useCallback, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { PiDiamondsFourBold } from 'react-icons/pi';
import { BsSearch } from 'react-icons/bs';
import PropTypes from 'prop-types';
import ProjectAction from '../../../redux/actions/ProjectActions';
import LoadingScreen from '../../ui/loader/Loader';
import './Sidebar.css';

const ProjectList = ({ currentPath, handleLinkClick }) => {
    const projectList = useSelector((state) => state?.DashboardReducer?.DashboardData);
    const isLoading = useSelector((state) => state?.DashboardReducer?.isLoading);
    const projectDetailList = useSelector((state) => state?.ProjectReducer?.ProjectData);
    const dispatch = useDispatch();
    const [searchInput, setSearchInput] = useState("");
    const filterInput = 1;

    const getProjectList = useCallback(async () => {
        dispatch(ProjectAction.DashboardTilesAsync(searchInput, filterInput))
    }, [dispatch, searchInput])

    useEffect(() => {
        getProjectList();
    }, [searchInput, projectDetailList, getProjectList])

    const handleSearch = (e) => {
        const keyword = e.target.value;
        setSearchInput(keyword);
    };

    return (
        <div>
            <div className='input-group search-width'>
                <input
                    type="text"
                    placeholder="Search project"
                    className="searchbox"
                    onChange={handleSearch}
                    value={searchInput} />
                <span className="input-group-text iconspan" >
                    <BsSearch className="icon-search" />
                </span>
            </div>
            <div className='nav-projectlist'>
            {isLoading && <LoadingScreen />}
            {projectList?.length > 0 && projectList?.map((project) => (
                <li
                    className={currentPath.includes(`/project/${project.id}`) ? 'project-item active-bg' : 'project-item'}
                    key={project.id}>
                    <Link to={`/project/${project.id}`}
                        className={currentPath.includes(`/project/${project.id}`) ? 'project-link active-link' : 'project-link'}
                        onClick={() => handleLinkClick(`/project/${project.id}`)}>
                        <PiDiamondsFourBold className="project-icon" />
                        {project.name}
                    </Link>
                </li>
            ))}
            </div>
        </div>
    )
}

ProjectList.propTypes = {
    currentPath: PropTypes.any,
    handleLinkClick: PropTypes.any
}

export default ProjectList
