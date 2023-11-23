import { useState, useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { useNavigate, useLocation } from 'react-router-dom';
import { MdDashboard } from 'react-icons/md';
import { FiLogOut } from 'react-icons/fi';
import clearReducer  from '../../../utils/common';
import ProjectList from './ProjectList';
import './Sidebar.css';

const Sidebar = () => {
  const [isProject, setIsProject] = useState(false);
  const [currentPath, setCurrentPath] = useState("");
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const location = useLocation();

  const handleLogout = () => {
    navigate('/login');
    clearReducer(dispatch);
  }

  useEffect(() => {
      const isPathIncludes = location.pathname.includes("project");
      setIsProject(isPathIncludes);
      setCurrentPath(location.pathname)
  },[location.pathname]);

  // Function to handle link clicks
  const handleLinkClick = (link) => {
    setCurrentPath(link);
  };

  return (
    <nav className="sidebar">
      <ul className="navbar-list">
        <li className={currentPath === '/dashboard' ? 'navbar-item active-bg' : 'navbar-item'} >
          <a href="/dashboard" data-testid="dash-link"
            className={currentPath === '/dashboard' ? 'navbar-link active-link' : 'navbar-link'} 
            onClick={() => handleLinkClick('/dashboard')}>
              <MdDashboard className="navbar-icon" />
            Dashboard
          </a>
        </li>

        {isProject && <ProjectList currentPath={currentPath} handleLinkClick={handleLinkClick}/>}

      </ul>
      <div className="row logout">
        <span className="btn-logout">
          <FiLogOut className="logout-icon" onClick={handleLogout} data-testid="logout-icon"/>
        </span>
      </div>
    </nav>
  )
}

export default Sidebar
