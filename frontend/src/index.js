import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import WordCloud from "./wordcloud.js";

// function Word(props) {
//     let size_str = (5*props.weight).toString() + "px";
//     let style_obj = {
//         fontSize: size_str,
//         padding: "0px",
//     };
//     console.log(size_str)
//     return <button id="word_cloud_bubble" style={style_obj}>{props.text}</button>;
// }

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
