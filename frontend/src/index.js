import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import WordCloud from "./wordcloud.js";

// main frame of home page
class Main extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      state: "init" // states: init, trial
    };
  }

  render() {
    if (this.state.state === "init") {
      return (
        <div style={{ width: "100%", height: "100%" }}>
          <WordCloud />
        </div>
      );
    }
  }
}

ReactDOM.render(<Main />, document.getElementById("root"));
