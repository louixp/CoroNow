import React from "react";
import "./index.css";
import ReactWordcloud from "react-wordcloud";
import "d3-transition";
import { select } from "d3-selection";

function wordCloudCallBack(callback_str) {
  return function(word, event) {
    const isActive = callback_str !== "onWordMouseOut";
    const element = event.target;
    const text = select(element);
    text
      .transition()
      // .attr('background', 'white')
      .attr("text-decoration", isActive ? "underline" : "none");
  };
}

const wordcloud_options = {
  colors: ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"],
  enableTooltip: true,
  deterministic: false,
  fontFamily: "helvetica",
  fontSizes: [20, 70],
  fontStyle: "normal",
  fontWeight: "bold",
  padding: 1,
  rotations: 2,
  rotationAngles: [-45, 45],
  scale: "sqrt",
  spiral: "archimedean",
  transitionDuration: 500
};

// wordcloud window, a div element, containing a bunch of words
class WordCloud extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      state: "init",
      words: props.words
    };
  }

  componentWillMount() {
    this.resize();
    window.addEventListener("resize", this.resize.bind(this));
    window.addEventListener("fullscreenchange", this.resize.bind(this));
  }

  resize() {
    var innerWidth = window.innerWidth;
    console.log(innerWidth);
    if (innerWidth < 500) wordcloud_options.fontSizes = [21, 56];
    else if (innerWidth < 1200) wordcloud_options.fontSizes = [24, 64];
    else if (innerWidth < 2000) wordcloud_options.fontSizes = [30, 80];
    else wordcloud_options.fontSizes = [30, 90];
  }

  shouldComponentUpdate(newProps, newStates) {
    console.log("will update: " + (this.props.ver !== newProps.ver));
    return this.props.ver !== newProps.ver;
  }

  wordClickCallback(word) {
    this.props.onWordClick(word);
  }

  wordCloudCallbacks = {
    // getWordColor: word => (word.value > 50 ? 'orange' : 'purple'),
    getWordTooltip: word => `See the trend of "${word.text}" on social media`,
    onWordClick: (word, event) => this.wordClickCallback(word.text),
    onWordMouseOut: wordCloudCallBack("onWordMouseOut"),
    onWordMouseOver: wordCloudCallBack("onWordMouseOver")
  };

  render() {
    console.log("wordcloud render");
    if (this.state.state === "init") {
      return (
        <div
          style={this.props.style}
          id={this.props.id}
        >
          <ReactWordcloud
            words={this.props.words}
            options={wordcloud_options}
            callbacks={this.wordCloudCallbacks}
          />
        </div>
      );
    }
  }
}

export default WordCloud;
