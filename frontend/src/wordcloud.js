import React from "react";
import "./index.css";
import ReactWordcloud from "react-wordcloud";

const wordcloud_options = {
  colors: ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"],
  enableTooltip: false,
  deterministic: false,
  fontFamily: "impact",
  fontSizes: [5, 60],
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
        // let new_words = [];
        // res.words.forEach(el => {
        //     new_words.push(el);
        // });
        // console.log(new_words);
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
            />
          </div>
        </div>
      );
    }
  }
}

export default WordCloud;
