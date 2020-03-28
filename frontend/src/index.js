import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import "bootstrap/dist/css/bootstrap.css"; // this file is required for Modal to work
import WordCloud from "./wordcloud.js";
import Trend from "./trend.js";

// main frame of home page
class Main extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      state: "init", // states: init, trend
      overlay_text: "",
      word_list_version: 0, // if there's need to update word list, increment this variable to notify wordcloud re-render
      words: [],
      wordcloud_height: "100%", // edit these 2 states to control wordcloud width and height
      wordcloud_width: "100%"
    };
    this.getWordList();
  }

  getWordList() {
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
          word_list_version: this.state.word_list_version + 1,
          words: res.words
        });
      });
  }

  // callback function for word clicking, display a trend overlay window
  activateTrend(text) {
    // fetch data here
    this.setState({
      state: "trend",
      overlay_text: text
      // add more data to pass in here
    });
  }

  // callback function for close window button on overlay, deactivate overlay window
  deactivateTrend() {
    this.setState({
      state: "init"
    });
  }

  render() {
    let trend_enable = false;
    if (this.state.state === "init") {
      trend_enable = false;
    } else if (this.state.state === "trend") {
      trend_enable = true;
    }

    console.log("main render");

    return (
      <div
        style={{
          width: "100%",
          height: "100%"
        }}
        id="main-div"
      >
        <WordCloud
          onWordClick={text => this.activateTrend(text)}
          words={this.state.words}
          ver={this.state.word_list_version}
          height={this.state.wordcloud_height}
          width={this.state.wordcloud_width}
        />{" "}
        <Trend
          enable={trend_enable}
          text={this.state.overlay_text}
          handleClose={() => {
            this.deactivateTrend();
          }}
        />{" "}
      </div>
    );
  }
}

ReactDOM.render(<Main />, document.getElementById("root"));
