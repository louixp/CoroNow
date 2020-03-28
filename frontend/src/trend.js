// class for trend pop-over window
import React from "react";
import "./index.css";
import "d3-transition";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";

class Trend extends React.Component {
    // props: enable, text, handleClose
    constructor({props}) {
        super(props);
        this.state = {
            state: "init",
        };
    }

    render() {
        if (this.state.state === "init") {
            // render an overlay
            const new_trend_window = (
                <Modal 
                    show={this.props.enable} 
                    onHide={this.props.handleClose} 
                    animation={true}
                    centered
                >
                    <Modal.Header closeButton>
                        <Modal.Title>Trend</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>{this.props.text}</Modal.Body>
                    <Modal.Footer>
                        <Button variant="secondary" onClick={this.props.handleClose}>
                            Close
                        </Button>
                    </Modal.Footer>
                </Modal>
            );

            return new_trend_window;
        }
    }
}

export default Trend;
