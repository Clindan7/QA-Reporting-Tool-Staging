import PropTypes from 'prop-types';
import './DashboardCard.css'

const CardContent = ({ title, content }) => {
    const shouldTruncate = content && content.length > 10;

    return (
        <div className="row">
            <div className="col-6">
                <p className="card-text card_content_style" >
                    {title}
                </p>
            </div>
            <div className="col-6 pos-rel">
                <p className="card-text card_content_style truncate-text">
                    {shouldTruncate ? (
                        <>
                            {content.slice(0, 10)}...
                            <span className="tooltip">{content}</span>
                        </>
                    ) : (
                        content
                    )}
                </p>
            </div>
        </div>
    )
}

CardContent.propTypes = {
    title: PropTypes.string,
    content: PropTypes.any
}

export default CardContent
