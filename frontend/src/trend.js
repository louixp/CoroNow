// class for trend pop-over window
import React from "react";
import "./index.css";
import ReactWordcloud from "react-wordcloud";
import "d3-transition";
import { select } from "d3-selection";
import Overlay from "react-bootstrap/Overlay";

class Trend extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      state: "init"
    };
  }

  render() {
    if (this.state.state === "init") {
      // render an overlay
    }
  }
}
