import PropTypes from "prop-types";
import "./DetailContent.css"

const DetailContent=({title,content})=>{

    const shouldTruncate = content && content?.length > 25;
    return(
        <div className="row">
            <div className="col-6">
                <p className="card-text card_content_style" style={{paddingLeft:"25px",height:"35px"}}>
                    {title}
                </p>
            </div>
            <div className="col-6 pos-rel">
                <p className="card-text card_content_style truncate_text" style={{height:"35px",width:"100%"}}>
                {shouldTruncate ? (
                        <>
                            {content.slice(0, 25)}...
                            <span id="tooltip">{content}</span>
                        </>
                    ) : (
                        content
                    )}
                </p>
            </div>
        </div>
    )
}

DetailContent.propTypes={
    title: PropTypes.string,
    content:PropTypes.any
}

export default DetailContent