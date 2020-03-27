import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import ReactWordcloud from 'react-wordcloud';
import { Resizable } from 're-resizable';

const resizeStyle = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    border: 'solid 1px #ddd',
    background: '#f0f0f0',
  };


function Word(props) {
    let size_str = (5*props.weight).toString() + "px";
    let style_obj = {
        fontSize: size_str,
        padding: "0px",
    };
    console.log(size_str)
    return <button id="word_cloud_bubble" style={style_obj}>{props.text}</button>;
} 


// wordcloud window, a div element, containing a bunch of words
class WordCloud extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            state: "init",
            words: [],
        };
        this.getWordCloud();
    }

    getWordCloud() {
        // fetch a wordcloud json from backend server
        fetch("/api/wordcloud", {
            method: "GET",
            cache: "no-cache",
            headers: {
                "Content-type": "application/json",
            },
            redirect: "follow",
        })
            .then((res) => res.json())
            .then((res) => {
                // let new_words = [];
                // res.words.forEach(el => {
                //     new_words.push(el);
                // });
                // console.log(new_words);
                console.log(res.words);
                this.setState({
                    state: "display",
                    words: res.words,
                });
            });
    }

    render() {
        if (this.state.state === "init") {
            return (
                <div>
                    <Word text='nothing here'/>
                </div>
            )
        }
        else if (this.state.state === "display") {
            return (
                <div>
                <p>Resize the container!</p>
                    <Resizable
                        defaultSize={{
                        width: 600,
                        height: 300,
                        }}
                        style={resizeStyle}>
                        <div style={{ width: '100%', height: '100%' }}>
                            <ReactWordcloud words={this.state.words} />
                        </div>
                    </Resizable>
                </div>
            )
        }
    }
}


// main frame of home page
class Main extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            state: "init", // states: init, trial
        }
    }

    render() {
        if (this.state.state === "init") {
            return (
                <WordCloud />
            );
        }
    }
}


ReactDOM.render(<Main />, document.getElementById('root'));
