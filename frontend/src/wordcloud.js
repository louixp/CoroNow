import React from "react";
import "./index.css";
import ReactWordcloud from "react-wordcloud";
import "d3-transition";
import { select } from "d3-selection";

function wordCloudCallBack(callback_str) {
    return function(word, event) {
        const isActive = callback_str !== 'onWordMouseOut';
        const element = event.target;
        const text = select(element);
        text
          .on('click', () => {
              if (isActive) {
                  // window.open(`https://duckduckgo.com/?q=${word.text}`, '_blank');
                  // TODO: add a function to display trend line of this word
                  alert(word.text);
              }
          })
          .transition()
          // .attr('background', 'white')
          .attr('text-decoration', isActive ? 'underline' : 'none');
    };
}

const callbacks = {
    // getWordColor: word => (word.value > 50 ? 'orange' : 'purple'),
    getWordTooltip: word =>
        `See the trend of "${word.text}" on social media`,
    onWordClick: wordCloudCallBack('onWordClick'),
    onWordMouseOut: wordCloudCallBack('onWordMouseOut'),
    onWordMouseOver: wordCloudCallBack('onWordMouseOver'),
};

const wordcloud_options = {
    colors: ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"],
    enableTooltip: true,
    deterministic: false,
    fontFamily: "helvetica",
    fontSizes: [10, 70],
    fontStyle: "normal",
    fontWeight: "normal",
    padding: 1,
    rotations: 3,
    rotationAngles: [0, 90],
    scale: "sqrt",
    spiral: "archimedean",
    transitionDuration: 1000
};

// wordcloud window, a div element, containing a bunch of words
class WordCloud extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
        state: "init",
        words: []
        };
        this.getWordCloud();
    }

    getWordCloud() {
        // fetch a wordcloud json from backend server
        fetch("/api/wordcloud", {
            method: "GET",
            cache: "no-cache",
            headers: {
                "Content-type": "application/json"
            },
            redirect: "follow"
        })
            .then(res => res.json())
            .then(res => {
                console.log(res.words);
                this.setState({
                state: "display",
                words: res.words
                });
            });
    }

    render() {
        if (this.state.state === "init") {
        return <p>Data not loaded</p>;
        } else if (this.state.state === "display") {
        return (
            <div style={{ width: "100%", height: "100%" }}>
            <div
                style={{ width: "100%", height: "100%" }}
                id="word-cloud-container"
            >
                <ReactWordcloud
                words={this.state.words}
                options={wordcloud_options}
                callbacks={callbacks}
                />
            </div>
            </div>
        );
        }
    }
}

export default WordCloud;
