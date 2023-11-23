import { useNavigate } from "react-router-dom";
import "./ErrorPage.css";


const ErrorPage=()=>{
const navigate=useNavigate()
return(
    <div>
      <div className="aligncenter">
        <div className="fourzerofourbg">
          <h1>404</h1>
        </div>

        <div className="contantbox404">
          <h3 className="h2">Look like you're lost</h3>

          <p>the page you are looking for not avaible!</p>

          <h3 className="link404" onClick={()=>{
            navigate("dashboard")
          }}>Go to Home</h3>
        </div>
      </div>
    </div>
)
}

export default ErrorPage