import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';


class WordCloud extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            state: "init",
        };
    }

    render() {
        if (this.state.state == "init") {
            return <canvas/>;
        }
    }
}


class Main extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            state: "init", // states: init, trial
        }
    }

    render() {
        if (this.state.state === "init") {

            return <WordCloud/>;
        }
    }
}


ReactDOM.render(<Main />, document.getElementById('root'));
