import { PropagateLoader } from "react-spinners"
import "./loader.css"

const LoadingScreen = () => {
    return (
        <div className="loadingScreen" data-testid="loading-screen">
            <PropagateLoader color="#19B5FE" />
        </div>
    )
}

export default LoadingScreen