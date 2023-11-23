import logo from '../../../assets/Logo11.svg'
import user from "../../../assets/user1.svg"
import { useNavigate } from 'react-router-dom';
import './Header.css';

const Header = () => {
  const username = localStorage.getItem("username");
  const navigate = useNavigate();
  return (
    <div className='row header d-flex justify-content-between'>
      <div className="header_logo col-2">
        <img src={logo} 
          className='logo_style'
          alt='Logo'
          onClick={() => {navigate(`/dashboard`); window.location.reload();}}
          ></img>
      </div>
      <div className="header_main col-10" data-testid="user-session">
        <img src={user} alt="userlogo" className='user-icon' />
        <div className='usrname_align'>
          <span className="header_usrlabel">{username}</span>
        </div>
      </div>
    </div>

  )
}


export default Header
