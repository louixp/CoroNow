import React from "react";
import "./index.css";

class Sentiments extends React.Component {
    render() {
        return (
            <div
                style={{
                    height: "100%",
                    width: "100%"
                }}
                id={this.props.id}
            >
                <p>this is sentiment</p>
            </div>
        )
    }
}

function Sentiment_item(props) {
    return (
        <p>this is a sentiment analysis</p>
    )
}

export default Sentiments;
