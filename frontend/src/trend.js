// class for trend pop-over window
import React from "react";
import "./index.css";
import "d3-transition";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";
import Wordtrend from "./wordtrend.js";

class Trend extends React.Component {
  // props: enable, text, handleClose
  constructor(props) {
    super(props);
    this.state = {
      state: "init"
    };
  }

  render() {
    if (this.state.state === "init") {
      // render an overlay
      const new_trend_window = (
        <Modal
          show={this.props.enable}
          onHide={this.props.handleClose}
          animation={false}
          size="xl"
          centered
        >
          <Modal.Header closeButton>
            <Modal.Title>
              Trend of "{this.props.text.toUpperCase()}" over Past 24 Hours
            </Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <Wordtrend data={this.props.currentTrend} />
          </Modal.Body>
        </Modal>
      );

      return new_trend_window;
    }
  }
}

export default Trend;
